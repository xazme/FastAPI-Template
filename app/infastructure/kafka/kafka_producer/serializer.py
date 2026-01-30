import pickle
import logging
from typing import Any

logger = logging.getLogger(__name__)


class SerializationError(Exception):
    pass


class Serializer:
    def serialize(self, data: Any) -> bytes:
        try:
            return pickle.dumps(data)
        except (pickle.PicklingError, TypeError, AttributeError) as e:
            logger.error(f"Failed to serialize data: {type(data).__name__}: {e}")
            raise SerializationError(
                f"Cannot serialize {type(data).__name__}: {e}"
            ) from e
        except RecursionError as e:
            logger.error(f"Recursion error while serializing: {e}")
            raise SerializationError("Circular reference detected in data") from e
        except MemoryError as e:
            logger.error(f"Memory error while serializing: {e}")
            raise SerializationError("Data too large to serialize") from e

    def serialize_key(self, key: Any) -> bytes | None:
        if key is None:
            return None

        if isinstance(key, bytes):
            return key

        if isinstance(key, str):
            try:
                return key.encode("utf-8")
            except UnicodeEncodeError as e:
                logger.error(f"Failed to encode key: {e}")
                raise SerializationError(f"Cannot encode key: {e}") from e

        return self.serialize(key)
