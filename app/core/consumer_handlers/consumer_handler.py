import logging
from typing import Any

logger = logging.getLogger(__name__)


async def consumer_handler(msg: Any) -> None:
    logger.debug("Recieved message %s", msg)
    # put it
    print("&" * 50)
    print(msg)
