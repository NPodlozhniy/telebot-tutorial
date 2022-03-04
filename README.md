# telebot-tutorial

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/NPodlozhniy/telebot-tutorial&env[SECRETNAME]=YOUR+SECRET+CODE&env[TOKEN]=YOUR+TELEGRAM+BOT+TOKEN)

The project is organized in such a way that it consistently improves from a simple echo bot working locally to a complex tool in the hands of a business team for daily monitoring of the required indicators.

[![Python application](https://github.com/NPodlozhniy/telebot-tutorial/actions/workflows/python-app.yml/badge.svg)](https://github.com/NPodlozhniy/telebot-tutorial/actions/workflows/python-app.yml)
![Build Status](https://app.travis-ci.com/NPodlozhniy/telebot-tutorial.svg?token=QqdGuvQuDTwHxcNPfezP&branch=master)
[![Heroku CI Status](https://generate-heroku-badge.herokuapp.com/last.svg)](https://dashboard.heroku.com/pipelines/6fd30bbc-6323-478e-8221-aff8dd2a93d8/tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Contents

1. [Getting started](#Getting-started)
    - [How to get secrets](#How-to-get-secrets)
    - [How to run](#How-to-run)
2. [Early versions](#Early-versions)
    - [Your first telegram bot](#Your-first-telegram-bot)
    - [Second telegram bot](#Second-telegram-bot)
    - [Third telegram bot](#Third-telegram-bot)
3. [See also](#See-also)

## Getting started

The project `@ZelfAlertBot` is a telegram bot, which is part of the analytical infrastructure at [ZELF](https://zelf.co/) and allows the startup team to monitor important business indicators on a daily basis.

### How to get secrets

You just need to create a bot using the `@BotFather` interface, you need to give it a name and save the received token. This value must be set to an environment variable `TOKEN`.
Also you need to specify `SECRETNAME` which is used as login password, you can choose any safe string you like.

### How to run

It is enough to download the latest version of the repository to your local computer, set the `TOKEN` and `SECRETNAME` environment variables, and modify the [stats](https://github.com/NPodlozhniy/telebot-tutorial/blob/master/dataloader.py#:~:text=def%20stats(credentials%2C%20button)%3A) function in [dataloader.py](https://github.com/NPodlozhniy/telebot-tutorial/blob/master/dataloader.py) file accordance with your goals, this function will not work by default.

[:arrow_up:Contents](#Contents)
___
## Early versions

This is the following sandbox for exploring telebot

### Your first telegram bot

To start the `Your first telegram bot` run the following commands:
```
$ pip install pytelegrambotapi
$ set TOKEN=<YOUR TOKEN>
$ python main.py
```
[Browse the repository at this point in the history](https://github.com/NPodlozhniy/telebot-tutorial/tree/65fd22f75f7b0fd6b6476f6ced9b408b1e69ebfc)

[:arrow_up:Contents](#Contents)
___
### Second telegram bot

`Second telegram bot` starts on the Heroku by default, but to run locally you should just add one line to the beginning of the code above and modify the launch command:

```
$ pip install flask
$ python main.py --local
```
[Browse the repository at this point in the history](https://github.com/NPodlozhniy/telebot-tutorial/tree/c350dfa2f0484c2435bf99389d0eaa5c9f919c25)

[:arrow_up:Contents](#Contents)
___
### Third telegram bot

Is the first intelligent version of `@ZelfAlertBot` bot with simple authentication through a security question, which, for instance, can send statistics on the main metrics for yesterday. In order to run locally, you need to run a few more commands:

```
$ pip install gspread
$ pip install oauth2client
$ pip install df2gspread
$ set SECRETNAME=<YOUR NAME>
```
[Browse the repository at this point in the history](https://github.com/NPodlozhniy/telebot-tutorial/tree/ffedf21b202aefdd4784b364d5c98ea6d5c669e2)

[:arrow_up:Contents](#Contents)
___
## See also

1. [PyTelegramBotAPI library source code](https://github.com/eternnoir/pyTelegramBotAPI)
2. [How to add Heroku CI badge](https://github.com/gregsadetsky/heroku-ci-badge)

[:arrow_up:Contents](#Contents)
___
