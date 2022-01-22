# telebot-tutorial
__Sandbox for exploring telebot__

[![Python application](https://github.com/NPodlozhniy/telebot-tutorial/actions/workflows/python-app.yml/badge.svg)](https://github.com/NPodlozhniy/telebot-tutorial/actions/workflows/python-app.yml)

1. To start the "My first telegram bot" run the following commands:
```
$ pip install pytelegrambotapi
$ set TOKEN=<YOUR TOKEN>
$ python main.py
```

2. "Second telegram bot" starts on the Heroku by default, but to run locally you should just add one line to the beginning of the code above and modify the launch command:

```
$ pip install flask
$ python main.py --local
```

3. "Third telegram bot" is the first intelligent version of bot with simple authentication through a security question, which, for instance, can send statistics on the main metrics for yesterday. In order to run locally, you need to run a few more commands:

```
$ pip install gspread
$ pip install oauth2client
$ pip install df2gspread
$ set SECRETNAME=<YOUR NAME>
```
