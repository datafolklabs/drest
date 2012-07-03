#!/bin/bash

bash ./utils/travis-bootstrap.sh
sleep 10
bash ./utils/run-tests.sh --without-mockapi
