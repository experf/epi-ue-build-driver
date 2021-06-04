import logging
import asyncio
from grpc import aio
import threading

from . import api_pb2
from . import api_pb2_grpc

from .helpers import get_or_create_eventloop

LOG = logging.getLogger(__name__)


class API(api_pb2_grpc.APIServicer):
    async def Status(self, request, context):
        return api_pb2.StatusResponse(code=200, message="OK")


class Server:
    DEFAULT_LISTEN_ADDR = "[::]:5000"

    server: aio.Server
    listen_addr: str

    def __init__(self, listen_addr=DEFAULT_LISTEN_ADDR):
        self.server = aio.server()
        self.listen_addr = listen_addr
        api_pb2_grpc.add_APIServicer_to_server(API(), self.server)
        self.server.add_insecure_port(self.listen_addr)
        self.loop = None

    async def _serve(self):
        LOG.info(f"Starting server on {self.listen_addr}")
        await self.server.start()
        try:
            LOG.info("Waiting for server termination...")
            await self.server.wait_for_termination()
        except KeyboardInterrupt:
            # Shuts down the server with 0 seconds of grace period. During the
            # grace period, the server won't accept new connections and allow
            # existing RPCs to continue within the grace period.
            await self.server.stop(0)

    def stop(self, done, grace=1.0):
        future = asyncio.run_coroutine_threadsafe(
            self.server.stop(grace),
            self.loop
        )
        future.add_done_callback(done)

    def run(self):
        LOG.info("Starting run...")
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self._serve())
        except Exception as error:
            LOG.error(f".run() {error}")
        LOG.info("Done w the run.")
