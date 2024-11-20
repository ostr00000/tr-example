import locale
import logging
import os
import sys

logger = logging.getLogger(__name__)


def configureApp():
    os.environ["QT_API"] = "pyqt6"
    logging.basicConfig(level=logging.DEBUG)
    locale.setlocale(locale.LC_ALL, "")


def main():
    from qtpy.QtWidgets import QApplication, QMainWindow
    from tr_example.main_widget import MainWidget
    from tr_example import loadTranslation

    app = QApplication(sys.argv)
    loadTranslation()


    from tr_example.inheritance import inheritanceBad, inheritanceGood, classVarGood
    inheritanceBad()
    inheritanceGood()
    classVarGood()


    mw = QMainWindow()
    mw.setCentralWidget(MainWidget(mw))
    mw.show()
    app.exec_()


if __name__ == "__main__":
    configureApp()
    main()
