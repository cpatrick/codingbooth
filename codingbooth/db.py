from pymongo import Connection
from bson.objectid import ObjectId
from bson.binary import Binary


def set_code(object_id=None, code=""):
    """Store the code block into the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    if object_id:
        collection.update({'_id': ObjectId(object_id)},
            {'$set': {'code': code}})
        db_id = object_id
    else:
        db_id = collection.insert({'code': code})
    connection.close()
    return str(db_id)


def set_output(object_id, file_path):
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes

    with open(file_path, 'r') as infile:
        blob = infile.read()
        collection.update({'_id': ObjectId(object_id)},
            {'$set': {'outputs': [{'name': 'output.png', 'content':Binary(blob)}]}})
    return object_id


def get_code(object_id):
    """Retrieve the code from the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    result = collection.find_one({'_id': ObjectId(object_id)})
    connection.close()
    return result['code']


def get_full_code(object_id):
    """get the full code document from the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.codes
    result = collection.find_one({'_id': ObjectId(object_id)})
    connection.close()
    return result


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


def create_user(email, password):
    """Create a user in the database with a given name, email, and password."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.users
    db_id = collection.insert({
        'email': email,
        'password': password})
    connection.close()
    return db_id


def save_user(object_id, email, password):
    """Save the user to the database."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.users
    collection.update({'_id': ObjectId(object_id)},
        {'$set': {
        'email': email,
        'password': password}})
    connection.close()


def load_user(object_id):
    """Load the user based on the given id."""
    connection = Connection()
    database = connection.codingbooth
    collection = database.users
    result = collection.find_one({'_id': ObjectId(object_id)})
    connection.close()
    return result


def load_user_by_email(email):
    """Load the user based on the given email"""
    connection = Connection()
    database = connection.codingbooth
    collection = database.users
    result = collection.find_one({'email': email})
    connection.close()
    return result
