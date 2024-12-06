import numpy as np
from pymilvus import MilvusException
from pymilvus.client.types import ExtraList
import pymilvus.client.types as types

def success_response( data ):
    return_data = None

    match type(data):
        case types.ExtraList:
            return_data = ExtraList(list(map(parse_extra_list, data)), extra=data.extra)
        case types.OmitZeroDict:
            return_data = parse_omit_zero_dict(data)
        case _: return_data = data

    return { "code": 0, "data": return_data }

def error_response( error_code: int, message: str ):
    return { "code": error_code, "message": message }

def parse_repeated_scalar_container( item ):
    elems = []
    for elem in item:
        elems.append(elem)
    return elems

def parse_omit_zero_dict( dict: types.OmitZeroDict ):
    data = {}
    for item in dict:
        if "RepeatedScalarContainer" in str(type(dict[item])):
            data[item] = parse_repeated_scalar_container( dict[item] )
        else:
            data[item] = dict[item]
    return data

def parse_extra_list( item ):
    if type(item) == dict:
        item = parse_dict_fields(item)

    return item

def parse_dict_fields( _dict: dict ):
    for key, value in _dict.items():
        if isinstance( value, list ) and isinstance(value[0], np.float32):
            _dict[key] = parse_embeddings( value )
    return _dict

def parse_embeddings( vec_array: list ):
    vec_array = list(map( lambda x: float(x) if isinstance(x, np.float32) else x, vec_array))
    return vec_array

def execute( x ):
    try:
        data = x()
        if not data or None == data:
            return success_response({})
        else:
            return success_response(data)
    except MilvusException as e:
        return error_response( e.code, e.message )