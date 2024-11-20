#!/usr/bin/make

LOCALES=en pl

TRANSLATION_UPDATE=pylupdate5
LANG_RELEASE=lrelease-qt5
I18N_PATH=src/tr_example/i18n
VIRTUAL_ENV_NAME=.venv

PYTHON=$(VIRTUAL_ENV_NAME)/bin/python
TRANSLATION_FILES=$(LOCALES:%=%.ts)
COMPILE_TRANSLATION_FILES=$(LOCALES:%=%.qm)
PYTHON_FILES=$(shell find src -type f -name "*.py")

################ Generate translation files ################
.PHONY: translation_update_init translation_update
translation_update: translation_update_init $(TRANSLATION_FILES)

translation_update_init:
	@echo "Generating translation files."
	mkdir -p "$(I18N_PATH)"

%.ts:
	$(TRANSLATION_UPDATE) $(PYTHON_FILES) -ts "$(I18N_PATH)/$@"

################ Generate compiled translation files ################
.PHONY: translation_compile_init translation_compile
translation_compile: $(COMPILE_TRANSLATION_FILES)

translation_compile_init:
	@echo "Generating translation files."

%.qm: %.ts
	$(LANG_RELEASE) "$(I18N_PATH)/$<" -qm "$(I18N_PATH)/$@"


################ Install in editable mode in local venv ################
create_venv:
	python3 -m venv .venv

pip_install:
	$(PYTHON) -m pip install --editable .
