from pymilvus import AnnSearchRequest, Collection, WeightedRanker, RRFRanker
from server import server
from response import execute

RERANKERS = {
    "rrf": lambda k: RRFRanker( k ),
    "weighted": lambda weights: WeightedRanker(*weights)
}

