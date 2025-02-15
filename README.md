# Libra

REST API for an e-library application, developed as part of the university project. It provides features for managing digital books and user authentication. Built with Flask and Vue.

## A brief guide on how to set up and run this project locally

1\. First you need to clone this repository:

```sh
git clone git@github.com:Son0fCain/Libra-back.git
```

2\. Then you need to add .env file using this command:

```sh
cp .env.example .env
```

After this, the file will be populated with needed variables. You just need to set values

3\. It's important to set up a virtual environment:

```sh
python3 -m venv venv

if you are on windows ->  venv\Scripts\activate
            otherwise ->  source venv/bin/activate
```

If the first command fails on Windows, run python without 3 at the end

4\. Now as virtual env is already set up you need to install dependencies:

```sh
pip install -r requirements.txt
```

5\. After that, run database migrations to set up the initial schema:

```sh
flask db upgrade
```

If migrations are missing, run:

```sh
flask db migrate -m "Initial migration"
flask db upgrade
```

6\. Lastly you should use any of these two commands to run a local server:

```sh
either `flask run` or `python3 app.py`
```
