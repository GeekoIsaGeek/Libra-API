# Libra

This repository has been created for the backend app of **Libra** which is going to be the yet another E-library app built using Flask and [Vue](https://github.com/GeekoIsaGeek/libra-front).

## A brief guide on how to set up and run this project locally

1\. First you need to clone this repository:

```sh
git clone git@github.com:Son0fCain/Libra-back.git
```

2\. Then you need to create .env file using this command:

```sh
cp .env.example .env
```

After this, the file will be populated with variables. You just need to set values

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

5\. Lastly you should use any of these two commands to run a local server:

```sh
either `flask run` or `python3 app.py`
```
