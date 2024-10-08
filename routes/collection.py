from pymilvus import CollectionSchema, MilvusClient
from pymilvus.milvus_client import IndexParams
from server import server
from response import execute

@server.post("/v2/vectordb/collections/create")
def create_collection():
    """
    This operation creates a collection in a specified cluster.
    """

    payload = server.get_payload()

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
        _p = server.milvus.prepare_index_params()
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
        lambda: server.milvus.create_collection(
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

    payload = server.get_payload()

    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.describe_collection( collectionName )
    )

@server.post("/v2/vectordb/collections/drop")
def drop_collection():
    """
    This operation drops the current collection and all data within the collection.
    """

    payload = server.get_payload()

    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.drop_collection( collectionName )
    )

@server.post("/v2/vectordb/collections/get_load_state")
def get_collection_load_state():
    """
    This operation returns the load status of a specific collection.
    """

    payload = server.get_payload()

    collectionName = payload.get('collectionName')
    partitionNames = payload.get('partitionNames')

    return execute(
        lambda: server.milvus.get_load_state(
            collection_name=collectionName,
            partition_name=partitionNames
        )
    )

@server.post("/v2/vectordb/collections/get_stats")
def get_collection_stats():
    """
    This operation gets the number of entities in a collection.
    """

    payload = server.get_payload()
    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.get_collection_stats( collectionName )
    )

@server.post("/v2/vectordb/collections/has")
def has_collection():
    """
    This operation checks whether a collection exists.
    """

    payload = server.get_payload()
    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.has_collection( collectionName )
    )

@server.post("/v2/vectordb/collections/list")
def list_collections():
    """
    This operation lists all collections in the specified database.
    """

    return execute(
        lambda: server.milvus.list_collections()
    )

@server.post("/v2/vectordb/collections/load")
def load_collections():
    """
    This operation loads the data of the current collection into memory.
    """

    payload = server.get_payload()
    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.load_collection( collectionName )
    )

@server.post("/v2/vectordb/collections/release")
def release_collection():
    """
    This operation releases the data of the current collection from memory.
    """

    payload = server.get_payload()
    collectionName = payload.get('collectionName')

    return execute(
        lambda: server.milvus.release_collection( collectionName )
    )

# UNIMPLEMENTED
# 
# @server.post("/v2/vectordb/collections/rename")
# def rename_collection():
#     """
#     This operation renames an existing collection and optionally moves the collection to a new database.
#     """

#     payload = server.get_payload()
#     collectionName    = payload.get('collectionName')
#     newCollectionName = payload.get('newCollectionName')

#     return execute(
#         lambda: server.milvus.rename_collection( collectionName, newCollectionName, "" )
#     )

