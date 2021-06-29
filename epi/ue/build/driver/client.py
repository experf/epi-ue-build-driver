import logging
import contextlib
import argparse

import grpc

from . import api_pb2
from . import api_pb2_grpc

from . import _credentials


class AuthGateway(grpc.AuthMetadataPlugin):
    def __call__(self, context, callback):
        """Implements authentication by passing metadata to a callback.
        Implementations of this method must not block.
        Args:
          context: An AuthMetadataContext providing information on the RPC that
            the plugin is being called to authenticate.
          callback: An AuthMetadataPluginCallback to be invoked either
            synchronously or asynchronously.
        """
        # Example AuthMetadataContext object:
        # AuthMetadataContext(
        #     service_url=u'https://localhost:50051/helloworld.Greeter',
        #     method_name=u'SayHello')
        callback(
            ((_credentials.PASSWORD_HEADER_KEY, _credentials.PASSWORD),), None
        )


@contextlib.contextmanager
def create_client_channel(addr):
    # Call credential object will be invoked for every single RPC
    call_credentials = grpc.metadata_call_credentials(
        AuthGateway(), name="auth gateway"
    )
    # Channel credential will be valid for the entire channel
    channel_credential = grpc.ssl_channel_credentials(
        _credentials.SERVER_CERTIFICATE
    )
    # # Combining channel credentials and call credentials together
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    channel = grpc.secure_channel(addr, composite_credentials)
    # channel = grpc.secure_channel(addr, channel_credential)
    # channel = grpc.insecure_channel(addr)
    yield channel


def status():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with create_client_channel("127.0.0.1:5000") as channel:
        stub = api_pb2_grpc.APIStub(channel)
        response = stub.Status(api_pb2.StatusRequest())
    print(f"Driver is: {response.code} {response.message}")


def stream(args):
    with create_client_channel("127.0.0.1:5000") as channel:
        stub = api_pb2_grpc.APIStub(channel)
        for response in stub.Stream(
            api_pb2.CmdRequest(cmd=args[0], args=args[1:])
        ):
            if response.type is api_pb2.CmdResponse.Type.OUT:
                print(f"OUT> {response.text}", end='')
            elif response.type is api_pb2.CmdResponse.Type.ERR:
                print(f"ERR> {response.text}", end='')
            elif response.type is api_pb2.CmdResponse.Type.CODE:
                print(f"CODE {response.code}")
            else:
                print(f"??? RESPONSE {response}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Client for EPI Unreal Engine Build Driver"
    )
    parser.add_argument(
        "method",
        help="What to call",
    )
    parser.add_argument(
        "args",
        help="Args to pass, if applicable",
        nargs="*",
    )

    return parser.parse_args()


def main():
    logging.basicConfig()
    args = parse_args()
    if args.method == "status":
        status()
    elif args.method == "stream":
        stream(args.args)
    else:
        raise Exception(f"WTF is this?! {args.method}")


if __name__ == "__main__":
    main()
