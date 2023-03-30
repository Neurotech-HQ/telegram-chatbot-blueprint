<samp>

# telegram-chatbot-blueprint

A blueprint for deploying telegram bots made using [Sarufi](https://docs.sarufi.io/)

## GETTING READY

- Create Project directory

  Create a project directory `Telegram bot`. In this directory we are going to create a virtual environment to hold our package.

  ```bash
  mkdir 'Telegram bot'
  cd 'Telegram bot'

  ```

- Make virtual environment and install requirements

  Using virtual environment is a good practice, so we are going to create one. You can read more on [why use virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). We install sarufi and dotenv which is used to laod envirnoment variables.

  ```bash
  python3 -m venv sarufi
  source sarufi/bin/activate
  pip3 install --upgrade sarufi
  pip3 install python-dotenv
  ```

We have the package required to get started

## CONFIGURATION

In this part, we are going to clone the [Sarufi Telegram Chatbot deployment Blueprint](https://github.com/Neurotech-HQ/telegram-chatbot-blueprint.git). Run

```bash
git clone https://github.com/Neurotech-HQ/telegram-chatbot-blueprint.git
cd telegram-chatbot-blueprint
```

We need to configure our credentials. Navigate into `telegram-chatbot-blueprint` folder to create a file to hold environment variables, `.env`

```bash
touch .env
```

In the file we are going to add the following credetials. You can do it in the terminal or open `.env` then add the following:-

- In the terminal

  ```bash
  echo "sarufi_username= Your sarfi username" >>.env &
  echo "sarufi_password = Your sarufi password" >> .env &
  echo "sarufi_bot_id= bot id" >> .env & 
  echo "token = telegram token" >>.env &
  echo "start_message= Hi {name}, Welcome To {bot_name}, How can i help you" >> .env
  ```
    
- Open `.env` file in text editor

  ```text
  sarufi_username= Your sarfi username
  sarufi_password = Your sarufi password
  sarufi_bot_id= bot id
  token = telegram token
  start_message= Hi {name}, Welcome To Your bot name. How can i help you
  ```

## LAUNCH

Its the time you have been waiting for. Lets lauch 🚀 our bot.

```python
python3 app.py
```

Open your telegram app, search for your bot --> Send it a text.

## Issues

If you will face any issue, please raise one so as we can fix it as soon as possible

## Contribution

If there is something you would like to contribute, from typos to code to documentation, feel free to do so, `JUST FORK IT`.

## Credits

All the credits to

1. [kalebu](https://github.com/Kalebu/)
2. [Jovine](https://github.com/jovyinny)
3. All other contributors

</samp>
