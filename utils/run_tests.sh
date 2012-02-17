#!/bin/bash

SOURCES="src/drest/"
pip install nose coverage

for path in $SOURCES; do
    pushd $path
        python setup.py develop
    popd
done

if [ "$1" == "--without-mockapi" ]; then
    echo "Not running drest.mockapi..."
else
    echo "Starting drest.mockapi..."
    python src/drest.mockapi/mockapi/manage.py testserver DREST_MOCKAPI_PROCESS 2>/dev/null 1>/dev/null &
fi

coverage erase
rm -rf coverage_html_report/
coverage run `which nosetests` --verbosity=3 $SOURCES


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