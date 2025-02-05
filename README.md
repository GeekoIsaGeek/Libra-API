# Libra

## A brief guide on how to set up and run this project locally 

1\. First you need to clone this repository:
```sh
git clone git@github.com:Son0fCain/Libra-back.git
```

2\. Then you need to create .env file using this command:
```sh
cp .env.example .env
```
after this, the file will be populated with variables you just need to set values for them

3\. It's important to set up a virtual environment:
```sh
python3 -m venv venv

if you are on windows ->  venv\Scripts\activate
otherwise -> source venv/bin/activate
```

4\. Now as virtual env is already set up you need to install dependencies:
```sh
pip install -r requirements.txt
```

5\. Lastly you should use this command to run a local server:
```sh
flask run
```


