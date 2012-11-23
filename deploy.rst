Setting up Deployment Server
----------------------------

To setup the server in EC2,

Installing updates

    sudo yum update

Setup the proper host name

    sudo hostname codingbooth.kitware.com
    sudo emacs /etc/sysconfig/network

Reboot the system

    sudo reboot

Installing some necessary utilities

    sudo yum install screen
    sudo chmod 777 var/run/screen/
    sudo yum install emacs-nox
    sudo yum install yum-utils

Installing nginx

    sudo useradd -s /usr/sbin/nologin -r nginx
    sudo yum install nginx
    sudo emacs /etc/nginx/conf.d/default.conf
    sudo systemctl enable nginx.service
    sudo systemctl status nginx.service

Edit the firewall to open port 80 via the tui and restart iptables

    sudo system-config-firewall-tui
    sudo systemctl restart iptables.service

Install mongo

    sudo yum install mongodb
    sudo yum install mongodb-server
    sudo emacs /etc/mongodb.conf
    sudo service mongod enable
    sudo service mongod start

Install general python tools

    sudo yum install python-pip
    sudo pip-python install virtualenv

Install C++ development tools (and libraries)

    sudo yum install cmake
    sudo yum install gcc-c++
    sudo yum install make
    sudo yum install python-devel
    sudo yum install zeromq-devel

Populate a python virtual environment

    virtualenv codingbooth_env
    source codingbooth_env/bin/activate
    pip install Flask
    pip install pyzmq
    pip install pymongo
    cd codingbooth_env
    git clone git://github.com/cpatrick/codingbooth.git
    cd codingbooth
    python setup.py develop

Now that the environment is basically setup. We will install uwsgi and
supervisor to daemonize uwsgi and beachserver (the server for compilation
in a sandbox). We use pip instead of yum because the version of uwsgi in pip
is more up-to-date, therefore more feature-rich.

    sudo pip-python install uwsgi
    sudo yum install supervisor

And enable supervisord:

    sudo systemctl enable supervisord.service

Once supervisor is setup, we need to setup jobs to start uwsgi and the server by
creating areas configs for the codingbooth uwsgi job and the beachserver. This
is done by adding the files in supervisor-configs to /etc/supervisord.d/.

    sudo cp /home/ec2-user/codingbooth_env/codingbooth/supervisor-configs/*.ini \
    /etc/supervisord.d/

Then start the supervisord:

    sudo systemctl start supervisord.service

With that, everything should be setup and ready to go.
