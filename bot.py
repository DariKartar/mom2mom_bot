from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

API_TOKEN = '7566792283:AAHlJmgc7bph85DjSWVt-fcQ8Bz2JnIwM0U'

# Подключаемся к Google Таблице
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import json
import os
print("GOOGLE_CREDENTIALS:", os.getenv('GOOGLE_CREDENTIALS'))
from dotenv import load_dotenv
load_dotenv()

from dotenv import load_dotenv
load_dotenv()
creds_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Ggyk-V-luAoZZlMoAqFe3erhsnvkKuBIOv2xDk7RGKY/edit?usp=sharing").sheet1

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_answers = {}

@dp.message_handler(commands=['start'])
async def start_survey(message: types.Message):
    user_answers[message.from_user.id] = []
    await message.answer(
        "Привет! Я — бот клуба «от Мамы к Маме (mom2mom)».\n"
        "Мы создаём пространство для живого общения, вдохновения и поддержки мам.\n"
        "Здесь ты можешь быть самой собой, не жертвуя личной жизнью и творчеством ради материнства.\n\n"
        "Спасибо за твой интерес! Сейчас я задам несколько вопросов, чтобы узнать о твоих предпочтениях "
        "и помочь нам сделать встречи максимально удобными и полезными."
    )
    await ask_question_1(message)

async def ask_question_1(message: types.Message):
    await message.answer("1. Для начала расскажи, пожалуйста, сколько у тебя детей и какого они возраста? "
                         "Планируешь ли ты брать ребёнка (или детей) с собой на встречи?")
    dp.register_message_handler(handle_answer_1, state=None)

async def handle_answer_1(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("2. Какие активности тебе интересны? Например:\n"
                         "• Создание ресурсных свечей\n"
                         "• Плетение ловцов снов или мандал\n"
                         "• Слушание сказок под глюкофон\n"
                         "• Телесные практики (мягкие упражнения, расслабление)\n"
                         "• Лекции, дискуссии, мастермайнды\n"
                         "• Совместная готовка\n"
                         "• Простой формат «прийти и пообщаться»\n\n"
                         "Что из этого тебе ближе? Если у тебя есть другие идеи, обязательно напиши!")
    dp.register_message_handler(handle_answer_2, state=None)

async def handle_answer_2(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("3. По стоимости: какую сумму ты считаешь комфортной для одной встречи?\n"
                         "Можешь указать конкретную цифру или примерный диапазон.\n"
                         "Учти, что часть средств идёт на аренду безопасного пространства "
                         "(где можно спокойно находиться с детьми), материалы, чай со вкусняшками.")
    dp.register_message_handler(handle_answer_3, state=None)

async def handle_answer_3(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("4. Поделись, пожалуйста, что могло бы тебя остановить от похода на такое мероприятие?")
    dp.register_message_handler(handle_answer_4, state=None)

async def handle_answer_4(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("5. А что, наоборот, мотивировало бы тебя прийти?")
    dp.register_message_handler(handle_answer_5, state=None)

async def handle_answer_5(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("6. Когда тебе удобнее всего встречаться? А когда ты точно не можешь?\n"
                         "Укажи, пожалуйста, дни и время.")
    dp.register_message_handler(handle_answer_6, state=None)

async def handle_answer_6(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("7. Есть ли какие-то дополнительные мысли, пожелания, вопросы по формату или содержанию встреч?")
    dp.register_message_handler(handle_answer_7, state=None)

async def handle_answer_7(message: types.Message):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("Спасибо большое за твои ответы!\n"
                         "Благодаря им мы сможем сделать наши встречи ещё интереснее и удобнее.\n"
                         "Скоро вернёмся с новостями и датами. Хорошего дня!")

    # Добавляем юзернейм, если он есть
    username = message.from_user.username if message.from_user.username else "Нет юзернейма"

    # Сохраняем ответы в Google Таблицу
    data = [message.from_user.id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + user_answers[message.from_user.id]
    sheet.append_row(data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
