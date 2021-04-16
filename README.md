# Dockerizing Django with Gunicorn, and Nginx
Uses gunicorn + nginx 

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

1. Change .env files MODE=prod if want to use PostgreSQL for db

1. Test it out at [http://localhost](http://localhost)
1. Api Docs at [http://localhost/api/docs/](http://localhost/api/docs/)
2. API ReDoc at [http://localhost/api/redoc/](http://localhost/api/redoc/)
1. Admin at [http://localhost/admin](http://localhost/admin) 
```sh
username: admin
password: admin
```