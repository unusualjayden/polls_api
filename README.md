# API для прохождения опросов

## Запуск дев-сервера
* Склонировать репозиторий
* `cd polls_api`
* `python -m venv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py createsuperuser` (для создания админа системы)
* `python manage.py runserver`

## Функционал
Перейдите в своем браузере `http://127.0.0.1:8000/`
####Админка
`/admin` - базовая админка, в которой реализованы создание, редактирование и удаление опросов и вопросов к ним
#### API
`GET /poll` - получение всех активных опросов

`GET /poll/<poll_id>` - получение опроса со всеми вопросами по id опроса

`POST /poll/<poll_id>` - отправка пройденного опроса в формате:

```JSON
{
  "user_id": <user_id>,
  "answers": [
    {
      "question": <question_id>,
      "content": <ответ на вопрос>,
    },
    ...
  ]
}
```

`GET /users/<user_id>` - получение всех пройденных опросов с ответами по <user_id>