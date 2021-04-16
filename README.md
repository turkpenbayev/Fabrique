# Dockerizing Django with Celery, Redis, Gunicorn, and Nginx
Uses gunicorn + nginx + celery + redis.

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```


1. Test it out at [http://localhost](http://localhost)
1. Api Docs at [http://localhost/api/docs/](http://localhost/api/docs/)
1. Admin at [http://localhost/admin](http://localhost/admin) 
```sh
username: admin
password: admin
```