from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN, PROXY_URL
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from city import lst, cash
import random
from aiogram.dispatcher import FSMContext

bot = Bot(token=TOKEN, proxy=PROXY_URL)
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

        ans = md.bold(data['val'])[-2]
        all_ans = md.bold(data['val'])[1:-1]

        if ans == 'ь' or ans == 'ы':
            ans = md.bold(data['val'])[-3]

        if all_ans in lst[md.bold(data['val'])[1].lower()]:
            if not all_ans in cash:
                num = random.randint(0, len(lst[ans]) - 1)
                cash.append(all_ans)
                cash.append(lst[ans].pop(num))

                await msg.answer(f'{cash[-1]}')
            else:
                await msg.answer('Этот город уже называли')
        else:
            await msg.answer('Или я чего-то не знаю, или же такого города нет')
    else:
        await state.finish()
        await msg.answer('Окей')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
