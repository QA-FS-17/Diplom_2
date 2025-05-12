# Очистка предыдущих результатов
Remove-Item -Path .\allure_results\* -Recurse -Force -ErrorAction SilentlyContinue
New-Item -Path .\allure_results -ItemType Directory -Force | Out-Null

# Запуск тестов с генерацией Allure-отчетов
pytest .\tests\ --alluredir=allure_results

# Генерация HTML-отчета
allure generate .\allure_results -o .\allure_report --clean

# Открытие отчета в браузере по умолчанию
allure open .\allure_report