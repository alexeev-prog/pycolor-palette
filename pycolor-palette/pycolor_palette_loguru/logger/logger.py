#!venv/bin/python3
"""
Copyright Alexeev Bronislav (C) 2024
"""

from time import time
import ast
import inspect
import pprint
import sys
import warnings
from datetime import datetime
import functools
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import colorama
import executing
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer
from typing import Union, List
import logging
from loguru import logger

from pycolor_palette_loguru.paint import debug_message
from pycolor_palette_loguru.pygments_colorschemes import *


PYTHON2 = sys.version_info[0] == 2

_absent = object()
default_theme = Terminal256Formatter(style=CatppuccinMocha)


def set_default_theme(theme):
    global default_theme
    default_theme = Terminal256Formatter(style=theme)


class InterceptHandler(logging.Handler):
    """
    This class describes an intercept handler.
    """

    def emit(self, record) -> None:
        """
        Get corresponding Loguru level if it exists

        :param      record:  The record
        :type       record:  record

        :returns:   None
        :rtype:     None
        """
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger(level: Union[str, int] = "DEBUG", ignored: List[str] = "") -> None:
    """
    Setup logger

    :param      level:    The level
    :type       level:    str
    :param      ignored:  The ignored
    :type       ignored:  List[str]
    """
    logging.basicConfig(
        handlers=[InterceptHandler()], level=logging.getLevelName(level)
    )

    for ignore in ignored:
        logger.disable(ignore)

    logger.info("Logging is successfully configured")


@contextmanager
def supportTerminalColorsInWindows():
    """
    Support terminal colors in Windows OS with colorama.
    """
    colorama.init()
    yield
    colorama.deinit()


def stderrPrint(*args):
    """
    Print to stderr.

    :param      args:  The arguments
    :type       args:  list
    """
    print(*args)


def isLiteral(s):
    """
    Check string if literal.

    :param      s:    string
    :type       s:    str

    :returns:   True if the specified s is literal, False otherwise.
    :rtype:     bool
    """
    try:
        ast.literal_eval(s)
    except Exception:
        return False
    return True


def bindStaticVariable(name, value):
    def decorator(fn):
        """
        Wrapper

        :param      fn:   The function
        :type       fn:   Function
        """
        setattr(fn, name, value)
        return fn

    return decorator


@bindStaticVariable(
    "lexer", PyLexer(ensurenl=False) if PYTHON2 else Py3Lexer(ensurenl=False)
)
def colorize(s):
    """
    Colorize with pygments.

    :param      s:    string
    :type       s:    str

    :returns:   highlighted
    :rtype:     str
    """
    self = colorize
    return highlight(s, self.lexer, default_theme)


DEFAULT_PREFIX = "pydbg_obj | "
DEFAULT_LINE_WRAP_WIDTH = 80  # Characters.
DEFAULT_CONTEXT_DELIMITER = "~ "
DEFAULT_OUTPUT_FUNCTION = colorized_stderr_print
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat


NO_SOURCE_AVAILABLE_WARNING_MESSAGE = (
    "Failed to access the underlying source code for analysis. Was PyDBG_Obj "
    "invoked in a REPL (e.g. from the command line), a frozen application "
    "(e.g. packaged with PyInstaller), or did the underlying source code "
    "change during execution?"
)


def colorized_stderr_print(obj):
    """
    Colorized stderr print.

    :param      obj:  The object
    :type       obj:  object
    """
    for s in obj.split("; "):
        if not s.startswith(f"{DEFAULT_PREFIX} |"):
            s = f"{DEFAULT_PREFIX} | {s}"
        colored = colorize(s)

        with supportTerminalColorsInWindows():
            stderrPrint(colored)


def callOrValue(obj):
    """
    Call or value.

    :param      obj:  The object
    :type       obj:  obj

    :returns:   function
    :rtype:     func
    """
    return obj() if callable(obj) else obj


class Source(executing.Source):
    """
    Source.
    """

    def get_text_with_indentation(self, node):
        """
        Get text with indents.

        :param      node:  The node
        :type       node:  node asttokens

        :returns:   The text with indentation.
        """
        result = self.asttokens().get_text(node)
        if "\n" in result:
            result = " " * node.first_token.start[1] + result
            result = dedent(result)
        result = result.strip()
        return result


def prefixLines(prefix, s, startAtLine=0):
    """
    Prefix lines.

    :param      prefix:       The prefix
    :param      s:            { parameter_description }
    :param      startAtLine:  The start at line
    """
    lines = s.splitlines()

    for i in range(startAtLine, len(lines)):
        lines[i] = prefix + lines[i]

    return lines


def prefixFirstLineIndentRemaining(prefix, s):
    """
    First line indent remaining prefix.

    :param      prefix:  The prefix
    :type       prefix:  prefix
    :param      s:       param
    :type       s:       type

    :returns:   lines
    :rtype:     list
    """
    indent = " " * len(prefix)
    lines = prefixLines(indent, s, startAtLine=1)
    lines[0] = prefix + lines[0]
    return lines


def formatPair(prefix, arg, value):
    """
    Formatting pair.

    :param      prefix:  The prefix
    :param      arg:     The argument
    :param      value:   The value
    """
    if arg is _absent:
        argLines = []
        valuePrefix = prefix
    else:
        argLines = prefixFirstLineIndentRemaining(prefix, arg)
        valuePrefix = argLines[-1] + ": "

    looksLikeAString = (value[0] + value[-1]) in ["''", '""']
    if looksLikeAString:  # Align the start of multiline strings.
        valueLines = prefixLines(" ", value, startAtLine=1)
        value = "\n".join(valueLines)

    valueLines = prefixFirstLineIndentRemaining(valuePrefix, value)
    lines = argLines[:-1] + valueLines
    return "\n".join(lines)


def singledispatch(func):
    """
    Single dispatch function.

    :param      func:                 The function
    :type       func:                 function

    :returns:   func
    :rtype:     func

    :raises     NotImplementedError
    """
    if "singledispatch" not in dir(functools):

        def unsupport_py2(*args, **kwargs):
            raise NotImplementedError(
                "functools.singledispatch is missing in " + sys.version
            )

        func.register = func.unregister = unsupport_py2
        return func

    func = functools.singledispatch(func)

    # add unregister based on https://stackoverflow.com/a/25951784
    closure = dict(zip(func.register.__code__.co_freevars, func.register.__closure__))
    registry = closure["registry"].cell_contents
    dispatch_cache = closure["dispatch_cache"].cell_contents

    def unregister(cls):
        del registry[cls]
        dispatch_cache.clear()

    func.unregister = unregister
    return func


@singledispatch
def argumentToString(obj):
    """
    Convert argument to string.

    :param      obj:  The object
    :type       obj:  obj

    :returns:   String representation of the argument.
    :rtype:     string
    """
    s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
    s = s.replace("\\n", "\n")  # Preserve string newlines in output.
    return s


class PyDBG_Obj:
    """Advanced print for debuging.

    >>> pydbg_obj | num: 12
                                    float_int: 12.12
                                    string: 'Hello'
                                    boolean: True
                                    list_array: [1, 2, 3, 'Hi', True, 12.2]
                                    dictionary: {1: 'HELLO', 2: 'WORLD'}

    """

    _pairDelimiter = "; "
    lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
    contextDelimiter = DEFAULT_CONTEXT_DELIMITER

    def __init__(
        self,
        prefix=DEFAULT_PREFIX,
        outputFunction=DEFAULT_OUTPUT_FUNCTION,
        argToStringFunction=argumentToString,
        includeContext=False,
        contextAbsPath=False,
    ):
        """
        Initialization.

        :param      prefix:               The prefix
        :type       prefix:               prefix
        :param      outputFunction:       The output function
        :type       outputFunction:       output function
        :param      argToStringFunction:  The argument to string function
        :type       argToStringFunction:  function
        :param      includeContext:       The include context
        :type       includeContext:       bool
        :param      contextAbsPath:       The context absolute path
        :type       contextAbsPath:       bool
        """
        self.enabled = True
        self.prefix = prefix
        self.includeContext = includeContext
        self.outputFunction = outputFunction
        self.argToStringFunction = argToStringFunction
        self.contextAbsPath = contextAbsPath

    def __call__(self, *args):
        """
        Call magic method.

        :param      args:  The arguments
        :type       args:  list

        :returns:   passthrough
        :rtype:     list
        """
        if self.enabled:
            callFrame = inspect.currentframe().f_back
            self.outputFunction(self._format(callFrame, *args))

        if not args:
            passthrough = None
        elif len(args) == 1:
            passthrough = args[0]
        else:
            passthrough = args

        return passthrough

    def format(self, *args):
        """
        Format arguments.

        :param      args:  The arguments
        :type       args:  list

        :returns:   formatted out
        :rtype:     call frame formatted
        """
        callFrame = inspect.currentframe().f_back
        out = self._format(callFrame, *args)
        return out

    def _format(self, callFrame, *args):
        """
        Format helper function.

        :param      callFrame:  The call frame
        :type       callFrame:  call frame
        :param      args:       The arguments
        :type       args:       list

        :returns:   formatted
        :rtype:     formatted out
        """
        prefix = callOrValue(self.prefix)

        context = self._formatContext(callFrame)
        if not args:
            time = self._formatTime()
            out = prefix + context + time
        else:
            if not self.includeContext:
                context = ""
            out = self._formatArgs(callFrame, prefix, context, args)

        return out

    def _formatArgs(self, callFrame, prefix, context, args):
        """
        Format arguments.

        :param      callFrame:  The call frame
        :type       callFrame:  call frame
        :param      prefix:     The prefix
        :type       prefix:     prefix
        :param      context:    The context
        :type       context:    content
        :param      args:       The arguments
        :type       args:       args

        :returns:   formatted args
        :rtype:     args
        """
        callNode = Source.executing(callFrame).node
        if callNode is not None:
            source = Source.for_frame(callFrame)
            sanitizedArgStrs = [
                source.get_text_with_indentation(arg) for arg in callNode.args
            ]
        else:
            warnings.warn(
                NO_SOURCE_AVAILABLE_WARNING_MESSAGE,
                category=RuntimeWarning,
                stacklevel=4,
            )
            sanitizedArgStrs = [_absent] * len(args)

        pairs = list(zip(sanitizedArgStrs, args))

        out = self._constructArgumentOutput(prefix, context, pairs)
        return out

    def _constructArgumentOutput(self, prefix, context, pairs):
        """
        Construct argument output.

        :param      prefix:   The prefix
        :type       prefix:   prefix
        :param      context:  context
        :type       context:  context
        :param      pairs:    The pairs
        :type       pairs:    pairs

        :returns:   argument output
        :rtype:     string
        """

        def argPrefix(arg):
            return "%s: " % arg

        pairs = [(arg, self.argToStringFunction(val)) for arg, val in pairs]
        pairStrs = [
            val if (isLiteral(arg) or arg is _absent) else (argPrefix(arg) + val)
            for arg, val in pairs
        ]

        allArgsOnOneLine = self._pairDelimiter.join(pairStrs)
        multilineArgs = len(allArgsOnOneLine.splitlines()) > 1

        contextDelimiter = self.contextDelimiter if context else ""
        allPairs = prefix + context + contextDelimiter + allArgsOnOneLine
        firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

        if multilineArgs or firstLineTooLong:
            if context:
                lines = [prefix + context] + [
                    formatPair(len(prefix) * " ", arg, value) for arg, value in pairs
                ]
            else:
                argLines = [formatPair("", arg, value) for arg, value in pairs]
                lines = prefixFirstLineIndentRemaining(prefix, "\n".join(argLines))
        else:
            lines = [prefix + context + contextDelimiter + allArgsOnOneLine]

        return "\n".join(lines)

    def _formatContext(self, callFrame):
        """
        Function for format call frame.

        :param      callFrame:  callframe
        :type       callFrame:  call frame

        :returns:   context
        :rtype:     string
        """
        filename, lineNumber, parentFunction = self._getContext(callFrame)

        if parentFunction != "<module>":
            parentFunction = "%s()" % parentFunction

        context = f"{filename}:{lineNumber} in {parentFunction}"
        return context

    def _formatTime(self):
        """
        Function for format time.

        :returns:   format time
        :rtype:     str
        """
        now = datetime.now()
        formatted = now.strftime("%H:%M:%S.%f")[:-3]
        return " at %s" % formatted

    def _getContext(self, callFrame):
        """
        Get context of call frame.

        :param      callFrame:  The call frame
        :type       callFrame:  callFrame

        :returns:   The context.
        :rtype:     context
        """
        frameInfo = inspect.getframeinfo(callFrame)
        lineNumber = frameInfo.lineno
        parentFunction = frameInfo.function

        filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
        return filepath, lineNumber, parentFunction

    def enable(self):
        """
        Enable pydbg_obj.
        """
        self.enabled = True

    def disable(self):
        """
        Disable pydbg_obj.
        """
        self.enabled = False

    def configureOutput(
        self,
        prefix=_absent,
        outputFunction=_absent,
        argToStringFunction=_absent,
        includeContext=_absent,
        contextAbsPath=_absent,
    ):
        """
        Configure output of pydbg_obj.

        :param      prefix:               The prefix
        :type       prefix:               prefix
        :param      outputFunction:       The output function
        :type       outputFunction:       output function
        :param      argToStringFunction:  The argument to string function
        :type       argToStringFunction:  arg to string function
        :param      includeContext:       The include context
        :type       includeContext:       include context
        :param      contextAbsPath:       The context absolute path
        :type       contextAbsPath:       context abs path

        :raises     TypeError:            no parameter provided
        """
        noParameterProvided = all(
            v is _absent for k, v in locals().items() if k != "self"
        )
        if noParameterProvided:
            raise TypeError("configureOutput() missing at least one argument")

        if prefix is not _absent:
            self.prefix = prefix

        if outputFunction is not _absent:
            self.outputFunction = outputFunction

        if argToStringFunction is not _absent:
            self.argToStringFunction = argToStringFunction

        if includeContext is not _absent:
            self.includeContext = includeContext

        if contextAbsPath is not _absent:
            self.contextAbsPath = contextAbsPath


def debug_func(func, *args, **kwargs):
    """Decorator for print info about function.

    Arguments:
    ---------
    + func - executed func

    """

    def wrapper():
        func(*args, **kwargs)

    message = f"debug @ Function {func.__name__}() executed at {datetime.now()}"
    debug_message(message, False)
    return wrapper


def benchmark(func, *args, **kwargs):
    """Measuring the speed of function execution (decorator).

    Arguments:
    ---------
    + func - executed func

    """
    start = time()

    def wrapper():
        func(*args, **kwargs)

    end = time()
    total = round(end - start, 2)
    debug_message(
        f"benchmark {func} @ Execution function {func.__name__} time: {total} sec", True
    )
    return wrapper
