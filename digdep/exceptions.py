"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Exceptions
"""

class DigDepException(Exception):
    pass

class JSONOutputError(DigDepException):
    """Raise when JSON output fails"""
    pass

class DependencyTypeError(DigDepException):
    """Raise when invalid dependency type is received"""
    pass

class OutputTypeError(DigDepException):
    """Raise when an invalid output type is received"""
    pass

class CLICommandError(DigDepException):
    """Raise when an invalid command is received"""
    pass

class CommandNotMappedError(DigDepException):
    """Raise when a command is not mapped to an analyzer function"""
    pass

class InvalidAnalyzerFunctionError(DigDepException):
    """Raise when an invalid analyzer function is called"""
    pass

class InvalidArgumentError(DigDepException):
    """Raise when invalid arguments are passed"""
    pass



