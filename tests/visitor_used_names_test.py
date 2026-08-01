import ast
import pytest

from digdep.visitors import DependencyVisitor


@pytest.fixture
def visitor():
    return DependencyVisitor()


def used_imports(visitor, code: str):
    tree = ast.parse(code)
    visitor.visit(tree)
    return visitor.used_imports


def test_import_used_as_function_argument(visitor):
    code = """
import os

print(os)
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_attribute_access(visitor):
    code = """
import os

os.getcwd()
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_assignment(visitor):
    code = """
import os

x = os
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_return_statement(visitor):
    code = """
import os

def func():
    return os
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_list(visitor):
    code = """
import os

items = [os]
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_tuple(visitor):
    code = """
import os

items = (os,)
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_set(visitor):
    code = """
import os

items = {os}
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_dict_key(visitor):
    code = """
import os

items = {os: 1}
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_dict_value(visitor):
    code = """
import os

items = {"key": os}
"""
    assert used_imports(visitor, code) == {"os"}


def test_import_used_in_binary_expression(visitor):
    code = """
import x

a = x + 1
"""
    assert used_imports(visitor, code) == {"x"}


def test_import_used_in_comparison(visitor):
    code = """
import x

if x == 1:
    pass
"""
    assert used_imports(visitor, code) == {"x"}


def test_import_used_in_boolean_expression(visitor):
    code = """
import x

if x and True:
    pass
"""
    assert used_imports(visitor, code) == {"x"}


def test_import_used_in_unary_expression(visitor):
    code = """
import x

if not x:
    pass
"""
    assert used_imports(visitor, code) == {"x"}


def test_import_used_in_for_loop(visitor):
    code = """
import items

for i in items:
    pass
"""
    assert used_imports(visitor, code) == {"items"}


def test_import_used_in_while_loop(visitor):
    code = """
import running

while running:
    break
"""
    assert used_imports(visitor, code) == {"running"}


def test_import_used_in_with_statement(visitor):
    code = """
import lock

with lock:
    pass
"""
    assert used_imports(visitor, code) == {"lock"}


def test_import_used_in_lambda(visitor):
    code = """
import x

func = lambda: x
"""
    assert used_imports(visitor, code) == {"x"}


def test_import_used_in_comprehension(visitor):
    code = """
import values

result = [x for x in values]
"""
    assert used_imports(visitor, code) == {"values"}


def test_import_used_in_generator_expression(visitor):
    code = """
import values

result = (x for x in values)
"""
    assert used_imports(visitor, code) == {"values"}


def test_import_used_in_f_string(visitor):
    code = """
import name

s = f"{name}"
"""
    assert used_imports(visitor, code) == {"name"}


def test_import_used_with_alias(visitor):
    code = """
import numpy as np

np.array([1, 2, 3])
"""
    assert used_imports(visitor, code) == {"np"}


def test_from_import_used(visitor):
    code = """
from pathlib import Path

Path("a.txt")
"""
    assert used_imports(visitor, code) == {"Path"}


def test_from_import_used_with_alias(visitor):
    code = """
from pathlib import Path as P

P("a.txt")
"""
    assert used_imports(visitor, code) == {"P"}

def test_submodule_import_used(visitor):
    code = """
import xml.etree

xml.etree.parse("a.xml")
"""
    assert used_imports(visitor, code) == {"xml.etree"}


def test_deep_submodule_import_used(visitor):
    code = """
import xml.etree.ElementTree

xml.etree.ElementTree.parse("a.xml")
"""
    assert used_imports(visitor, code) == {"xml.etree.ElementTree"}


def test_submodule_import_used_directly(visitor):
    code = """
import xml.etree

xml.etree
"""
    assert used_imports(visitor, code) == {"xml.etree"}


def test_submodule_import_called(visitor):
    code = """
import xml.etree

xml.etree()
"""
    assert used_imports(visitor, code) == {"xml.etree"}


def test_submodule_import_with_deeper_attributes(visitor):
    code = """
import xml.etree

xml.etree.foo.bar.baz()
"""
    assert used_imports(visitor, code) == {"xml.etree"}
