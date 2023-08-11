from aiogram import Bot, Dispatcher, executor, types

from decouple import config

bot = Bot(config('API_TOKEN'))
dp = Dispatcher(bot)

FILE_PHOTO_IDS = "photo_ids.txt"

all_photos = []

def save_photo_ids(photo_id):
    with open(FILE_PHOTO_IDS, "a") as file:
        file.write(photo_id + "\n")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привіт, заватажуй фото і дивись що буде")
    await message.answer("Список команд: /help /get_photo")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("Список команд: /help /get_photo")
    
@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    print(message.from_user.full_name,message.photo[-1].file_id)
    all_photos.append(message.photo[-1].file_id) # Додаємо фото в список
    await message.answer("Фото збережено") # Відповідаємо користувачу

@dp.message_handler(commands=['get_photo'])
async def get_photo(message: types.Message):
    for photo in all_photos[:-6:-1] :
        await message.answer_photo(photo)
    await message.answer("Фото відправлено")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)