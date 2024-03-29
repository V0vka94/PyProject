import  logging, datetime
import adminka as adm
from datetime import datetime as dt

import asyncio 
import sys

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

status = 0
nowdate=dt.now()
tdate=dt.now()+datetime.timedelta(days=1)
day=nowdate.strftime('%d')
month=nowdate.strftime('%m')
tday=tdate.strftime('%d')
tmonth=tdate.strftime('%m')
print ('Сегодня ', nowdate.strftime('%d.%m'))
print ('Завтра ', tdate.strftime('%d.%m'))



TOKEN = 'YOUR_API_TOKEN' # это нельзя! писать здесь / you cannot write this here!  
# используй .env файл / use .env file 

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")
    global status, youngs
    if status == 0:
        adm.select_items(day, month)
        await message.answer(str(youngs['name'])+", "+str(youngs['text']) )
    else: await message.answer(f"Сообщение уже отправлено!")

@dp.message(F.text, Command("insert"))
async def any_message(message: Message):
    await message.answer(f"Введите имя:")
    name = message.text
    await message.answer(f"Введите день рождения:")
    bday = message.text
    await message.answer(f"Введите текст поздравления:")
    text = message.text
    adm.insert_item(name, bday, text)
    await message.answer(f"Значения добавлены!\n"+str(youngs))
    
@dp.message(F.text, Command("list"))
async def any_message(message: Message):
    global items
    adm.select_items(day, month)
    await message.answer(f"\n"+str(items))
    adm.select_items(tday,tmonth)
    await message.answer(f"Завтра "+tdate.strftime("%d.%m")+"\n"+str(items))

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        global status, items #youngs 
        if status == 0:
            adm.select_items(day, month)
            
            await message.answer(str(items))
            status = 1
        else: await message.answer(f"Не знаю, что ответить")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer(f"Не знаю, что ответить")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)
    adm.smth()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
