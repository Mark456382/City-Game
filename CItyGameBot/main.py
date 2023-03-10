from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from city import lst, cash
import random
from aiogram.dispatcher import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class User(StatesGroup):
    val = State()


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer(f"Hello, {msg.from_user.full_name}")


@dp.message_handler(commands=['city_game'])
async def game(msg: types.Message):
    await User.val.set()
    await msg.answer('Введите город')


@dp.message_handler(state=User.val)
async def game_(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['val'] = msg.text
    if md.bold(data['val']) != '*Хватит*':
        try:
            ans = md.bold(data['val'])[-2]

            if ans == 'ь':
                ans = md.bold(data['val'])[-3]

            otv = random.choice(lst[ans])
            cash.append(otv)
            await msg.answer(f'{cash[-1]}')
        except KeyError:
            await msg.answer('Нет городов на такую букву')
    else:
        await state.finish()
        await msg.answer('Окей')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
