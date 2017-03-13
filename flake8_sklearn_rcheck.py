import ast
import imp
import inspect
import logging

logger = logging.getLogger('flake8_sklearn_rcheck')
logging.basicConfig(level=logging.ERROR)

class RandomStateCheck(object):
    name = 'sklearn-rcheck'
    version = '0.1'
    off_by_default = False

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        if self.filename.find('test_') == -1:
            return

        takes_random_state = {}

        # Load the test source file as a module to be able to get the
        # signature of all imported callables
        try:
            module = imp.load_source('', self.filename)
        except ImportError as e:
            logger.error(("Could not load the file {} as a module. This Flake8"
            " plugin needs to be able to load the scikit-learn test file it is"
            " linting as a module in order to get function/class signatures."
            " Reasons for this error could be: missing packages, or a syntax"
            " error in the test file. This plugin should ideally be run in a"
            " virtual environment with the built and installed scikit-learn"
            " version it is linting, together with its neceassy dependencies."
            ).format(self.filename))

            raise e

        module_callables = inspect.getmembers(module, lambda x:
                                    inspect.isfunction(x) or inspect.isclass(x))

        for name, obj in module_callables:
            try:
                if 'random_state' in inspect.signature(obj).parameters:
                    takes_random_state[name] = True
            except:
                pass

        if not takes_random_state:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id'): # Keep it simple and stop traversing here
                    name = node.func.id
                    if name in takes_random_state:
                        kwdnames = []
                        for kwd in node.keywords:
                            kwdnames.append(kwd.arg)
                        if 'random_state' not in kwdnames:
                            yield (node.lineno,
                                   node.col_offset,
                                  'S100 missing random_state argument',
                                  'RandomStateCheck')
