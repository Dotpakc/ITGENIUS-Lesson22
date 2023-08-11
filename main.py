from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from utils import save_photo_ids, load_data, check_ban , FILE_PHOTO_IDS

bot = Bot(config('API_TOKEN'))
dp = Dispatcher(bot)

all_photos = load_data(FILE_PHOTO_IDS) # Завантажуємо id фото з файлу

@dp.message_handler(commands=['start'])
@check_ban
async def start(message: types.Message):
    await message.answer("Привіт, заватажуй фото і дивись що буде")
    await message.answer("Список команд: /help /get_photo")

@dp.message_handler(commands=['help'])
@check_ban
async def help(message: types.Message):
    await message.answer("Список команд: /help /get_photo")
    
@dp.message_handler(content_types=['photo'])
@check_ban
async def photo_handler(message: types.Message):
    print(message.from_user.id,message.from_user.full_name,message.photo[-1].file_id)
    all_photos.append(message.photo[-1].file_id) # Додаємо фото в список
    save_photo_ids(message.photo[-1].file_id) # Зберігаємо id фото в файл
    await message.answer("Фото збережено") # Відповідаємо користувачу

@dp.message_handler(commands=['get_photo'])
@check_ban
async def get_photo(message: types.Message):
    for photo in all_photos[:-6:-1] :
        await message.answer_photo(photo)
    await message.answer("Фото відправлено")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)