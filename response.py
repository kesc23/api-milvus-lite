from pymilvus import MilvusException

def success_response( data ):
    return { "code": 0, "data": data }

def error_response( error_code: int, message: str ):
    return { "code": error_code, "message": message }

def execute( x ):
    try:
        data = x()
        if not data or None == data:
            return success_response({})
        else:
            return success_response(data)
    except MilvusException as e:
        return error_response( e.code, e.message )