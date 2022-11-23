import config

from time import time
import aiogram
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.token)
dp = Dispatcher(bot)

# Activate custom filters
dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    me = await bot.get_me()
    #if message.new_chat_participant.id == me.id:
    for chat_member in message.new_chat_members:
        if chat_member.id == me.id and message.chat.id not in config.chat_id:
            await message.answer("Привет!\nЭто группа не находится в списке разрешенных!\nБот будет удален!")
            await bot.leave_chat(chat_id=message.chat.id)
        else:
            await message.delete()


@dp.message_handler(content_types=["any"])
async def give_automute(message: types.Message):
    if message.from_user.id in config.users:
        await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(),
                                           until_date=int(time()) + config.restriction_time * 60
                                           )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
