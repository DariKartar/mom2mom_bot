
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
    await message.answer(
        "Привет! Я — бот клуба «от Мамы к Маме (mom2mom)».
"
        "Спасибо за твой интерес! Сейчас я задам несколько вопросов."
    )
    await message.answer("1. Сколько у тебя детей и какого они возраста? Планируешь ли ты брать ребёнка с собой?")
    await SurveyStates.Q1.set()

@dp.message_handler(state=SurveyStates.Q1)
async def handle_q1(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("2. Какие активности тебе интересны?")
    await SurveyStates.Q2.set()

@dp.message_handler(state=SurveyStates.Q2)
async def handle_q2(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("3. Какую сумму ты считаешь комфортной для одной встречи?")
    await SurveyStates.Q3.set()

@dp.message_handler(state=SurveyStates.Q3)
async def handle_q3(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("4. Что могло бы тебя остановить от похода на мероприятие?")
    await SurveyStates.Q4.set()

@dp.message_handler(state=SurveyStates.Q4)
async def handle_q4(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("5. Что мотивировало бы тебя прийти?")
    await SurveyStates.Q5.set()

@dp.message_handler(state=SurveyStates.Q5)
async def handle_q5(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("6. Когда тебе удобнее всего встречаться?")
    await SurveyStates.Q6.set()

@dp.message_handler(state=SurveyStates.Q6)
async def handle_q6(message: types.Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text)
    await message.answer("7. Есть ли пожелания, вопросы по формату встреч?")
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
