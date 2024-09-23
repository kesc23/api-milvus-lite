from pymilvus import MilvusException

def success_response( data ):
    return { "code": 0, "data": data }

def error_response( error_code: int, message: str ):
    return { "code": error_code, "message": message }

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