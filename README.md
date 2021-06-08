# E-9.11 Event manager

## Характеристики:

Приложение создаёт пользователям события.

Создано на  Python + Flask.

### Инсталяция:

скачать проект, перейти в его директорию

создать виртуальное окружение

активировать виртуальное окружение

установить зависимости

создать переменные окружения:

export FLASK_APP=events

export FLASK_DEBUG=1

export SECRET_KEY=your_secret_key

export DATABASE_

URL=postgresql://postgres:password@postgres:5432/database

Если не задать DATABASE_URL, то будет использована SQLite
                                      (sqlite:///temp.db)

создать таблицы в базе данных

flask db upgrade

запустить сервер

flask run

#### Работа:

перейти на страницу: http://127.0.0.1:5000/

зарегистрироватся, создать событие

проверить результат.
