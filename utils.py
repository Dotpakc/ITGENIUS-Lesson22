import json
from datetime import datetime
from aiogram import types

FILE_PHOTO_IDS = "photo_ids.json" #[{"file_id":"asfas","user_id":123123}]
FILE_BAN_LIST = "ban_list.txt"



def save_photo_ids(photo_id, user_id):
    try:
        with open(FILE_PHOTO_IDS, "r") as file:
            data = json.load(file)
    except:
        data = []
    data.append({"file_id": photo_id, "user_id": user_id, "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
    with open(FILE_PHOTO_IDS, "w") as file:
        json.dump(data, file, indent=4)
    
def load_data_photo_ids():
    try:
        with open(FILE_PHOTO_IDS, "r") as file:
            data = json.load(file)
    except:
        data = []
    return data


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

