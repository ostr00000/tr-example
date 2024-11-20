import importlib.resources
import locale
import logging
from pathlib import Path

from qtpy.QtCore import QCoreApplication, QTranslator

logger = logging.getLogger(__name__)


def loadTranslation(lang: str = ""):
    try:
        i18nDir = importlib.resources.files("tr_example.i18n")
    except ImportError:
        i18nDir = Path(__file__).resolve().parent / "i18n"

    validTr = i18nDir / "en.qm"

    if not lang:
        maybeLang, encoding = locale.getlocale()
        if maybeLang is not None:
            lang = maybeLang[:2]

    if lang:
        trFile = i18nDir / f"{lang}.qm"
        if trFile.exists():
            validTr = trFile

    translator = QTranslator(QCoreApplication.instance())
    ok = translator.load(str(validTr))
    if not ok:
        logger.error(f"Failed to load {validTr}")
        return False

    ok = QCoreApplication.installTranslator(translator)
    if not ok:
        logger.error(f"Failed to install translator for {validTr}")
        return False
    logger.info(f"Translation loaded: {validTr}")
    return True
