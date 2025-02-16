from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(os.getenv("GOOGLE_SHEET_URL")).sheet1

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_answers = {}

class SurveyStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()

@dp.message_handler(commands=['start'], state='*')
async def start_survey(message: types.Message, state: FSMContext):
    await state.finish()
    user_answers[message.from_user.id] = []
    await message.answer( "Привет! Я — бот клуба «от Мамы к Маме (mom2mom)».\n"
        "Мы создаём пространство для живого общения, вдохновения и поддержки мам.\n"
        "Здесь ты можешь быть самой собой, не жертвуя личной жизнью и творчеством ради материнства.\n\n"
        "Спасибо за твой интерес! Сейчас я задам несколько вопросов, чтобы узнать о твоих предпочтениях "
        "и помочь нам сделать встречи максимально удобными и полезными."
)
    await message.answer("Для начала расскажи, пожалуйста, сколько у тебя детей и какого они возраста? "
                         "Планируешь ли ты брать ребёнка (или детей) с собой на встречи?")
    await SurveyStates.Q1.set()

@dp.message_handler(state=SurveyStates.Q1)
async def handle_q1(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("Какие активности тебе интересны?\n" 
"Например:\n"
                         "• Создание ресурсных свечей\n"
                         "• Плетение ловцов снов или мандал\n"
                         "• Слушание сказок под глюкофон\n"
                         "• Телесные практики (мягкие упражнения, расслабление)\n"
                         "• Лекции, дискуссии, мастермайнды\n"
                         "• Совместная готовка\n"
                         "• Простой формат «прийти и пообщаться»\n\n"
                         "Что из этого тебе ближе? Если у тебя есть другие идеи, обязательно напиши!")
    await SurveyStates.Q2.set()

@dp.message_handler(state=SurveyStates.Q2)
async def handle_q2(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("По стоимости: какую сумму ты считаешь комфортной для одной встречи?\n"
                         "Можешь указать конкретную цифру или примерный диапазон.\n"
                         "Учти, что часть средств идёт на аренду безопасного пространства "
                         "(где можно спокойно находиться с детьми), материалы, чай со вкусняшками.")
    await SurveyStates.Q3.set()

@dp.message_handler(state=SurveyStates.Q3)
async def handle_q3(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("Поделись, пожалуйста, что могло бы тебя остановить от похода на такое мероприятие?")
    await SurveyStates.Q4.set()

@dp.message_handler(state=SurveyStates.Q4)
async def handle_q4(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("А что, наоборот, мотивировало бы тебя прийти?")
    await SurveyStates.Q5.set()

@dp.message_handler(state=SurveyStates.Q5)
async def handle_q5(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("Когда тебе удобнее всего встречаться? А когда ты точно не можешь?")
    await SurveyStates.Q6.set()

@dp.message_handler(state=SurveyStates.Q6)
async def handle_q6(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer(" Есть ли какие-то дополнительные мысли, идеи, пожелания или вопросы по встречам и клубу? Поделись всем, чем посчитаешь нужным!")
    await SurveyStates.Q7.set()

@dp.message_handler(state=SurveyStates.Q7)
async def handle_q7(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    username = message.from_user.username if message.from_user.username else "Нет юзернейма"
    data = [message.from_user.id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] + user_answers[message.from_user.id]
    sheet.append_row(data)
    await message.answer("Спасибо за твои ответы!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
