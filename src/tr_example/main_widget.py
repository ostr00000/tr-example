import logging

from qtpy.QtWidgets import QGridLayout, QLineEdit, QPushButton, QWidget

logger = logging.getLogger(__name__)


class MainWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.counter = 0

        self._layout = QGridLayout(self)
        self.setMinimumSize(300, 20)

        self.button = QPushButton(self.tr("Click me"), self)
        self.button.clicked.connect(self.onClicked)
        self._layout.addWidget(self.button)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setReadOnly(True)
        self._layout.addWidget(self.lineEdit)

    def onClicked(self):
        self.counter += 1
        msg = self.tr(
            "Created %n object", "This is a comment for translation", self.counter
        )
        logger.debug(msg)
        self.lineEdit.setText(msg)
