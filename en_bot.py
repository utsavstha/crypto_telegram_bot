#!/usr/bin/env python

import logging
import requests
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply, ReplyKeyboardMarkup

from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
CHECK_THIS_OUT = "check-this-out"
USING_ENTITIES = "using-entities-here"
USING_KEYBOARD = "using-keyboard-here"
SO_COOL = "so-cool"
KEYBOARD_CALLBACKDATA = "keyboard-callback-data"
WELCOME_TEXT = "Hello! I am the Artificial Intelligence System of ⚡ENERGY GO PLUS⚡"
BASE_URL = 'http://vps91640.inmotionhosting.com:8001/api/'
FILE_BASE_URL = 'http://vps91640.inmotionhosting.com:8001'
BOT_LANGUAGE = "en"
TOKEN = "6200167918:AAGqgl9XylwPEhayNW8is-b3EsVcnWYHmNg"


def get_data(url):
    url = f"{BASE_URL}{url}"
    response = requests.request(
        "GET", url)

    return response.json()


def post_data(url, first_name, last_name, language_code, telegram_id, registration_link):
    url = f"{BASE_URL}{url}"
    myobj = {
        'first_name': first_name,
        'last_name': last_name,
        'language_code': language_code,
        'telegram_id': telegram_id,
        'registration_link': registration_link,
    }

    response = requests.post(url, json=myobj)

    return (response.status_code, response.json())


def get_register_link(url, telegram_id):
    url = f"{BASE_URL}{url}"
    myobj = {

        'bot_language': BOT_LANGUAGE,
        'telegram_id': telegram_id,
    }

    response = requests.post(url, json=myobj)

    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print(user)
    url = f'botuser/'

    if len(context.args) > 0:
        code, response = post_data(url, user.first_name, user.last_name,
                                   user.language_code, user.id, context.args[0])
        # print(response)
        if code == 201:
            # print(context.args)
            url = f"leads/{context.args[0]}"
            welcome_message = ''

            response = get_data(url)
            welcome_message = response['full_name_seller'] + '\n'
            welcome_message += response['seller_whatsapp_number'] + '\n'
            welcome_message += response['seller_referral_link'] + '\n'
            keyboard = [
                [InlineKeyboardButton(
                    "I WANT TO MULTIPLY MY CAPITAL", callback_data="0")],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        else:
            await welcome(update)
    else:
        await welcome(update)
        # welcome_message += 'Please provide your Email Address to continue' + '\n'
        # await update.message.reply_html(
        #     welcome_message,
        #     reply_markup=ForceReply(selective=True),
        # )
        # url = f'welcome/{BOT_LANGUAGE}'
        # response = get_data(url)
        # keyboard = [
        #     [InlineKeyboardButton(
        #         response['continue_to_main_menu'], callback_data="continue_to_main_menu")],
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # file = open('files/intro.mp4', 'rb')
        # await update.message.reply_video(file)
        # await update.message.reply_text(text=response['content'], reply_markup=reply_markup)
        # await update.answer()


async def welcome(query):
    url = f'welcome/{BOT_LANGUAGE}'
    response = get_data(url)
    keyboard = [
        [InlineKeyboardButton(
            response['continue_to_main_menu'], callback_data="continue_to_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    file = open('files/en_intro.mp4', 'rb')
    await query.message.reply_video(file)
    await query.message.reply_text(text=response['content'], reply_markup=reply_markup)
    # await query.answer()


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    if query.data == "0":
        await welcome(query)
    elif query.data == "continue_to_main_menu":
        url = f'mainmenu/{BOT_LANGUAGE}'
        response = get_data(url)
        keyboard = [

            [InlineKeyboardButton(
                response["presentation_pdf"], callback_data="presentation_pdf")],
            [InlineKeyboardButton(
                response["presentation_videos"], callback_data="presentation_videos")],
            [InlineKeyboardButton(response["register"],
                                  callback_data="register")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text=response['content'], reply_markup=reply_markup)
        # await query.answer()

    elif query.data == "presentation_pdf":
        url = f'presentationMenu/{BOT_LANGUAGE}'
        response = get_data(url)
        keyboard = [

            [InlineKeyboardButton(
                response["register"], callback_data="register")],
            [InlineKeyboardButton(
                response["more_info"], callback_data="presentation_videos")],
            [InlineKeyboardButton(response["main_menu"],
                                  callback_data="continue_to_main_menu")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        file = open('files/en_energy.pdf', 'rb')
        await query.message.reply_document(file)
        await query.message.reply_text(text=response['content'], reply_markup=reply_markup)
    elif query.data == "presentation_videos":
        url = f'videoMenu/{BOT_LANGUAGE}'
        response = get_data(url)
        keyboard = []
        for index, menu in enumerate(response['VideoMenu']):
            keyboard.append([InlineKeyboardButton(
                response['VideoMenu'][index]['content'], url=response['VideoMenu'][index]['url'])])
        keyboard.append([InlineKeyboardButton(
            response["register"], callback_data="register")])
        keyboard.append([InlineKeyboardButton(
            response["main_menu"], callback_data="continue_to_main_menu")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(text=response['content'], reply_markup=reply_markup)
    elif query.data == "register":
        url = f'register/'
        print(user.id)
        response = get_register_link(url, user.id)

        keyboard = [
            [InlineKeyboardButton(response['register_data']["main_menu"],
                                  callback_data="continue_to_main_menu")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        content = response['register_data']['content'].replace(
            "{link}", response["lead"]["seller_referral_link"])
        await query.message.reply_text(text=content, reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
