# Yandex.Disk API Автотесты

Автоматизированные тесты для API Яндекс.Диска на Python с использованием Pytest и Requests.

---

## Установка

```bash
# Клонировать репозиторий
git clone <repository-url>
cd pythonYandex.tech

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

---

## Настройка

```bash
# Скопировать файл окружения
cp .env.example .env
```

После этого откройте `.env` и добавьте ваш токен Яндекс.Диска.

---

## Запуск тестов

```bash
# Запуск всех тестов
pytest -v

# Запуск с HTML-отчетом
pytest -v --html=report.html --self-contained-html
```
**Важно**

Прямой доступ к публичным ссылкам (`https://yadi.sk/...`) через библиотеку `requests`  
блокируется капчей.

Для скачивания публичных файлов используется официальный метод API:

```http
GET /resources/download?public_key={key}
```

Этот метод возвращает прямую ссылку на файл без капчи.
