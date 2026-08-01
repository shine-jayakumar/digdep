import pytest
import ast
from digdep.visitors import DependencyVisitor, ImportItem


@pytest.fixture
def visitor():
    return DependencyVisitor()


def imported_names(visitor, code: str):
    tree = ast.parse(code)
    visitor.visit(tree)
    return [
        item
        for items in visitor.imports.values()
        for item in items
    ]


def test_simple_import(visitor):
    code = """
import os
"""
    name = imported_names(visitor, code)[0]
    assert isinstance(name, ImportItem)
    assert name.imported == "os"
    assert name.module == "os"
    assert name.asname is None


def test_multiple_imports(visitor):
    code = """
import os, sys, re
"""
    names = imported_names(visitor, code)
    assert len(names) == 3
    for name, dst in zip(names, ("os", "sys", "re")):
        assert name.imported == dst
        assert name.module == dst
        assert name.asname is None
 

def test_import_with_alias(visitor):
    code = """
import numpy as np
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "numpy"
    assert name.module == "numpy"
    assert name.asname == "np"


def test_multiple_imports_with_aliases(visitor):
    code = """
import numpy as np, pandas as pd
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = (
        ("numpy", "numpy", "np"),
        ("pandas", "pandas", "pd"),
    )

    for name, (exp_name, exp_module, exp_asname) in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == exp_module
        assert name.asname == exp_asname


def test_import_submodule(visitor):
    code = """
import xml.etree
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "xml.etree"
    assert name.module == "xml.etree"
    assert name.asname is None


def test_import_deep_submodule(visitor):
    code = """
import xml.etree.ElementTree
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "xml.etree.ElementTree"
    assert name.module == "xml.etree.ElementTree"
    assert name.asname is None


def test_import_deep_submodule_with_alias(visitor):
    code = """
import xml.etree.ElementTree as ET
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "xml.etree.ElementTree"
    assert name.module == "xml.etree.ElementTree"
    assert name.asname == "ET"


def test_from_import(visitor):
    code = """
from pathlib import Path
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "Path"
    assert name.module == "pathlib"
    assert name.asname is None


def test_from_import_multiple_names(visitor):
    code = """
from pathlib import Path, PurePath
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = ("Path", "PurePath")

    for name, exp_name in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == "pathlib"
        assert name.asname is None


def test_from_import_with_alias(visitor):
    code = """
from pathlib import Path as P
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "Path"
    assert name.module == "pathlib"
    assert name.asname == "P"


def test_from_import_mixed_aliases(visitor):
    code = """
from numpy import array, random as rnd
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = (
        ("array", "numpy", None),
        ("random", "numpy", "rnd"),
    )

    for name, (exp_name, exp_module, exp_asname) in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == exp_module
        assert name.asname == exp_asname


def test_wildcard_import(visitor):
    code = """
from math import *
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "*"
    assert name.module == "math"
    assert name.asname is None


def test_relative_import(visitor):
    code = """
from . import utils
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "utils"
    assert name.module is None
    assert name.asname is None


def test_relative_import_from_package(visitor):
    code = """
from .utils import helper
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "helper"
    assert name.module == "utils"
    assert name.asname is None


def test_relative_import_parent(visitor):
    code = """
from ..utils import helper
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "helper"
    assert name.module == "utils"
    assert name.asname is None


def test_relative_import_parent_with_alias(visitor):
    code = """
from ..utils import helper as h
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "helper"
    assert name.module == "utils"
    assert name.asname == "h"


def test_multiline_import_parentheses(visitor):
    code = """
from pathlib import (
    Path,
    PurePath,
    PosixPath,
)
"""
    names = imported_names(visitor, code)
    assert len(names) == 3

    expected = ("Path", "PurePath", "PosixPath")

    for name, exp_name in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == "pathlib"
        assert name.asname is None


def test_multiline_import_backslash(visitor):
    code = """
from pathlib import Path, \\
                     PurePath
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = ("Path", "PurePath")

    for name, exp_name in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == "pathlib"
        assert name.asname is None


def test_conditional_import(visitor):
    code = """
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = ("TYPE_CHECKING", "Self")

    for name, exp_name in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == "typing"
        assert name.asname is None


def test_import_inside_function(visitor):
    code = """
def foo():
    import os
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "os"
    assert name.module == "os"
    assert name.asname is None


def test_import_inside_class(visitor):
    code = """
class Test:
    import os
"""
    name = imported_names(visitor, code)[0]
    assert name.imported == "os"
    assert name.module == "os"
    assert name.asname is None


def test_import_inside_try_except(visitor):
    code = """
try:
    import ujson as json
except ImportError:
    import json
"""
    names = imported_names(visitor, code)
    assert len(names) == 2

    expected = (
        ("ujson", "ujson", "json"),
        ("json", "json", None),
    )

    for name, (exp_name, exp_module, exp_asname) in zip(names, expected):
        assert name.imported == exp_name
        assert name.module == exp_module
        assert name.asname == exp_asname


def test_import_map_keys(visitor):
    code = """
import numpy as np
import pandas
from pathlib import Path
"""

    tree = ast.parse(code)
    visitor.visit(tree)

    assert set(visitor.imports) == {
        "np",
        "pandas",
        "Path",
    }

def test_import_map_multiple_items_same_bound_name(visitor):
    code = """
try:
    import ujson as json
except ImportError:
    import json
"""

    tree = ast.parse(code)
    visitor.visit(tree)

    assert list(visitor.imports) == ["json"]
    assert len(visitor.imports["json"]) == 2
