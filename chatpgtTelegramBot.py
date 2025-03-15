import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def ChatGPT():
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    openai_key = os.getenv("OPENAI_KEY")
    chatgpt_career = os.getenv("CHATPGT_CAREER")

    bot = telebot.TeleBot(telegram_token, parse_mode=None)
    url = "https://api.openai.com/v1/chat/completions"


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "سلام چطوری میتونم کمکت کنم؟")


    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system",
                "content": f"{chatgpt_career}"
                },
                {"role": "user", "content": message.text}
            ]
        }

        response = requests.post(url, headers=headers, json=data).json()

        if response.status_code != 200:
            bot.reply_to(message, "مشکلی در ارتباط با سرور OpenAI به وجود آمده. لطفاً بعداً امتحان کنید.")
            return

        json_response = response.json()
        if 'choices' not in json_response:
            bot.reply_to(message, "خطایی در دریافت پاسخ از OpenAI رخ داده است.")
            return

        assistant_message = response['choices'][0]['message']['content']
        bot.reply_to(message, assistant_message)

    bot.infinity_polling()


def DeepSeek():
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    chatgpt_career = os.getenv("CHATPGT_CAREER")
    bot = telebot.TeleBot(telegram_token, parse_mode=None)
    ollama_url = "http://localhost:11434/api/generate"  # آدرس API لوکال Ollama
    model_name = "deepseek-r1:8b"  # مدل موردنظر در Ollama

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "سلام! من ربات تلگرام هستم که با Ollama کار می‌کنم. سوالت رو بپرس!")

    @bot.message_handler(func=lambda m: True)
    def chat_with_ollama(message):
        data = {
            "model": model_name,
            "prompt": f"""
                {chatgpt_career}
                
                سوال کاربر: {message.text}
                """,
            "stream": False  # غیرفعال کردن استریم برای دریافت پاسخ یکجا
        }

        # data = {
        #     "model":model_name,  # یا هر مدل دیگر که استفاده می‌کنید
        #     "messages": [
        #         {"role": "system", "content": chatgpt_career},
        #         {"role": "user", "content": message.text}
        #     ]
        # }

        try:
            response = requests.post(ollama_url, json=data).json()
            assistant_message = response.get("response", "خطایی رخ داد، دوباره امتحان کن.")
        except Exception as e:
            assistant_message = f"خطا در ارتباط با Ollama: {str(e)}"

        bot.reply_to(message, assistant_message)

    bot.infinity_polling()



if(__name__ == '__main__'):
    DeepSeek()