#!/bin/bash

./utils/travis-bootstrap.sh
sleep 15
./utils/run-tests.sh --without-mockapi
