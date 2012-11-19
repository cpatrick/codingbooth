from pymongo import Connection
from bson.objectid import ObjectId

connection = Connection()
database = connection.codingbooth
collection = database.codes


def set_code(object_id=None, code=""):
    """Store the code block into the database."""
    if id:
        db_id = collection.insert({'code': code})
    else:
        db_id = collection.update({'_id': ObjectId(object_id)}, {'code': code})
    return str(db_id)


def get_code(object_id):
    """Retrieve the code from the database."""
    result = collection.find_one({'_id': ObjectId(object_id)})
    return result['code']


def set_compile_results(object_id, results):
    """Put the compilation results into the database."""
    db_id = collection.update({'_id': ObjectId(object_id)},
        {'compilation': results})
    return db_id


def set_run_results(object_id, results):
    """Put the results of running the compiled executable into the database."""
    db_id = collection.update({'_id': ObjectId(object_id)},
        {'run': results})
    return db_id
