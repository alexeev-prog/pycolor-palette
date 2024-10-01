#!/usr/bin/python3
from datetime import datetime
from sys import stdout, stdin
from time import sleep
import os


def cls():
    """
    Clear screen (unix).
    """
    os.system("clear")


class FG:
    """
    Foreground class.
    """

    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """
        Function for convert rgb to ansi color code.

        :param      r:    red color
        :type       r:    int
        :param      g:    green color
        :type       g:    int
        :param      b:    blue color
        :type       b:    int

        :returns:   color
        :rtype:     str
        """
        return f"\u001b[38;2;{r};{g};{b}m"


class BG:
    """
    Background class.
    """

    black = "\u001b[40m"
    red = "\u001b[41m"
    green = "\u001b[42m"
    yellow = "\u001b[43m"
    blue = "\u001b[44m"
    magenta = "\u001b[45m"
    cyan = "\u001b[46m"
    white = "\u001b[47m"

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """
        Function for convert rgb to ansi color code.

        :param      r:    red color
        :type       r:    int
        :param      g:    green color
        :type       g:    int
        :param      b:    blue color
        :type       b:    int

        :returns:   color
        :rtype:     str
        """
        return f"\u001b[48;2;{r};{g};{b}m"


class Style:
    """
    Style class.
    """

    reset = "\u001b[0m"
    bold = "\u001b[1m"
    dim = "\u001b[2m"
    italic = "\u001b[3m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"
    clear = "\u001b[2J"
    clearline = "\u001b[2K"
    up = "\u001b[1A"
    down = "\u001b[1B"
    right = "\u001b[1C"
    left = "\u001b[1D"
    nextline = "\u001b[1E"
    prevline = "\u001b[1F"
    top = "\u001b[0;0H"

    @staticmethod
    def to(x, y):
        """
        Move cursor to x, y.

        :param      x:    x
        :type       x:    int
        :param      y:    y
        :type       y:    int

        :returns:   cursor
        :rtype:     string
        """
        return f"\u001b[{y};{x}H"

    @staticmethod
    def write(text="\n"):
        """
        Print to stdout.

        :param      text:  The text
        :type       text:  str
        """
        stdout.write(text)
        stdout.flush()

    @staticmethod
    def writew(text="\n", wait=0.01):
        """
        Print (typewrite effect).

        :param      text:  The text
        :type       text:  str
        :param      wait:  The wait
        :type       wait:  float
        """
        for char in text:
            stdout.write(char)
            stdout.flush()
            sleep(wait)

    @staticmethod
    def read(begin=""):
        """
        Read input from keyboard.

        :param      begin:  The begin
        :type       begin:  str
        """
        text = ""
        stdout.write(begin)
        stdout.flush()
        while True:
            char = ord(stdin.read(1))

        if char == 3:
            return
        elif char in (10, 13):
            return text
        else:
            text += chr(char)

    @staticmethod
    def readw(begin="", wait=0.5):
        """
        Read input with wait.

        :param      begin:  The begin
        :type       begin:  str
        :param      wait:   The wait
        :type       wait:   float
        """
        text = ""

        for char in begin:
            stdout.write(char)
            stdout.flush()
            sleep(wait)

        while True:
            char = ord(stdin.read(1))

            if char == 3:
                return
            elif char in (10, 13):
                return text
            else:
                text += chr(char)


def info_message(text: str, highlight: bool = False) -> str:
    """
    print info message

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.green}{FG.black}" if highlight else f"{FG.green}"
    message = "%s%-*s | %-*s%s ::: %s%s" % (
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        "INFO",
        Style.reset,
        text,
        Style.reset,
    )
    print(message)


def warn_message(text: str, highlight: bool = False) -> str:
    """
    print warn message

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.yellow}{FG.black}" if highlight else f"{FG.yellow}"
    message = "%s%-*s | %-*s%s ::: %s%s" % (
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        "WARNING",
        Style.reset,
        text,
        Style.reset,
    )
    print(message)


def error_message(text: str, highlight: bool = False) -> str:
    """
    print error message

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.red}{FG.black}" if highlight else f"{FG.red}"
    message = "%s%-*s | %-*s%s ::: %s%s" % (
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        "ERROR",
        Style.reset,
        text,
        Style.reset,
    )
    print(message)


def debug_message(text: str, highlight: bool = False) -> str:
    """
    print debug message

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.blue}{FG.black}" if highlight else f"{FG.blue}"
    message = "%s%-*s | %-*s%s ::: %s%s" % (
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        "DEBUG",
        Style.reset,
        text,
        Style.reset,
    )
    print(message)


def other_message(text: str, msg_type: str, highlight: bool = False) -> str:
    """
    print message

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.magenta}{FG.black}" if highlight else f"{FG.magenta}"
    message = "%s%-*s | %-*s%s ::: %s%s" % (
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        msg_type,
        Style.reset,
        text,
        Style.reset,
    )
    print(message)


def run_exception(text: str, highlight: bool = False):
    """
    print and raise exception

    :param      text:       The text
    :type       text:       str
    :param      highlight:  The highlight
    :type       highlight:  bool

    :returns:   message
    :rtype:     str
    """
    prefix = f"{BG.red}{FG.black}" if highlight else f"{FG.red}"
    message = "%s%s%-*s | %-*s ::: %s%s" % (
        Style.bold,
        prefix,
        20,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        20,
        "EXCEPTION",
        text,
        Style.reset,
    )
    print(message)
    raise Exception(text)
