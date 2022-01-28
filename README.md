# sample_project  ![example workflow](https://github.com/kagabof/sample_project/actions/workflows/docker-image.yml/badge.svg)

Django application storing vectors of float values of certain length (hashes)

### How to run the project

- Clone the project and change the current directory to `sample_project`

```
    $ git clone https://github.com/kagabof/sample_project
    $ cd sample_project
    $ git checkout dev

```

- create an activate a python environment

```
    $ python3 -m venv <your folder path>
    $ source <your folder path>/bin/activate
```

- create `.env` file for development environment and copy env example from the `./.env.example`
- create `.env.text` file for development environment and copy env example from the `./.env.text.example`

- Build the project using docker

```
    $ docker-compose build app
    $ docker compose up app
```

NB: At first it might fail to run at first because of the database delaying to start but yu can try the `docker compose up app` like two times

Now you can run the consume the end point

# List off endpoints

|       Name / description       | METHOD | URL                                         |
| :----------------------------: | :----: | ------------------------------------------- |
|          Create User           |  POST  | http://127.0.0.1:8000/auth/create           |
|           User login           |  POST  | http://127.0.0.1:8000/auth/login            |
|          Create Hash           |  POST  | http://127.0.0.1:8000/hash/                 |
|         Get Hash by ID         |  GET   | http://127.0.0.1:8000/hash/<id>             |
|         Get all Hashes         |  GET   | http://127.0.0.1:8000/hash                  |
| Get all Hashes with pagination |  GET   | http://127.0.0.1:8000/hash?limit=1&offset=0 |
| Get Hash by ID and the nearest |  GET   | http://127.0.0.1:8000/hash                  |

- Create user Payload
```
{
    "username": "kagabo",
    "email": "fofo123@gmail.com",
    "password": "dede"
}
```

- User login payload
```
{
    "email": "fofo123@gmail.com",
    "password": "dede"
}
```

- Create Hash payload
```
{
    "hash": [3, 6]
}
```

NB:
- Only Create User and User login does not need a token. You need to get the token by using user login url.
- By default the hash length is 2 but you can change it by editing `HASH_LENGTH` value in `.env` file.  




# Using post man collection to run those listed endpoint

- Import collection in postman the `sample_project.postman_collection.json` file from root directory of the project

# Running test for the project

- you can check running test on [GIT Actions](https://github.com/kagabof/sample_project/actions).

- Running test on locally

Stop the container and remove them

```
    $ docker compose down -v
```

```
    $ docker-compose build test_app
    $ docker compose up test_app ; 
```

NB: At first it might fail to run at first because of the database delaying to start but yu can try the `docker compose up test_app` like two times

# challenge with this solution 

- We set the size of the vector (HASH_LENGTH) in the environment variables and with that it can be hard to change it.
- I check the nearest vector from a given one can only be done with vectors of the same dimensions (shape) and by the time we change the dimension (HASH_LENGTH) of our hash vector it will cause problems