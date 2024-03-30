import sys
import socketio
from aiohttp import web

from proto import EVENT_XY, StructXY, config_dict
from utils import enable_logger, init_logger
import loguru

sio = socketio.AsyncServer(async_mode="aiohttp")


@sio.on(EVENT_XY)
async def xy_event(sid, raw_data: bytes):
    data = StructXY.model_validate(raw_data)
    loguru.logger.info(f"Got data: {raw_data} ({data})")
    pass


def run_server(run_args: dict):
    app = web.Application()
    # app.router.add_get("/", index)
    sio.attach(app)
    loguru.logger.info(
        f"Create server on host={run_args['host']}; port={run_args['port']}"
    )
    return web.run_app(app, **run_args)


def main():
    init_logger("DEBUG", enable_logger=enable_logger())
    run_server(config_dict())


if __name__ == "__main__":
    sys.exit(main())
