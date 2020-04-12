namespace java com.capillary.dimension_builder.thrift.exceptions
#@namespace scala com.capillary.scala.dimension_builder.thrift.exceptions
namespace php dimension_builder_exceptions

exception  WrongArgumentException {
    1: required string error;
}

exception  InvalidMetadataException {
    1: required string error;
}

exception  MetaApiRunTimeException {
    1: required string error;
}