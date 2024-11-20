# Example for PyQt translations

This project aim to show how translation works in PyQt.

1. First `pylupdate`
   [program](https://code.qt.io/cgit/qt/qttools.git/tree/src/linguist/lupdate/python.cpp#n676)
   scann `.py` files (also `.ui` files)
   for translation strings (`.py` -> `.ts`).

    - You can use `translate` function with any context name.
    - You can use `.tr` method only on `self` object (your class must inherit
      from
      `QObject`).

2. The programmer now should edit `.ts` files using QtLinguist.
3. After translation is completed and saved, `lrelease` program must be executed
   to generate binary files with translations (`.ts` -> `.qm`).
4. When Python program starts, it should load translations from `.qm` files.
5. Finally, when program call `tr` or `translate`,
   the requested text is searched.
   On success the translated text is returned,
   otherwise unmodified text is returned.

See also official documentations:

- https://doc.qt.io/qt-5/i18n-source-translation.html
- https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html