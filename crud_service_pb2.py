# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: crud_service.proto
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
    'crud_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63rud_service.proto\"$\n\x06Record\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"\x12\n\x03Key\x12\x0b\n\x03key\x18\x01 \x01(\t\"0\n\x08Response\x12\x13\n\x0bstatus_code\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x07\n\x05\x45mpty\",\n\x10SnapshotResponse\x12\x18\n\x07records\x18\x01 \x03(\x0b\x32\x07.Record2\xd1\x01\n\x0c\x43loudStorage\x12\x1e\n\x06\x43reate\x12\x07.Record\x1a\t.Response\"\x00\x12\x19\n\x04Read\x12\x04.Key\x1a\t.Response\"\x00\x12\x1e\n\x06Update\x12\x07.Record\x1a\t.Response\"\x00\x12\x1b\n\x06\x44\x65lete\x12\x04.Key\x1a\t.Response\"\x00\x12 \n\tHeartbeat\x12\x06.Empty\x1a\t.Response\"\x00\x12\'\n\x08Snapshot\x12\x06.Empty\x1a\x11.SnapshotResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'crud_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RECORD']._serialized_start=22
  _globals['_RECORD']._serialized_end=58
  _globals['_KEY']._serialized_start=60
  _globals['_KEY']._serialized_end=78
  _globals['_RESPONSE']._serialized_start=80
  _globals['_RESPONSE']._serialized_end=128
  _globals['_EMPTY']._serialized_start=130
  _globals['_EMPTY']._serialized_end=137
  _globals['_SNAPSHOTRESPONSE']._serialized_start=139
  _globals['_SNAPSHOTRESPONSE']._serialized_end=183
  _globals['_CLOUDSTORAGE']._serialized_start=186
  _globals['_CLOUDSTORAGE']._serialized_end=395
# @@protoc_insertion_point(module_scope)
