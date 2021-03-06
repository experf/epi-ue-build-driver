# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import api_pb2 as api__pb2


class APIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Status = channel.unary_unary(
                '/API/Status',
                request_serializer=api__pb2.StatusRequest.SerializeToString,
                response_deserializer=api__pb2.StatusResponse.FromString,
                )
        self.Stream = channel.unary_stream(
                '/API/Stream',
                request_serializer=api__pb2.CmdRequest.SerializeToString,
                response_deserializer=api__pb2.CmdResponse.FromString,
                )
        self.Plastic_CloneRepo = channel.unary_stream(
                '/API/Plastic_CloneRepo',
                request_serializer=api__pb2.Plastic_CloneRepoRequest.SerializeToString,
                response_deserializer=api__pb2.CmdResponse.FromString,
                )
        self.UE4CLI_SetRoot = channel.unary_stream(
                '/API/UE4CLI_SetRoot',
                request_serializer=api__pb2.UE4CLI_SetRootRequest.SerializeToString,
                response_deserializer=api__pb2.CmdResponse.FromString,
                )
        self.UE4CLI_Package = channel.unary_stream(
                '/API/UE4CLI_Package',
                request_serializer=api__pb2.UE4CLI_PackageRequest.SerializeToString,
                response_deserializer=api__pb2.CmdResponse.FromString,
                )
        self.Upload = channel.unary_unary(
                '/API/Upload',
                request_serializer=api__pb2.UploadRequest.SerializeToString,
                response_deserializer=api__pb2.StatusResponse.FromString,
                )


class APIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Plastic_CloneRepo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UE4CLI_SetRoot(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UE4CLI_Package(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Upload(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Status': grpc.unary_unary_rpc_method_handler(
                    servicer.Status,
                    request_deserializer=api__pb2.StatusRequest.FromString,
                    response_serializer=api__pb2.StatusResponse.SerializeToString,
            ),
            'Stream': grpc.unary_stream_rpc_method_handler(
                    servicer.Stream,
                    request_deserializer=api__pb2.CmdRequest.FromString,
                    response_serializer=api__pb2.CmdResponse.SerializeToString,
            ),
            'Plastic_CloneRepo': grpc.unary_stream_rpc_method_handler(
                    servicer.Plastic_CloneRepo,
                    request_deserializer=api__pb2.Plastic_CloneRepoRequest.FromString,
                    response_serializer=api__pb2.CmdResponse.SerializeToString,
            ),
            'UE4CLI_SetRoot': grpc.unary_stream_rpc_method_handler(
                    servicer.UE4CLI_SetRoot,
                    request_deserializer=api__pb2.UE4CLI_SetRootRequest.FromString,
                    response_serializer=api__pb2.CmdResponse.SerializeToString,
            ),
            'UE4CLI_Package': grpc.unary_stream_rpc_method_handler(
                    servicer.UE4CLI_Package,
                    request_deserializer=api__pb2.UE4CLI_PackageRequest.FromString,
                    response_serializer=api__pb2.CmdResponse.SerializeToString,
            ),
            'Upload': grpc.unary_unary_rpc_method_handler(
                    servicer.Upload,
                    request_deserializer=api__pb2.UploadRequest.FromString,
                    response_serializer=api__pb2.StatusResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'API', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class API(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/API/Status',
            api__pb2.StatusRequest.SerializeToString,
            api__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/API/Stream',
            api__pb2.CmdRequest.SerializeToString,
            api__pb2.CmdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Plastic_CloneRepo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/API/Plastic_CloneRepo',
            api__pb2.Plastic_CloneRepoRequest.SerializeToString,
            api__pb2.CmdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UE4CLI_SetRoot(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/API/UE4CLI_SetRoot',
            api__pb2.UE4CLI_SetRootRequest.SerializeToString,
            api__pb2.CmdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UE4CLI_Package(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/API/UE4CLI_Package',
            api__pb2.UE4CLI_PackageRequest.SerializeToString,
            api__pb2.CmdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Upload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/API/Upload',
            api__pb2.UploadRequest.SerializeToString,
            api__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
