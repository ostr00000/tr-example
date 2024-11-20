from __future__ import annotations

import inspect
import sys
from typing_extensions import LiteralString

from qtpy.QtWidgets import QApplication


class TR:
    """
    This class add translation functions that respect current class name.

    When generating translations, a class name is used as a context.
    Ex:
    >>> class Context(TR):
    >>>     pass
    >>> Context.tr("Some text to translate")
    Starting from Python 3, the `tr` method is supported as class method.
    Multiple inheritance is allowed (QObject.tr do not respect it).

    WARNING:
        Translation will not work if you put a breakpoint
        in scope with `tr` method and an IDE change its bytecode (PyCharm confirmed).
    """

    @classmethod
    def QT_TR_NOOP(cls, text: LiteralString) -> str:
        """
        This function is detected by qt translation finder (lupdate).

        It should be used to create text translation when the python code should not
        return translation yet.
        """
        return text

    @classmethod
    def runtimeTr(cls, msg: str, disambiguation: str | None = None, n: int = -1):
        """Same method as `tr`, but without LiteralString.

        This is only to prevent type-checker raising an error.
        We cannot call `tr` function, because then add another frame.
        """
        curFrame = inspect.currentframe()
        name = cls.__name__ if curFrame is None else cls.__getClassName(curFrame.f_back)
        return QApplication.translate(name, msg, disambiguation, n)

    @classmethod
    def tr(
        cls, msg: LiteralString, disambiguation: str | None = None, n: int = -1
    ) -> str:
        curFrame = inspect.currentframe()
        # frameless python, maybe try normal class name
        name = cls.__name__ if curFrame is None else cls.__getClassName(curFrame.f_back)
        return QApplication.translate(name, msg, disambiguation, n)

    @classmethod
    def __getClassName(cls, frame) -> str:
        # if we are in class definition `co_name` is a name of currently defined class
        codeName = frame.f_code.co_name
        className = frame.f_locals.get("__qualname__", "").rsplit(".")[-1]
        if className and codeName == className:
            return codeName

        for mro in cls.__mro__:
            functionName = cls.__mangle(frame.f_code.co_name, mro.__name__)
            funOrDescriptor = mro.__dict__.get(functionName)
            if funOrDescriptor is None:
                continue

            if hasattr(funOrDescriptor, "__func__"):
                # classmethod/staticmethod
                fun = funOrDescriptor.__func__
            elif isinstance(funOrDescriptor, property):
                # we need to check all function used in property
                for f in (
                    funOrDescriptor.fget,
                    funOrDescriptor.fset,
                    funOrDescriptor.fdel,
                ):
                    if f is not None and f.__code__ is frame.f_code:
                        return mro.__name__
                continue
            else:
                fun = funOrDescriptor

            fun = inspect.unwrap(fun)
            if fun.__code__ is frame.f_code:
                return mro.__name__

        # if none function match then maybe it is called as class method
        return cls.__name__

    MANGLE_LEN = sys.maxsize

    @classmethod
    def __mangle(cls, name: str, klass: str):
        """
        This function comes from compile package that was removed in Python 3.

        More info: https://stackoverflow.com/a/11024578
        """
        if not name.startswith("__"):
            return name
        if len(name) + 2 >= cls.MANGLE_LEN:
            return name
        if name.endswith("__"):
            return name
        try:
            i = 0
            while klass[i] == "_":
                i = i + 1
        except IndexError:
            return name
        klass = klass[i:]

        tlen = len(klass) + len(name)
        if tlen > cls.MANGLE_LEN:
            klass = klass[: cls.MANGLE_LEN - tlen]

        return f"_{klass}{name}"
