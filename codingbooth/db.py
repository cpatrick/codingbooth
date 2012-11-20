from pymongo import Connection
from bson.objectid import ObjectId


def set_code(object_id=None, code=""):
    """Store the code block into the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    if object_id:
        collection.update({'_id': ObjectId(object_id)}, {'code': code})
        db_id = object_id
    else:
        db_id = collection.insert({'code': code})
    connection.close()
    return str(db_id)


def get_code(object_id):
    """Retrieve the code from the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    result = collection.find_one({'_id': ObjectId(object_id)})
    connection.close()
    return result['code']


def get_code_from_name(name):
    """Retrieve code from the database given a name."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    result = collection.find_one({'name': name})
    connection.close()
    return result


def set_compile_results(object_id, results):
    """Put the compilation results into the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    db_id = collection.update({'_id': ObjectId(object_id)},
        {'$set': {'compilation': results}})
    connection.close()
    return db_id


def set_run_results(object_id, results):
    """Put the results of running the compiled executable into the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    db_id = collection.update({'_id': ObjectId(object_id)},
        {'$set': {'run': results}})
    connection.close()
    return db_id
