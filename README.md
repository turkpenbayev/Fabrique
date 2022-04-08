# Dockerizing Django with Gunicorn, and Nginx
Предлагается написать микросервис,  который реализует API для защиты интеллектуальной собственности на любом питонячем фреймворке: Flask / Django / FastAPI / whatever rocks your boat, использовать можно любые БД.

Сервис реализует единственный API handle:

POST /protect  – принимает на вход:
Имя автора,
файл размером до 1 гб., считает по нему чек-сумму (алгоритм – на ваше успотрение), сохраняет это в базе и возвращает эту чек-сумму, имя автора и timestamp. В случае, если такой файл уже был кем-то "задепонирован", сервис возвращает ошибку.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

1. Build the images for production uses PostgreSQL for db:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

1. Test it out at [http://localhost/protect/](http://localhost/protect/)
1. Api Docs at [http://localhost/api/docs/](http://localhost/api/docs/)
2. API ReDoc at [http://localhost/api/redoc/](http://localhost/api/redoc/)
