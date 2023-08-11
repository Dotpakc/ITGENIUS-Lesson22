from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from utils import (save_photo_ids,
                    check_ban, 
                    FILE_PHOTO_IDS,
                    load_data_photo_ids)

bot = Bot(config('API_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
@check_ban
async def start(message: types.Message):
    await message.answer("Привіт, заватажуй фото і дивись що буде")
    await message.answer("Список команд: /help /get_photo /get_photo_group")

@dp.message_handler(commands=['help'])
@check_ban
async def help(message: types.Message):
    await message.answer("Список команд: /help /get_photo")
    
@dp.message_handler(content_types=['photo'])
@check_ban
async def photo_handler(message: types.Message):
    print(message.from_user.id,message.from_user.full_name,message.photo[-1].file_id)
    file_id = message.photo[-1].file_id # Отримуємо id фото
    user_id = message.from_user.id # Отримуємо id користувача
    save_photo_ids(file_id, user_id) # Зберігаємо id фото в файл
    await message.answer("Фото збережено") # Відповідаємо користувачу

@dp.message_handler(commands=['get_photo'])
@check_ban
async def get_photo(message: types.Message):
    all_photos = load_data_photo_ids()
    for photo in all_photos[:-6:-1] :
        user = await bot.get_chat_member(photo["user_id"], photo["user_id"])
        await message.answer_photo(photo["file_id"], caption=f"Відправив: {user.user.full_name}, {photo['date']}")
    await message.answer("Фото відправлено")

#media group
@dp.message_handler(commands=['get_photo_group'])
@check_ban
async def get_photo_group(message: types.Message):
    media = types.MediaGroup()
    all_photos = load_data_photo_ids()  
    for photo in all_photos[:-6:-1] :
        user = await bot.get_chat_member(photo["user_id"], photo["user_id"])
        media.attach_photo(photo["file_id"], caption=f"Відправив: {user.user.full_name}, {photo['date']}")
    await message.answer_media_group(media=media)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)