from optparse import OptionParser
from pymongo import Connection
from bson.objectid import ObjectId
from bson.binary import Binary


def main():
    # Setup CLI
    parser = OptionParser()
    parser.add_option('-i', '--input', help="Get input from this file.")
    parser.add_option('-a', '--input2', help="Get input from this file.")
    parser.add_option('-c', '--cmake', help="Get cmake from this file.")

    # Parse CLI
    (options, args) = parser.parse_args()
    options = vars(options)
    name = args[0]
    code_name = args[1]

    print options

    connection = Connection()
    database = connection.codingbooth
    collection = database.codes

    cur_object = collection.find_one({'name': name})

    if cur_object:
        object_id = cur_object['_id']
        print "get document"
    else:
        print "create document"
        object_id = collection.insert({'name': name})

    with open(code_name, 'r') as infile:
        print "insert code"
        code = infile.read()
        collection.update({'_id': ObjectId(object_id)},
            {'$set': {'code': code}})

    cmake = options['cmake']
    if cmake:
        print "insert cmake"
        with open(cmake, 'r') as infile:
            blob = infile.read()
            collection.update({'_id': ObjectId(object_id)},
                {'$set': {'cmake': blob}})

    input_image = options['input']
    print input_image
    if input_image:
        print "insert input"
        with open(input_image, 'r') as infile:
            blob = infile.read()
            collection.update({'_id': ObjectId(object_id)},
                {'$set':
                {'inputs': [{'name': input_image, 'contents':Binary(blob)}]}})

    run_parameters = raw_input('Enter the run parameters: ')
    collection.update({'_id': ObjectId(object_id)},
        {'$set': {'run_parameters': run_parameters}})

    print "complete"

if __name__ == '__main__':
    main()
