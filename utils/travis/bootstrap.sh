#!/bin/bash

# install this to the default virtualenv - it fails on python3 which is why
# we put it here rather than in .travis.yml
pip install simplejson --use-mirrors

source /home/vagrant/virtualenv/python2.7/bin/activate
pip install -r src/drest.mockapi/requirements.txt --use-mirrors
python src/drest.mockapi/mockapi/manage.py testserver DREST_MOCKAPI_PROCESS &