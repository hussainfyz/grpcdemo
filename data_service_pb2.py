# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: data_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'data_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x64\x61ta_service.proto\x12\x0b\x64\x61taservice\"\"\n\x0b\x44\x61taRequest\x12\x13\n\x0bnum_records\x18\x01 \x01(\x05\"G\n\nDataRecord\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x02\x12\x10\n\x08\x63\x61tegory\x18\x04 \x01(\t2R\n\x0b\x44\x61taService\x12\x43\n\x0cGetLargeData\x12\x18.dataservice.DataRequest\x1a\x17.dataservice.DataRecord0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATAREQUEST']._serialized_start=35
  _globals['_DATAREQUEST']._serialized_end=69
  _globals['_DATARECORD']._serialized_start=71
  _globals['_DATARECORD']._serialized_end=142
  _globals['_DATASERVICE']._serialized_start=144
  _globals['_DATASERVICE']._serialized_end=226
# @@protoc_insertion_point(module_scope)
