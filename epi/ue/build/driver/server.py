import logging
import asyncio
import grpc
from concurrent import futures
import selectors
import subprocess
import sys
import threading
from queue import Queue

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


class ProcessCommunicator():
    def enqueue_output(self):
        if not self.popen.stdout or self.popen.stdout.closed:
            return
        out = self.popen.stdout
        for line in iter(out.readline, b''):
            self.queue.put(("out", line))

    def enqueue_err(self):
        if not self.popen.stderr or self.popen.stderr.closed:
            return
        err = self.popen.stderr
        for line in iter(err.readline, b''):
            self.queue.put(("err", line))

    def enqueue_code(self):
        self.out_thread.join()
        self.err_thread.join()
        self.queue.put(("code", self.popen.returncode))

    def __init__(self, popen):
        self.popen = popen
        self.running = True
        self.queue = Queue()

        self.out_thread = threading.Thread(
            name="out_read",
            target=self.enqueue_output,
            args=()
        )
        self.out_thread.daemon = True  # thread dies with the program
        self.out_thread.start()

        self.err_thread = threading.Thread(
            name="err_read",
            target=self.enqueue_err,
            args=()
        )
        self.err_thread.daemon = True  # thread dies with the program
        self.err_thread.start()

        self.code_thread = threading.Thread(
            name="code",
            target=self.enqueue_code,
            args=()
        )
        self.code_thread.daemon = True
        self.code_thread.start()

class API(api_pb2_grpc.APIServicer):
    def Status(self, request, context):
        return api_pb2.StatusResponse(code=200, message="OK")

    def Stream(self, request, context):
        p = subprocess.Popen(
            [request.cmd, *request.args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

        pc = ProcessCommunicator(p)

        while True:
            stream, content = pc.queue.get()
            if stream == "out":
                yield api_pb2.StreamResponse(out=content)
            elif stream == "err":
                yield api_pb2.StreamResponse(err=content)
            elif stream == "code":
                yield api_pb2.StreamResponse(code=content)
                break
            else:
                raise Exception(f"Bad stream name: {repr(stream)}")

        yield api_pb2.StreamResponse(code=p.returncode)


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
