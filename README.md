# Diplom_2
Тестирование API для Stellar Burgers

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов с генерацией и просмотром Allure-отчета

pytest --alluredir=allure_results
allure serve allure_results