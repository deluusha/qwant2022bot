import support
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # отслеживание сообщений от пользователя
from aiogram.utils import executor
import markups as nav

TOKEN = '5465869926:AAEiXaW1fnzRJggHar6TEBsVL1rhpb-13rk'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


                           # на команду появляется меню


@dp.message_handler()
async def bot_message(message: types.Message):


#  if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)  # сообщения оффлайн игнорируются
