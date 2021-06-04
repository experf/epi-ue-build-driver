import logging

import grpc

from . import api_pb2
from . import api_pb2_grpc


def status():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('127.0.0.1:5000') as channel:
        stub = api_pb2_grpc.APIStub(channel)
        response = stub.Status(api_pb2.StatusRequest())
    print(f"Driver is: {response.code} {response.message}")


if __name__ == '__main__':
    logging.basicConfig()
    status()
