import pathlib
from ast import parse
import importlib

from ast import *
from copy import copy
from typing import Union

"""
Checks that there was an import of dataclass if there are any class definitions
"""


class RewriteImport(NodeTransformer):
    def visit_ImportFrom(self, node: ImportFrom) -> Union[ImportFrom, AST]:
        if node.module in ["pycardano", "typing"]:
            return node
        assert (
            len(node.names) == 1
        ), "The import must have the form 'from <pkg> import *'"
        assert (
            node.names[0].name == "*"
        ), "The import must have the form 'from <pkg> import *'"
        assert (
            node.names[0].asname == None
        ), "The import must have the form 'from <pkg> import *'"
        # TODO set anchor point according to own package
        module_file = pathlib.Path(importlib.import_module(node.module).__file__)
        assert (
            module_file.suffix == ".py"
        ), "The import must import a single python file."
        # visit the imported file again - make sure that recursive imports are resolved accordingly
        with module_file.open("r") as fp:
            module_content = fp.read()
        return self.visit(parse(module_content, filename=module_file.name))
