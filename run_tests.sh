#!/bin/bash

# Полные пути к директориям
ALLURE_RESULTS="${PWD}/allure_results"
ALLURE_REPORT="${PWD}/allure_report"
TESTS_RESULTS="${PWD}/tests/allure_results"

# Жёсткая очистка всех возможных директорий
rm -rf "$ALLURE_RESULTS" "$ALLURE_REPORT" "$TESTS_RESULTS" 2>/dev/null || true

# Дополнительная очистка на случай кэширования
find . -type d -name "allure_results" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "allure_report" -exec rm -rf {} + 2>/dev/null || true

# Запуск только нужного теста с явным указанием директории
pytest tests/test_orders.py::TestOrderCreation::test_unauthorized_access \
  -v \
  --alluredir="$ALLURE_RESULTS"

# Генерация и открытие отчёта
allure serve "$ALLURE_RESULTS" --clean