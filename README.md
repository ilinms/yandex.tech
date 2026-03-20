# Yandex.Disk API Автотесты

Автоматизированные тесты для API Яндекс.Диска на Python с использованием Pytest и Requests.

Реализованы автотесты для проверки основных HTTP-методов:
- GET — получение информации и ресурсов
- PUT — создание папок и публикация
- POST — копирование и перемещение файлов
- DELETE — удаление ресурсов

---

## Стек

- Python 3
- Pytest
- Requests
- Faker
- python-dotenv

---

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/ilinms/yandex.tech.git
cd yandex.tech

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
```

После этого откройте `.env` и укажите OAuth-токен Яндекс.Диска.

---

## Запуск тестов

```bash
# Запуск всех тестов
pytest -v

# Запуск с HTML-отчетом
pytest -v --html=report.html --self-contained-html
```

---

## Особенности

**Важно**

Тесты `test_publish_file` и `test_publish_and_access_public_resource` 
завершаются с ошибкой при проверке скачивания по публичной ссылке.

**Причина:** Яндекс.Диск блокирует автоматические запросы к публичным 
ссылкам (`https://yadi.sk/...`) и возвращает страницу с капчей.

**Решение:** Использовать эндпоинт 
`GET /public/resources/download?public_key={key}`, который возвращает 
прямую ссылку без капчи. В рамках тестового задания данный эндпоинт не использовался.