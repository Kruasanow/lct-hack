



![LOGO](https://storage.blackterminal.com/source/img/emitents/background_img_logo/1/2VNzTGsSAtMWkjd1czBI5JXSmv0S-So8.jpg)

<h1 align="center">CopyPasteAdapt</h1>
<h1 align="center"><a href="http://188.242.135.131:5000/">Live Demo</a></h21>
<h2 align="center">Решение команды CopyPasteAdapt</h2>


[![Описание](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=008BFF&background=2DFFDA00&width=435&lines=%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)](https://git.io/typing-svg)

Наше решение основано на фреимворке Flask, позволяет администратору в автоматическом режиме распределять задачи между сотрудниками банка. Ресурс рабоает а паре с мобилным приложением для сотрудников,созданном на фреимворке Flutter.

<br />

> Фишки:

- ✅ База данный: `SQLite`
- ✅ `DB Tools`: SQLAlchemy ORM
- ✅ Session-Based authentication (via **flask_login**), Forms validation
- ✅ `Docker`
- ✅ Система уведомлений



<br />

[![DEMO](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=008BFF&random=false&width=435&lines=DEMO)](https://git.io/typing-svg)

> Для аутентификации используйте стандартное имя пользователя и пароль ***admin / 1234***  

-  [Страница авторизации](https://www.creative-tim.com/live/material-dashboard-flask)

<br />

[![Порядок установки и запуска](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=008BFF&background=2DFFDA00&width=435&lines=%D0%9F%D0%BE%D1%80%D1%8F%D0%B4%D0%BE%D0%BA+%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8+%D0%B8+%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0)](https://git.io/typing-svg)

> 👉 **Важно** -Локальный запуск 

```bash
$ # Клонируйте репозиторий
$ git clone https://github.com/creativetimofficial/material-dashboard-flask.git
$ cd material-dashboard-flask
$
$ # Активируйте виртуальное окружение
$ virtualenv env
$ .\env\Scripts\activate
$
$ # Установите модули
$ pip3 install -r requirements.txt
$
$ # Запустите приложение (режим разработчика)
$ flask run 
$
$ # Перейдите в браузер по ссылке: http://127.0.0.1:5000/
```
<br />

### 👉 Создание пользователей

Чтобы создать пользователей необходимо от имени администратора перейти в таблицу пользователи,добавить нового пользователя, или прописать 
  - `/register` от имени администратора

[![Структура проекта](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=008BFF&random=false&width=435&lines=%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0+%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0)](https://git.io/typing-svg)

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # обработчики HTML файлов из папки home
   |    |
   |    |-- authentication/                 # обработчики страниц авторизации и регистрации
   |    | 
   |    |-- api/                            # обработчики api
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS, Javascripts файлы
   |    |
   |    |-- templates/                      #  
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Навигация
   |    |    |    |-- sidebar.html          # Слайд бар 
   |    |    |    |-- scripts.html          # Скрипты
   |    |    |
   |    |    |-- layouts/                   # 
   |    |    |    |-- base-fullscreen.html  # Используется в навигации
   |    |    |    |-- base.html             # Используется всеми страницами
   |    |    |
   |    |    |-- accounts/                  # Страницы авторизации и регистрации
   |    |    |    |-- login.html            
   |    |    |    |-- register.html         
   |    |    |
   |    |    |-- home/                      # Основные страницы приложения
   |    |         |-- billing.html           
   |    |         |-- calendar.html         
   |    |         |-- index.html
   |    |         |-- map.html
   |    |         |-- points.html
   |    |         |-- porfile.html
   |    |         |-- tables.html
   |    |         |-- temlpate.html
   |    |         |-- users.html
   |    |         |-- workers.html                         
   |    |
   |  db.sqlite3
   |  config.py                             
   |    __init__.py                         
   |
   |-- requirements.txt                     # Зависимости
   |
   |-- run.py                               # 
   |
   |-- ************************************************************************
```

![](https://github.com/Platane/snk/raw/output/github-contribution-grid-snake.svg)