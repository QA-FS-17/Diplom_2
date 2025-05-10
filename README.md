# Diplom_2
Тестирование API для Stellar Burgers

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов с генерацией Allure-отчета
pytest --alluredir=allure-results

# Просмотр отчета
allure serve allure-results
