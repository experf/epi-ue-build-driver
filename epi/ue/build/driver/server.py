import logging
import asyncio
import grpc
from concurrent import futures

from . import api_pb2
from . import api_pb2_grpc

from . import _credentials

# LOG = logging.getLogger(__name__)

class SignatureValidationInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid signature")

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        # Example HandlerCallDetails object:
        #     _HandlerCallDetails(
        #       method=u'/helloworld.Greeter/SayHello',
        #       invocation_metadata=...)
        signature = _credentials.PASSWORD
        expected_metadata = (_credentials.PASSWORD_HEADER_KEY, signature)
        if expected_metadata in handler_call_details.invocation_metadata:
            return continuation(handler_call_details)
        else:
            return self._abortion


class API(api_pb2_grpc.APIServicer):
    def Status(self, request, context):
        return api_pb2.StatusResponse(code=200, message="OK")


class Server:
    DEFAULT_LISTEN_ADDR = "[::]:5000"

    server: grpc.Server
    listen_addr: str

    def __init__(self, listen_addr=DEFAULT_LISTEN_ADDR):
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=3),
            interceptors=(SignatureValidationInterceptor(),),
        )
        self.listen_addr = listen_addr

        api_pb2_grpc.add_APIServicer_to_server(API(), self.server)

        # Loading credentials
        server_credentials = grpc.ssl_server_credentials(
            [
                [
                    _credentials.SERVER_CERTIFICATE_KEY,
                    _credentials.SERVER_CERTIFICATE,
                ]
            ],
        )

        # Pass down credentials
        port = self.server.add_secure_port(self.listen_addr, server_credentials)

    def run(self):
        self.server.start()
        self.server.wait_for_termination()

    def stop(self, grace: float = 1.0):
        self.server.stop(grace)
