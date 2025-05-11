# Получаем текущую директорию
$ROOT_DIR = $PWD

# Очищаем предыдущие результаты
Remove-Item -Recurse -Force -Path "$ROOT_DIR\allure_results" -ErrorAction SilentlyContinue

# Запускаем тесты с явным указанием директории для отчетов
& pytest "$ROOT_DIR\tests" -v --alluredir="$ROOT_DIR\allure_results"

# Проверяем наличие результатов
if (Test-Path "$ROOT_DIR\allure_results\*.json") {
    & allure serve "$ROOT_DIR\allure_results" --clean
} else {
    Write-Host "Файлы с результатами не найдены в $ROOT_DIR\allure_results" -ForegroundColor Red
    exit 1
}