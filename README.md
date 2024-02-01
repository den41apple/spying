# За нами следят (Python)
**Сервис принимает список ссылок, и предоставляет список доменов из переданных ссылок**


### Установка зависимостей
```shell
python -m pip install -r requirements.txt
```

### Переменные окружения
```
DB_ECHO <bool> - Включает вывод SQL в командной строке
DB_FILE <str> - Путь до файла с БД
```

### Запуск сервера
```shell
python -m uvicorn main:app
```

### Запуск тестов
```shell
python -m pytest tests/tests.py -v
```

### Документация Swagger 
http://127.0.0.1:8000/docs


### Структура проекта
```
│   main.py             # Точка входа
│   config.py           # Конфигурационные параметры
│   validator_utils.py  # Инструменты для валидации
│
├───api 
│       models.py       # Модели запросов и ответов API
│       __init__.py
│
├───db
│       actions.py      # Операции с БД
│       db.py           # Объекты базы данных
│       models.py       # Модели базы данных
│       __init__.py
│
├───migrations          # Миграции схем БД
│
└───tests
        conftest.py
        tests.py        # Тесты API
```
