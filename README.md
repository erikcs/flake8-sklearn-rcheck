Flake8 plugin for scikit-learn test files: (attempt to) check that estimators set the `random_state` parameter

## Installation

The plugin works with Flake8 out of the box

`$ pip install git+https://github.com/nuffe/flake8-sklearn-rcheck.git`

(uninstall the package to remove the plugin)


## Example

In the `sklearn` base directory, append an offending line to a test file, and send the diff to flake8:

```
$ printf "\n\nnono = make_classification(1)\n" >> sklearn/tests/test_learning_curve.py
$ git diff --unified=0 | flake8 --diff --show-source "$*"
  sklearn/tests/test_learning_curve.py:289:8: S100 missing random_state argument
  nono = make_classification(1)
         ^
```
