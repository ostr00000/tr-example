from qtpy.QtCore import QObject
import logging

from tr_example.tr_wrapper import TR

logger = logging.getLogger(__name__)


class Base(QObject):
    def method(self):
        return self.tr("Translation")


class Inherited(Base):
    pass


def inheritanceBad():
    inh = Inherited()
    logger.debug(f"This is Qt inheritance (bad): {inh.method()=}")


################################################################


class BaseTr(TR, QObject):
    def method(self):
        return self.tr("Translation")


class InheritedTr(BaseTr):
    pass


def inheritanceGood():
    inh = InheritedTr()
    logger.debug(f"This is TR inheritance (good): {inh.method()=}")
    logger.debug(f"This is TR class method (good): {BaseTr.tr("Translation")=}")


################################################################
class TranslatedClassVar(TR):
    TranslatedClassVar = TR

    name = TranslatedClassVar.tr("Name")
    age = TranslatedClassVar.tr("Age")

    # use original string - we translate it later
    address = TranslatedClassVar.QT_TR_NOOP("Address")


def classVarGood():
    logger.debug(f"This is TR class variable (good): {TranslatedClassVar.name=}")
    logger.debug(f"This is TR class variable (good): {TranslatedClassVar.age=}")

    address = TranslatedClassVar.runtimeTr(TranslatedClassVar.address)
    logger.debug(f"This is TR raw class variable (good): {address=}")
