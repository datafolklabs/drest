
ChangeLog
==============================================================================

All bugs/feature details can be found at: 

   https://github.com/derks/drest/issues/XXXXX


Where XXXXX is the 'Issue #' referenced below.  Additionally, this change log
is available online at:

    http://drest.readthedocs.org/en/latest/changelog.html

.. raw:: html

    <BR><BR>

0.9.4 - Feb 16, 2012
------------------------------------------------------------------------------

Bug Fixes:

    - :issue:`3` - TypeError: object.__init__() takes no parameters
 
Feature Enhancements:

    - Improved test suite, now powered by Django TastyPie!
    
Incompatible Changes:

    - drest.api.API.auth() no longer performs anything by default, but rather
      raises a NotImplementedError.
    
    
.. raw:: html

    <BR><BR>
    
0.9.2 - Feb 01, 2012
------------------------------------------------------------------------------

    - Initial Beta release.  Future versions will detail bugs/features/etc.