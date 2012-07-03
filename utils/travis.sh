#!/bin/bash

./utils/travis-bootstrap.sh
sleep 5
./utils/run-tests.sh --without-mockapi