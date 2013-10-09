#!/bin/bash

bash ./utils/travis-bootstrap.sh
sleep 10
bash ./utils/run-tests.sh --without-mockapi
RET="$?"

if [ "$RET" != "0" ]; then
    echo '----------------------------------------------------------------------'
    echo 'MOCKAPI STDOUT'
    echo '----------------------------------------------------------------------'
    cat ./mockapi.out
    echo
    echo '----------------------------------------------------------------------'
    echo 'MOCKAPI STDERR'
    echo '----------------------------------------------------------------------'
    cat ./mockapi.err
    echo
    exit 1
else
    exit 0
fi