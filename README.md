<samp>

# telegram-chatbot-blueprint

A blueprint for deploying telegram bots

## Requirements

Make sure you have ]sarufi package](<https://github.com/Neurotech-HQ/sarufi-python-sdk>) installed on your machine before launching your telegram bot, you can easily install by the following command;

```bash
git clone https://github.com/Neurotech-HQ/sarufi-python-sdk
cd sarufi-python-sdk
sarufi-python-sdk $ python setup.py install
```

## YAML CONFIGURATION

Configure yaml to resemble your project details and telegram keys

```YAML
sarufi:
  username: kalebu@neurotech.africa #Your user name
  password: 123 #Your password
  project:
    id: 3 # Project ID here

telegram:
  token: 5539985581:AAGwHSY4Phn3ORD7Xac8sNDj-eHlam8wvA8 # Telegram token
  start_message: |
    Hi {name}, I can help you with ABC
```

## LAUNCH

Once you have configured your YAML file, now you are ready to launch your telegram bot.

```bash
python3 app.py
```

## Issues

If you will face any issue, please raise one so as we can fix it as soon as possible

## Contribution

If there is something you would like to contribute, from typos to code to documentation, feel free to do so, ```JUST FORK IT```.

## Credits

All the credits to

1. [kalebu](https://github.com/Kalebu/)
2. All other contributors

</samp>
