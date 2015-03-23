Changelog
=========

v0.6.2
-------------------------------------------
* Change the log to Standard output only by default, the user can add more handlers by self


v0.6.0
-------------------------------------------
* add has(=>) and hasnt(!>) operator, to check if a set has or hasnt an item.


v0.5.1
-------------------------------------------
* add __auto_func_detection__ local variable to disable the function detection
* add function to disable auto function detection globally
* add function for user to start a function logging explicitly.


v0.4.0
-------------------------------------------
* add lesson 5 example for checks batch argument
* fix issue #12: multiple options for checks error


v0.3.0
-------------------------------------------
* add passdesc (-p) and faildesc (-f) option for step/check function
* add check/checks as alias for step/steps
* add the return values for step and steps function
* add a batch parameter to steps/checks function


v0.2.0
-------------------------------------------
* added debug info logging
* added -e and -w option for exception and warning
* add a mechanism for new option insertion
* enhanced the ok function


v0.1
-------------------------------------------

This is a fairly complete list of v0.1, which can
serve as a reference for test engineers.

* automatically log test cases and steps
* implemented general operators and corresponding functions, including::
    eq, ne, gt, lt, ge, le, match, unmatch
* implemented the framework for adding new operators and functions
* implemented step/steps/s functions, which can be used in some test frameworks
