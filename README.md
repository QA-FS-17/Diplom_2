# 🚀 Diplom_2: Тестирование API для Stellar Burgers

 
*Дипломный проект для курса автоматизации тестирования*

## 📌 О проекте

Проект содержит автоматизированные тесты API для сервиса Stellar Burgers.  
Покрыты основные сценарии работы с:
- Пользователями (регистрация, авторизация, профиль)
- Заказами (создание, получение списка)
- Ингредиентами

## ⚙️ Технологии

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Pytest-7.4-green?logo=pytest" alt="Pytest">
  <img src="https://img.shields.io/badge/Allure-2.13-orange?logo=allure" alt="Allure">
  <img src="https://img.shields.io/badge/Requests-2.32-lightgrey?logo=python" alt="Requests">
</p>

## 📂 Структура проекта
```bash
Diplom_2/
├── tests/               # Тесты
│   ├── test_*.py        # Тестовые классы
│   └── conftest.py      # Фикстуры Pytest
├── helpers/             # Вспомогательные модули
│   ├── api_client.py    # Клиент для работы с API
│   ├── data.py          # Константы и данные
│   └── generators.py    # Генераторы тестовых данных
├── .gitignore
├── requirements.txt     # Зависимости
├── pytest.ini          # Конфигурация Pytest
└── README.md           # Этот файл
```

## 🛠 Установка и запуск

### Установка зависимостей
```bash
pip install -r requirements.txt
```

## 🛠 Запуск тестов

### Стандартный запуск
```bash
pytest tests/
```

### С генерацией отчета Allure
```bash
pytest --alluredir=allure_results
allure serve allure_results
```

### Параметры запуска
```bash
# Запуск конкретного теста
pytest tests/test_user_creation.py::TestUserCreation::test_registration_success
```
```bash
# Запуск с подробным выводом
pytest -v
```
```bash
# Генерация HTML-отчета
pytest --html=report.html
```

## 📊 **Тест-кейсы**

| Модуль                  | Тестовые сценарии                          | Статус |
|-------------------------|--------------------------------------------|--------|
| `test_user_creation.py` | Регистрация пользователя, ошибки валидации | ✅      |
| `test_user_login.py`    | Авторизация, неверные credentials          | ✅      |
| `test_user_profile.py`  | Обновление профиля, ошибки доступа         | ✅      |
| `test_orders.py`        | Создание заказов, проверка ингредиентов    | ✅      |
| `test_user_orders.py`   | Получение истории заказов                  | ✅      |

## 📈 Allure-отчет
### После запуска тестов с генерацией отчета:

Откроется браузер с интерактивным отчетом

### Доступна фильтрация по:

Тегам (@allure.story)

Статусу тестов

Времени выполнения