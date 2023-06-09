# Покрокова інструкція для запуску проєкту

Для запуску проекту знадобиться виконати всі подальші налаштування.  

- [Покрокова інструкція для запуску проєкту](#покрокова-інструкція-для-запуску-проєкту)
  - [Скачування та налаштування проєкту](#скачування-та-налаштування-проєкту)
  - [MongoDB](#mongodb)
    - [Віддалена БД](#віддалена-бд)
    - [Локальна БД](#локальна-бд)
  - [api](#api)
  - [web](#web)


## Скачування та налаштування проєкту

1. Виконати встановлення Git для вашої системи
2. Відкрити Термінал та директорію для зберігання проєктів у ньому 
3. *git clone git@github.com:IKerrigan/Universal-software-platform-for-applied-statistical-data-analysis.git*

## MongoDB 

Варіантів розгорнути MongoDB багато - нижче розглянуто два найбільш популярних:

### Віддалена БД

1. Зареєструватись та створити віддалену БД з офіційного сайту https://www.mongodb.com/  

### Локальна БД

1. Встановити Docker Desktop https://www.docker.com/products/docker-desktop/
2. Відкрити Термінал і виконати *docker pull mongo*

## api

1. Виконати встановлення Python 3.10+ з офіційного сайту https://www.python.org/
2. Встановити всі залежності проєкту за допомогою *pip install package* де package ім'я пакету:

- flask
- matplotlib
- scipy
- mpld3
- math
- pandas
- numpy
- scikit_posthocs

3. Потім з кореня проєкту запустіть сервер командою *python .\api\index.py*

## web

1. Виконати встановлення NodeJS 17+ з офіційного сайту https://nodejs.org/
2. Зайдіть в директорію web та виконайте *npm i* для встановлення всіх залежностей.
3. В цій самій директорії створіть файл з назвою *.env* для налаштування web-серверу:

```
PORT=3000 # Порт серверу

SALT_WORK_FACTOR=10 # Параметр для генерації солі для пароля
MONGO_URI=mongodb://localhost:27017 # Адреса MongoDB сервера
ANALYSER_URL=http://127.0.0.1:5000 # Адреса api сервера
JWT_SECRET=RandomJWTString # JWT секрет для генерації ключа
```

3. Потім запустіть web-сервер командою *npm start*
4. Відкрийте браузер і зайдіть на сторінку http://localhost:3000/ де 3000 це порт, що вказанний у файлі *.env*
