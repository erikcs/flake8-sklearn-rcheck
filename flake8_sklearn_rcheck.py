import ast
import imp
import inspect

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

        # Load the test source file as a module to be able to introspect and
        # get the signature of all imported callables
        module = imp.load_source('_', self.filename)
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
