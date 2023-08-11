from aiogram import types

FILE_PHOTO_IDS = "photo_ids.txt"
FILE_BAN_LIST = "ban_list.txt"



def save_photo_ids(photo_id):
    with open(FILE_PHOTO_IDS, "a") as file:
        file.write(photo_id + "\n")


def load_data(file):
    with open(file) as file:
        data = file.read().split("\n")
    return data


#декоратор для перевірки чи є користувач в бан листі
def check_ban(func):
    async def wrapper(message: types.Message):
        ban_list = load_data(FILE_BAN_LIST)
        if str(message.from_user.id) in ban_list:
            await message.answer("Ви забанені")
            return
        await func(message)
    return wrapper

