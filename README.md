# Auto Telegram nickname checker
Automated Telegram nickname register ability checker. Works as userbot. 

## Prerequisite
A Telegram account with *api_id* and *api_hash*. Visit https://my.telegram.org/apps and fill out the forms.

## Installation 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## How-to
* Fill out the form on the link mentioned above
* Create a configuration .env
```
touch .env
```
* Add your API_HASH and API_ID

```
API_ID = YOUR_TELEGRAM_API_ID
API_HASH = YOUR_TELEGRAM_API_HASH
```

* Run
```
python3 main.py
```

* Specify your phone in the console. It will send an authentication code. Put it back into console.

Enjoy!