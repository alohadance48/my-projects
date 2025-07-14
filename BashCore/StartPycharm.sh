#!/bin/bash

# Путь к Pycharm
patch="/home/vladosl/Загрузки/pycharm-professional-2024.3.2/pycharm-2024.3.2/bin/"

#Смена пути до Pycharm

cd "$patch" || exit 1

echo 'Запуск.....'

# Запуск Pycharm
./pycharm.sh
