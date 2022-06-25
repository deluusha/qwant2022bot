import os
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

HEROKU_APP_NAME = "qwant2022"
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Здравствуйте! Напишите сюда свой вопрос или пожелание и он попадет к эксперту! Он ответит Вам в личные сообщения, ожидайте...")
REPLY_TO_THIS_MESSAGE = os.getenv("REPLY_TO_THIS_MESSAGE", "REPLY_TO_THIS")
WRONG_REPLY = os.getenv("Неправильный ответ", "WRONG_REPLY")
TELEGRAM_TOKEN = "5465869926:AAEiXaW1fnzRJggHar6TEBsVL1rhpb-13rk"
TELEGRAM_SUPPORT_CHAT_ID = "-712554152"
PORT = int(os.environ.get('PORT', '8443'))


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Подключен {user_info}.
        """,
    )


import os
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

HEROKU_APP_NAME = "qwant2022"
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Здравствуйте! Напишите сюда свой вопрос или пожелание и он попадет к эксперту! Он ответит Вам в личные сообщения, ожидайте...")
REPLY_TO_THIS_MESSAGE = os.getenv("REPLY_TO_THIS_MESSAGE", "REPLY_TO_THIS")
WRONG_REPLY = os.getenv("Неправильный ответ", "WRONG_REPLY")
TELEGRAM_TOKEN = "5465869926:AAEiXaW1fnzRJggHar6TEBsVL1rhpb-13rk"
TELEGRAM_SUPPORT_CHAT_ID = "-712554152"
PORT = int(os.environ.get('PORT', '8443'))


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Подключен {user_info}.
        """,
    )


def forward_to_chat(update, context):
    """{
        'message_id': 5,
        'date': 1605106546,
        'chat': {'type': 'private', 'Никнейм': 'danokhlopkov', 'Имя': 'Daniil', 'Фамилия': 'Okhlopkov'},
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'Имя': 'Daniil', 'Фамилия': 'Okhlopkov', 'Никнейм': 'danokhlopkov'}
    }"""
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )


def forward_to_user(update, context):
    """{
        'message_id': 10, 'date': 1605106662,
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659,
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True},
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'},
            'forward_date': 1605106658,
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [],
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        },
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False,
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False,
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = None
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
    else:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=WRONG_REPLY
        )


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp


updater = Updater(TELEGRAM_TOKEN)

dp = updater.dispatcher
dp = setup_dispatcher(dp)

if HEROKU_APP_NAME is None:  # pooling mode
    print("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
    print("Note: this is not a great way to deploy the bot in Heroku.")

    updater.start_polling()
    updater.idle()

else:  # webhook mode
    print(f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}"
    )

    updater.idle()
