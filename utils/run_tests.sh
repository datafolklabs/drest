#!/bin/bash

SOURCES="src/drest/"

pip install nose coverage

for path in $SOURCES; do
    pushd $path
        python setup.py develop
    popd
done

python utils/drest_test_api.py 2>/dev/null 1>/dev/null &
coverage erase
coverage run `which nosetests` --verbosity=3 $SOURCES


# This is a hack to wait for tests to run
sleep 5
/bin/ps auxw \
| /usr/bin/grep '[p]ython utils/drest_test_api.py' \
| /usr/bin/awk {' print $2 '} \
| /usr/bin/xargs kill 2>/dev/null 1>/dev/null

echo; echo
coverage combine
coverage html

coverage report