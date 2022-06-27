import os
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

HEROKU_APP_NAME = "qwant2022"
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "Здравствуйте! Напишите сюда свой вопрос или пожелание и он попадет к "
                                               "эксперту! Ваш вопрос должен быть ясным. Опишите свою проблему и какую "
                                               "помощь Вы хотите получить. Так нам легче помогать "
                                               "пользователям.\nЭксперт ответит Вам в личные сообщения, ожидайте...") 
REPLY_TO_THIS_MESSAGE = os.getenv("REPLY_TO_THIS_MESSAGE", "REPLY_TO_THIS")
WRONG_REPLY = os.getenv("WRONG REPLY", "WRONG_REPLY")
TELEGRAM_TOKEN = "5465869926:AAEiXaW1fnzRJggHar6TEBsVL1rhpb-13rk"
TELEGRAM_SUPPORT_CHAT_ID = "-712554152"
PORT = int(os.environ.get('PORT', '8443'))


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)
    user_name = str(update.message.from_user.first_name)
    user_username = str(update.message.from_user.username)
    user_lang = str(update.message.from_user.language_code)
    user_id = str(update.message.from_user.id)
    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Подключен новый клиент.
Имя: {user_name}.
Username: @{user_username}
Язык: {user_lang}
id клиента: {user_id}
        """,
    )


def forward_to_chat(update, context):

    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )


def forward_to_user(update, context):

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

    
    
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # отслеживание сообщений от пользователя
from aiogram.utils import executor
import markups as nav
import information

TOKEN = '5465375647:AAEPTkq8lk1s4GOFwR5fiwBeuXOUBDob644'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])  # обозачает событие в чате, команда через /
async def command_start(message: types.Message):  # асинхронность
    await bot.send_message(message.from_user.id, "Здравствуйте, {0.first_name}!".format(message.from_user),
                           reply_markup=nav.mainMenu)  # на команду появляется меню


@dp.message_handler()
async def bot_message(message: types.Message):
    # await bot.send_message(message.from_user.id, message.text)

    if message.text == 'Кто мы?':
        photo = open('icon.jpeg', 'rb')
        text = '*Special Care* - организация, которая помогает родителям детей с ограниченными ' \
               'возможностями.\n\n\nС нашей помощью родители смогут узнать о _правильном воспитании, ' \
               'поддержке и развитии своего ребёнка._\n\n\nДля нас важно, чтобы каждый особый ребенок ' \
               'получил *должностный уход* и *заслуживаемую любовь.*\n\nИменно поэтому мы *не требуем ' \
               'никакой платы* за наши услуги и наши ресурсы доступны для *каждого!*\n\n\n*Помогаем ' \
               'сделать этот мир лучше! ✨*'
        await bot.send_photo(message.from_user.id, photo, caption=text, parse_mode="Markdown")
    if message.text == 'Консультация с экспертом':
        await bot.send_message(message.from_user.id,
                               'Для связи с экспертом Вам достаточно написать этому боту @QWANT2022bot и ваш запрос '
                               'попадет к профессионалам!')
    if message.text == 'Обратная связь':
        await bot.send_message(message.from_user.id, 'Переходим в меню обратной связи...', reply_markup=nav.otherMenu)
    if message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, 'Переходим в главное меню...', reply_markup=nav.mainMenu)

    if message.text == 'Оставьте нам отзыв':
        await bot.send_message(message.from_user.id, "Оставьте этому боту @QWANT2022bot свой отзыв")
    elif message.text == 'Поддержите нас!':
        await bot.send_message(message.from_user.id, "Вы можете поддержать нас! \nКаспи: +123456789")

    if message.text == 'Опрос':
        await bot.send_message(message.from_user.id,
                               'Этот опрос поможет лучше понять Ваши предпочтения и дать Вам наилучшие рекомендации. '
                               '\nКакие возможности ограничены у Вашего ребенка?',
                               reply_markup=nav.Quiz)

    if message.text == 'Нарушение слуха':
        await bot.send_message(message.from_user.id, 'Какая у ребенка степень инвалидности?', reply_markup=nav.Quiz1)

    if message.text == 'Совершенно глухой':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?', reply_markup=nav.Quiz11)
    if message.text == 'На ментальном здоровье глухого ребенка':
        await bot.send_message(message.from_user.id, information.text111, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии глухого ребенка':
        await bot.send_message(message.from_user.id, information.text112, reply_markup=nav.mainMenu)

    if message.text == 'Слабослышащий':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?', reply_markup=nav.Quiz12)
    if message.text == 'На ментальном здоровье слабослышащего ребенка':
        await bot.send_message(message.from_user.id, information.text121, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии слабослышащего ребенка':
        await bot.send_message(message.from_user.id, information.text122, reply_markup=nav.mainMenu)

    if message.text == 'Нарушение зрения':
        await bot.send_message(message.from_user.id, 'Какая у ребенка степень инвалидности?', reply_markup=nav.Quiz2)

    if message.text == 'Совершенно слепой':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?', reply_markup=nav.Quiz21)
    if message.text == 'На ментальном здоровье слепого ребенка':
        await bot.send_message(message.from_user.id, information.text211, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии слепого ребенка':
        await bot.send_message(message.from_user.id, information.text212, reply_markup=nav.mainMenu)

    if message.text == 'Слабовидящий':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz12)
    if message.text == 'На ментальном здоровье слабовидящего ребенка':
        await bot.send_message(message.from_user.id, information.text221, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии слабовидящего ребенка':
        await bot.send_message(message.from_user.id, information.text222, reply_markup=nav.mainMenu)

    if message.text == 'Нарушение речи':
        await bot.send_message(message.from_user.id, 'Какая у ребенка степень инвалидности?',
                               reply_markup=nav.Quiz3)

    if message.text == 'Совершенно немой':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz31)
    if message.text == 'На ментальном здоровье немого ребенка':
        await bot.send_message(message.from_user.id, information.text311, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии немого ребенка':
        await bot.send_message(message.from_user.id, information.text312, reply_markup=nav.mainMenu)

    if message.text == 'Плохо говорит, но может':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?', reply_markup=nav.Quiz32)
    if message.text == 'На ментальном здоровье плохоговорящего ребенка':
        await bot.send_message(message.from_user.id, information.text321, reply_markup=nav.mainMenu)
    elif message.text == 'На умственном развитии плохоговорящего ребенка':
        await bot.send_message(message.from_user.id, information.text322, reply_markup=nav.mainMenu)

    if message.text == 'Нарушение опорно-двигательного аппарата':
        await bot.send_message(message.from_user.id, 'Какая у ребенка степень инвалидности?',
                               reply_markup=nav.Quiz4)

    if message.text == 'Совершенно не способен ходить':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz41)
    if message.text == 'На ментальном здоровье ребенка с НОДА':
        await bot.send_message(message.from_user.id, information.text411, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии ребенка с НОДА':
        await bot.send_message(message.from_user.id, information.text412, reply_markup=nav.mainMenu)

    if message.text == 'Может, но плохо':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz42)
    if message.text == 'На ментальном здоровье ребенка с слабым НОДА':
        await bot.send_message(message.from_user.id, information.text421, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии ребенка с слабым НОДА':
        await bot.send_message(message.from_user.id, information.text422, reply_markup=nav.mainMenu)

    if message.text == 'Умственная отсталость':
        await bot.send_message(message.from_user.id, 'Какая у ребенка степень инвалидности?',
                               reply_markup=nav.Quiz5)

    if message.text == 'Совершенно умственно отсталый':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz51)
    if message.text == 'На ментальном здоровье умственно отсталого ребенка':
        await bot.send_message(message.from_user.id, information.text511, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии умственно отсталого ребенка':
        await bot.send_message(message.from_user.id, information.text512, reply_markup=nav.mainMenu)

    if message.text == 'Отсталый, но не сильно':
        await bot.send_message(message.from_user.id, 'На чем вы бы хотели сосредоточиться?',
                               reply_markup=nav.Quiz52)
    if message.text == 'На ментальном здоровье не сильно умственно отсталого ребенка':
        await bot.send_message(message.from_user.id, information.text521, reply_markup=nav.mainMenu)
    if message.text == 'На умственном развитии не сильно умственно отсталого ребенка':
        await bot.send_message(message.from_user.id, information.text522, reply_markup=nav.mainMenu)


if __name__ == '__main__':   
   executor.start_polling(dp, skip_updates=True)  # сообщения оффлайн игнорируются
