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

    virtualenv booth_env
    source booth_env/bin/activate
    pip install Flask
    pip install pyzmq
    pip install pymongo
