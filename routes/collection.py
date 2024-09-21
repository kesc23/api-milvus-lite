from pymilvus import CollectionSchema, MilvusClient
from pymilvus.milvus_client import IndexParams
from operator import itemgetter
from flask import request
from server import server, client as milvus
from response import execute

def get_payload() -> dict: return request.json

@server.post("/v2/vectordb/collections/create")
def create_collection():
    """
    This operation creates a collection in a specified cluster.
    """

    payload = get_payload()

    collectionName: str   = payload.get('collectionName')
    dimension             = payload.get('dimension')
    metricType: str       = payload.get('metricType', "COSINE")
    idType: str           = payload.get('idType', "int")
    autoID: bool          = payload.get('autoID', False)
    primaryFieldName: str = payload.get('primaryFieldName', "id")
    vectorFieldName       = payload.get('vectorFieldName', 'vector')
    schema: CollectionSchema | dict       = payload.get('schema')
    indexParams: IndexParams | list[dict] = payload.get('indexParams')
    params: dict          = payload.get('params', {})

    if indexParams is not None:
        _p = milvus.prepare_index_params()
        for param in indexParams:
            _p.add_index(field_name=param["fieldName"], metric_type=param["metricType"], kwargs=param["params"])
        indexParams = _p
    
    if schema is not None:
        _s = MilvusClient.create_schema(
            auto_id=schema.get("autoId", False),
            enable_dynamic_field=schema.get("enabledDynamicField", False)
        )

        for field in schema.get("fields", []):
            o = {}
            if "isPrimary" in field: o["isPrimary"] = field["isPrimary"]
            if "elementTypeParams" in field and "dim" in field["elementTypeParams"]: o["dim"] = field["elementTypeParams"]["dim"]
            _s.add_field(field_name=field["fieldName"], datatype=field["dataType"], kwargs=o )

        schema = _s

    return execute(
        lambda: milvus.create_collection(
            collection_name=collectionName,
            dimension=dimension,
            primary_field_name=primaryFieldName,
            id_type=idType,
            vector_field_name=vectorFieldName,
            metric_type=metricType,
            auto_id=autoID,
            schema=schema,
            index_params=indexParams,
            kwargs=params
        )
    )

@server.post("/v2/vectordb/collections/describe")
def describe_collection():
    """
    Describes the details of a collection.
    """

    payload = get_payload()

    collectionName = payload.get('collectionName')

    return execute(
        lambda: milvus.describe_collection( collectionName )
    )
