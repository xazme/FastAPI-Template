import pickle
import logging
from typing import Any

logger = logging.getLogger(__name__)


class DeserializationError(Exception):
    pass


class Deserializer:
    def deserialize(self, data: bytes) -> Any:
        try:
            return pickle.loads(data)
        except (pickle.UnpicklingError, EOFError, AttributeError, ValueError) as e:
            logger.error("Failed to deserialize data: %s", e)
            raise DeserializationError(f"Cannot deserialize data: {e}") from e

        except RecursionError as e:
            logger.error("Recursion error while deserializing: %s", e)
            raise DeserializationError(
                "Circular reference detected in serialized data"
            ) from e

        except MemoryError as e:
            logger.error("Memory error while deserializing: %s", e)
            raise DeserializationError(
                "Serialized data too large to deserialize"
            ) from e

    def deserialize_key(self, key: bytes | None) -> Any:
        if key is None:
            return None
        try:
            return key.decode("utf-8")
        except UnicodeDecodeError:
            return self.deserialize(key)
