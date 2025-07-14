#!/bin/bash

VENV_NAME="venv"

# Создание виртуальной среды
python3 -m venv $VENV_NAME

# Инструкция по активации
echo "Для активации виртуальной среды выполните: source $VENV_NAME/bin/activate"
