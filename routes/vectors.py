from pymilvus import AnnSearchRequest, Collection, WeightedRanker, RRFRanker
from server import server
from response import execute

RERANKERS = {
    "rrf": lambda k: RRFRanker( k ),
    "weighted": lambda weights: WeightedRanker(*weights)
}

@server.post("/v2/vectordb/entities/delete")
def delete_vector():
    """
    This operation deletes entities by their IDs or with a boolean expression.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    filter = payload.get("filter")
    ids = payload.get("ids")
    partitionName = payload.get("partitionName")

    return execute(
        lambda: server.milvus.delete(
            collection_name=collectionName,
            filter=filter,
            ids=ids,
            partition_name=partitionName
        )
    )

@server.post("/v2/vectordb/entities/get")
def get_vector():
    """
    This operation gets specific entities by their IDs.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    ids            = payload.get("ids")
    outputFields   = payload.get("outputFields")
    partitionName  = payload.get("partitionName")

    return execute(
        lambda: server.milvus.get(
            collection_name=collectionName,
            ids=ids,
            output_fields=outputFields,
            partition_names=partitionName
        )
    )

@server.post("/v2/vectordb/entities/hybrid_search")
def hybrid_search_vector():
    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    search         = payload.get("search")
    rerank: dict   = payload.get("rerank")
    limit          = payload.get("limit")
    outputFields   = payload.get("outputFields")
    
    collection = Collection(collectionName)
    collection.load()

    reqs: list[AnnSearchRequest] = []

    if search is not None:
        for (data, annsField, filter, groupingField, metricType, limit, offset, ignoreGrowing, params) in search:
            search_data = {}

            search_data["anns_field"] = annsField
            search_data["data"]       = data
            search_data["limit"] = limit
            search_data["param"] = {
                "metric_type": metricType,
                "params": params
            }
            
            # filter: "string",
            # groupingField: "string",
            # offset: "integer",
            # ignoreGrowing: "boolean",
            reqs.append( AnnSearchRequest(**search_data) )
        
    reranker: RRFRanker | WeightedRanker = None

    if rerank is not None:
        try:
            reranker = RERANKERS[rerank.get("strategy")](
                rerank.get("k") if rerank.get("k") else rerank.get("weights")
            )
        except Exception as e:
            print( e )


    return execute(
        lambda: collection.hybrid_search(
            reqs=reqs,
            rerank=reranker,
            limit=limit,
            output_fields=outputFields,
            kwargs={ "_async": False }
        )
    )

@server.post("/v2/vectordb/entities/insert")
def insert_vector():
    """
    This operation inserts data into a specific collection.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    data           = payload.get("data")

    return execute(
        lambda: server.milvus.insert(
            collection_name=collectionName,
            data=data
        )
    )

@server.post("/v2/vectordb/entities/query")
def query_vector():
    """
    This operation conducts a filtering on the scalar field with a specified boolean expression.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    ids            = payload.get("ids")
    limit          = payload.get("limit")
    filter         = payload.get("filter", "")
    outputFields   = payload.get("outputFields")
    partitionNames = payload.get("partitionNames")

    return execute(
        lambda: server.milvus.query(
            collection_name=collectionName,
            ids=ids,
            filter=filter,
            limit=limit,
            output_fields=outputFields,
            partition_names=partitionNames
        )
    )


@server.post("/v2/vectordb/entities/search")
def search_vector():
    """
    This operation conducts a vector similarity search with an optional scalar filtering expression.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    data           = payload.get("data")
    annsField      = payload.get("annsField")
    outputFields   = payload.get("outputFields")
    partitionNames = payload.get("partitionNames")
    searchParams   = payload.get("searchParams")
    limit          = payload.get("limit", 10)

    return execute(
        lambda: server.milvus.search(
            collection_name=collectionName,
            data=data,
            anns_field=annsField,
            output_fields=outputFields,
            partition_names=partitionNames,
            search_params=searchParams,
            limit=limit
        )
    )

@server.post("/v2/vectordb/entities/upsert")
def upsert_vector():
    """
    This operation inserts new records into the database or updates existing ones.
    """

    payload = server.get_payload()

    collectionName = payload.get("collectionName")
    data           = payload.get("data")
    partitionName  = payload.get("partitionNames")

    return execute(
        lambda: server.milvus.upsert(
            collection_name=collectionName,
            data=data,
            partition_name=partitionName,
        )
    )