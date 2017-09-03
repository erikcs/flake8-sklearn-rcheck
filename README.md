Flake8 plugin for scikit-learn test files: (attempt to) check that estimators set the `random_state` parameter

## Installation

The plugin works with Flake8 out of the box

`$ pip install git+https://github.com/erikcs/flake8-sklearn-rcheck.git`

(uninstall the package to remove the plugin)

This plugin needs to be able to import the test file it is linting as a module. So ideally
this plugin is installed in a virtual environment with the scikit-learn build it is supposed to lint.

## Example

In the `scikit-learn` base directory, append an offending line to a test file, and send the diff to flake8:

```
$ printf "\n\nnono = make_classification(1)\n" >> sklearn/tests/test_learning_curve.py
$ git diff --unified=0 | flake8 --diff --show-source "$*"
  sklearn/tests/test_learning_curve.py:289:8: S100 missing random_state argument
  nono = make_classification(1)
         ^
```

## Misc

Tested with latest Anaconda + Python 3

As with most problems in static analysis, this tool cannot uncover absolutely all cases


## Issues

* Weird issue with error not reported by Flake8 when other builtin errors are present nearby (for example
  an indent error on the line above a call missing `random_state`). This is not a big issue since the check should not pass anyways, and the `random_state` error will be reported when the "native" nearby error has been fixed.
