#!/bin/bash

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not running in a virtualenv???  You've got 10 seconds to CTRL-C ..."
    sleep 10
    virtualenv .env/
    source .env/bin/activate
fi

pip install nose coverage
pip install -r requirements.txt
python setup.py develop --no-deps

if [ "$1" == "--without-mockapi" ]; then
    echo "Not running drest.mockapi..."
else
    ./utils/run-mockapi.sh DREST_MOCKAPI_PROCESS 2>/dev/null 1>/dev/null &
    sleep 5
fi

rm -rf coverage_report/
coverage erase
python setup.py nosetests
RET=$?

# This is a hack to wait for tests to run
sleep 5

if [ "$1" == "--without-mockapi" ]; then
    echo "Not killing drest.mockapi (I didn't start it) ..."
else
    echo "Killing drest.mockapi..."
    # Then kill the mock api
    ps auxw \
    | grep 'DREST_MOCKAPI_PROCESS' \
    | awk {' print $2 '} \
    | xargs kill 2>/dev/null 1>/dev/null
fi

echo
if [ "$RET" == "0" ]; then
    echo "TESTS PASSED OK"
else
    echo "TESTS FAILED"
fi
echo

exit $RET
