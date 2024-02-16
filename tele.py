import json
import datetime
from telegram.ext import ContextTypes, Application
from scrape import get_papers


with open("config.json") as f:
    token = json.load(f)['token']

async def callback_daily(context: ContextTypes.DEFAULT_TYPE):
    url = "https://arxiv.org"
    topic = "/list/cs.LG/recent"
    for paper in get_papers(url, topic):
        await context.bot.send_message(chat_id='186940643', text=paper)

application = Application.builder().token(token).build()
job_queue = application.job_queue

job_minute = job_queue.run_repeating(callback_daily, interval=10, first=10)

# job_daily = job_queue.run_daily(callback_daily, time=datetime.time(hour=0), days=(0,1,2,3,4))

application.run_polling()