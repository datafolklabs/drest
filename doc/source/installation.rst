Installation
============

The following outlines installation of dRest.  It is recommended to work out 
of a `VirtualENV <http://pypi.python.org/pypi/virtualenv>`_ 
for development, which is reference throughout this documentation.  VirtualENV
is easily installed on most platforms either with 'easy_install' or 'pip' or
via your OS distributions packaging system (yum, apt, brew, etc).

Creating a Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    $ virtualenv --no-site-packages ~/env/drest/
    
    $ source ~/env/drest/bin/activate
    

When installing drest, ensure that your development environment is active
by sourcing the activate script (as seen above).


Installing Development Version From Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    (drest) $ git clone git://github.com/derks/drest.git
    
    (drest) $ cd drest/
    
    (drest) $ python setup.py install
    

To run tests, do the following from the 'root' directory:

.. code-block:: text
    
    (drest) $ pip install nose
    
    (drest) $ python setup.py nosetests


Installing Stable Versions From PyPi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    (drest) $ pip install drest
    
    
Running Unit Tests
^^^^^^^^^^^^^^^^^^

Unit tests should be run to ensure dRest is completely functional on your 
system:

.. code-block:: text

    (drest) $ ./utils/run-tests.sh
    

For Python 3 testing, you will need to run 'drest.mockapi' manually via a 
seperate virtualenv setup for Python 2.6+ (in a separate terminal), and then 
run the test suite with the option '--without-mockapi':

Terminal 1:

.. code-block:: text

    $ virtualenv-2.7 ~/env/drest-py27/
    
    $ source ~/env/drest-py27/bin/activate
    
    (drest-py27) $ ./utils/run-mockapi.sh
    

Terminal 2:

.. code-block:: text

    $ virtualenv-3.2 ~/env/drest-py32/
    
    $ source ~/env/drest-py32/bin/activate
    
    (drest-py32) $ ./utils/run-tests.sh --without-mockapi
