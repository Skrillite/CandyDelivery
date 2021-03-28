## Установка и запуск приложения
### Зависимости python
Для запуска приложения потребуется python версии 3.9 и выше. Следующая команда установит зависимости

    pip install -r requirements.txt
    
### Переменные окружения
Вы можете выставить следующие переменные окружения в системе или .evn файле

    # postgresql conf
    # all fields are required
    POSTGRES_USER = user
    POSTGRES_PASSWORD = password 
    POSTGRES_DB = postgres_database_name

    #sanic conf
    HOSTNAME = localhost  #default localhost
    PORT = 8000           #default 8000
    WORKERS = 2           #default 1
    DEBUG = 0             #default 0
    
### Применение миграции
Для применения миграции к базе выполните, находясь в корне проекта

    alembic upgrade head
