import telebot
from confic import token, api_key, secret_key, api_url
from logic import Text2ImageAPI
import os 

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для генерации изображений по текстовым запросам.\n"
        "Доступные команды:\n"
        "/start или /help - Показать это сообщение\n"
        "/gen <текст> - Сгенерировать изображение на основе описания"
    )


@bot.message_handler(commands=["gen"])
def gen(message):
    bot.send_chat_action(message.chat.id, "typing")  
    loading_message = bot.send_message(message.chat.id, "Генерирую картинку...")

    try:
        if len(message.text.split()) > 1:
            api = Text2ImageAPI(api_url, api_key, secret_key)
            model_id = api.get_model()
            prompt = ' '.join(message.text.split()[1:])
            uuid = api.generate(prompt, model_id)
            images = api.check_generation(uuid)
            api.decode(images[0])
            get_img(message)
        else:
            bot.send_message(message.chat.id, "Вы не указали промт для генерации.")
    finally:
        bot.delete_message(message.chat.id, loading_message.message_id)  


def get_img(message):
    img_path = "decoded_image.png"
    with open(img_path, "rb") as img:
        bot.send_photo(message.chat.id, img)
    os.remove(img_path)  


if __name__ == "__main__":
    bot.polling(non_stop=True)
