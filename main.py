import logging
import logging
import re
import asyncio
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
logging.basicConfig(level=logging.INFO)
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:tgrMDkXkTiT08mcO@cluster0.ik8yi.mongodb.net/Sunami?retryWrites=true&w=majority")
db = client.database
nasafcl = db.nasafcl
addusers = db.addusers





API_TOKEN = '1104132630:AAGWf0bCt9qF4aUXVsYfd8_nxRU3XgQfM3k'
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    lang = State()
    obl = State()
    category = State()
    gender = State()
    gender2 = State()
    gender3 = State()
    gender4 = State()



@dp.message_handler(commands='start')
@dp.message_handler(state='*', commands='start')
async def cmd_start(message: types.Message):
       print(message)
       await  message.answer('Assalomu aleykum 🙂')

@dp.message_handler(content_types=['new_chat_members'])
async def schet(message: types.Message):
       if str(message.chat.id) == str(-1001438737022):
            print(message)
            ncm = addusers.find_one_and_update({'userid': message.from_user.id}, {
                '$set': {'userid': message.from_user.id, 'name': message.from_user.full_name}},
                                      upsert=True)
            try:
                added = int(ncm['added'])+int(len(message.new_chat_members))
                print(added)
                print('a1')
            except:
                added = int(len(message.new_chat_members))
                print(added)
                print('b2')
            print(added)
            ncm = addusers.find_one_and_update({'userid': message.from_user.id}, {
                '$set': {'added': added, 'p': 0}},
                                               upsert=True)
async def scheduleded(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        try:
            kon = addusers.find_one_and_update({'p': 0}, {
                '$set': {'p': 1}})
            if kon == None:
                continue
            try:
                print('111')
                msg = await bot.send_message(chat_id=-1001246127898, text='<a href="tg://user?id='+str(kon['userid'])+'">'+str(kon['name'])+'</a> (<code>'+str(kon['userid'])+'</code>) -  ' + str(kon['added']) , parse_mode=ParseMode.HTML)
                print('222')
                addusers.find_one_and_update({'userid': int(kon['userid'])}, {'$set': {'messageid': msg.message_id}})
                print('333')
                await bot.delete_message(chat_id=-1001246127898, message_id=int(kon['messageid']))
                print('444')

            except:
                print('555')
        except:
            a=1
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduleded(5))
    executor.start_polling(dp, skip_updates=True)