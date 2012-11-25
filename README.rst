Coding Booth
------------

The goal of this is a simple web interface for delivering coding tutorials.

This is a simple Flask app that using ZeroMQ and Mongo.

To install the app, install the dependencies (preferably in a virtual 
environment) like so:

    pip install -r requirements.txt

To run the app, run the beachserver

    python beachserver.py

Then run the flask server (or deploy it).

    python runserver.py

Then navigate the browser to localhost:5000 to verify the installation. See
deploy.rst for documentation on setting up a production instance.
