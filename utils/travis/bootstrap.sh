#!/bin/bash

source /home/vagrant/virtualenv/python2.7/bin/activate
pip install -r src/drest.mockapi/requirements.txt --use-mirrors
python src/drest.mockapi/mockapi/manage.py testserver DREST_MOCKAPI_PROCESS &