# Проверка работоспособности API-сервиса для учёта инцидентов

<h2>Переменные окружения для работы с БД</h2>

Добавляем в корневую папку .env файл с данными
```bash
# .env
DB_USER=root
DB_PASS=supersecretpwd
DB_NAME=incidents_db
DB_HOST=db
DB_PORT=3306
```

<h2>Команды в терминале Linux для запуска:</h2>

Переходим в папку с проектом
```bash
cd <path_to_project_folder>/incident_service
```

Сборка проекта и запуск контейнеров
```bash
docker compose up -d --build
```
<h2>Тестирование сервиса через встроенную документацию FastAPI:</h2>

После успешного запуска документация доступна по адресу:
```bash
http://127.0.0.1:8000/docs
```

<h2>Тестирование сервиса через команду curl:</h2>

Список всех инцидентов
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/incidents' \
  -H 'accept: application/json'
```

Список инцидентов с фильтром по статусу new
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/incidents?status=new' \
  -H 'accept: application/json'
```

Получение конкретного инцидента по ID
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/incidents/2' \
  -H 'accept: application/json'
```

Создание инцидента
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/incidents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Самокат не в сети",
  "source": "monitoring"
  }'
```

Изменение статуса инцидента на resolved
```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/incidents/2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"status": "resolved"}'

```
