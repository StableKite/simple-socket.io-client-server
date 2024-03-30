import asyncio
from functools import partial
import sys
import socketio
from random import randint

from proto import EVENT_XY, TASK_PERIOD, StructXY, clinet_config
from utils import enable_logger, init_logger
import loguru

rand_int = partial(randint, -10000, 10000)


async def get_xy_data() -> StructXY:
    return StructXY(rand_int(), rand_int(), rand_int(), rand_int())


async def xy_task(sio: socketio.AsyncSimpleClient):
    data = await get_xy_data()
    send_data = data.model_dump()
    loguru.logger.debug(f"Sending data: {send_data} ({data})")
    await sio.emit(EVENT_XY, send_data)
    await asyncio.sleep(TASK_PERIOD)


async def manage_forever():
    config = clinet_config()
    async with socketio.AsyncSimpleClient(logger=loguru.logger) as sio:
        loguru.logger.info(f"Connecting to url=`{config['url']}`")

        await sio.connect(**config)
        while True:
            await xy_task(sio)


async def main_client():
    while True:
        try:
            await manage_forever()
        except InterruptedError:
            sys.exit(0)
        except Exception as e:
            loguru.logger.error(str(e))
            loguru.logger.warning("Reconnecting...")
        finally:
            await asyncio.sleep(2)


def main():
    init_logger("DEBUG", enable_logger=enable_logger())
    asyncio.run(main_client())


if __name__ == "__main__":
    main()
