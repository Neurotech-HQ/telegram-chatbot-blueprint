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

  Using virtual environment is a good practice, so we are going to create one. You can read more on [why use virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). We shall install all necessary packages in the environment

  ```bash
  python3 -m venv sarufi
  source sarufi/bin/activate
  ```

## CONFIGURATION

In this part, we are going to clone the [Sarufi Telegram Chatbot deployment Blueprint](https://github.com/Neurotech-HQ/telegram-chatbot-blueprint.git) and install the packages. Run

```bash
git clone https://github.com/Neurotech-HQ/telegram-chatbot-blueprint.git
cd telegram-chatbot-blueprint
pip3 install -r requirements.txt
```

After installing packages, we need to configure our credentials. In `telegram-chatbot-blueprint`, create a file(`.env`) to hold environment variables.

In `.env`, we are going to add the following credetials. Using your favourite text editor add the following:-

```text
sarufi_username= Your sarfi username
sarufi_password = Your sarufi password
sarufi_bot_id= bot id
token = telegram token
start_message= Hi {name}, Welcome To {bot_name}, How can i help you
```

## LAUNCH

Its the time you have been waiting for. Lets lauch 🚀 our bot.

```python
python3 app.py
```

Open your telegram app, search for your bot --> Send it a text.

**NOTE:** All operations are done in activated virtual environment for convience

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
