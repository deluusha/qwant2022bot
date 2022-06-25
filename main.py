import support
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # отслеживание сообщений от пользователя
from aiogram.utils import executor
import markups as nav

TOKEN = '5465869926:AAEiXaW1fnzRJggHar6TEBsVL1rhpb-13rk'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])  # обозачает событие в чате, команда через /
async def command_start(message: types.Message):  # асинхронность
    await bot.send_message(message.from_user.id, "Hi {0.first_name}".format(message.from_user),
                           reply_markup=nav.mainMenu)  # на команду появляется меню


@dp.message_handler()
async def bot_message(message: types.Message):
    # await bot.send_message(message.from_user.id, message.text)
    if message.text == 'Рандомное число':
        await bot.send_message(message.from_user.id, 'алалала ' + str(1))

    elif message.text == 'Main menu':
        await bot.send_message(message.from_user.id, 'Другое ', reply_markup=nav.mainMenu)

    elif message.text == 'Main menu':
        await bot.send_message(message.from_user.id, 'Другое ', reply_markup=nav.mainMenu)

    elif message.text == 'Main menu':
        await bot.send_message(message.from_user.id, 'Другое ', reply_markup=nav.mainMenu)

    elif message.text == 'Другое':
        await bot.send_message(message.from_user.id, 'Другое ', reply_markup=nav.otherMenu)

#  if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)  # сообщения оффлайн игнорируются
