#!/bin/bash

SOURCES="src/drest/"

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not running in a virtualenv???  You've got 10 seconds to CTRL-C ..."
    sleep 10
    virtualenv .env/
    source .env/bin/activate
fi

pip install nose coverage

for path in $SOURCES; do
    pushd $path
        pip install -r requirements.txt
        python setup.py develop --no-deps
    popd
done

if [ "$1" == "--without-mockapi" ]; then
    echo "Not running drest.mockapi..."
else
    echo "Starting drest.mockapi..."
    pushd src/drest.mockapi
        pip install -r requirements.txt
        python setup.py develop --no-deps
        python mockapi/manage.py testserver DREST_MOCKAPI_PROCESS 2>/dev/null 1>/dev/null &
        sleep 10
    popd
    
fi

coverage erase
rm -rf coverage_html_report/
coverage run `which nosetests` --verbosity=3 $SOURCES
RET=$?

# This is a hack to wait for tests to run
sleep 5

if [ "$1" == "--without-mockapi" ]; then
    echo "Not killing drest.mockapi (I didn't start it) ..."
else
    echo "Killing drest.mockapi..."
    # Then kill the mock api
    /bin/ps auxw \
    | /usr/bin/grep 'DREST_MOCKAPI_PROCESS' \
    | /usr/bin/awk {' print $2 '} \
    | /usr/bin/xargs kill 2>/dev/null 1>/dev/null
fi

echo; echo
coverage combine
coverage html

coverage report
exit $RET