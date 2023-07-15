import telebot
import random
import os
import mc
from telebot import types
from mc import *
from mc.builtin import validators
from Config import TokenGabrielTG, DefaultGenChanceTG
import datetime

bot = telebot.TeleBot(TokenGabrielTG)
print("Bot started!")

def generate():
    with open("GabrielDropoutDataBase.txt", encoding='utf8') as file:
      txt = file.read().split('·')
      generated_text = PhraseGenerator(samples=txt).generate_phrase()
      return generated_text
    
def ale():
    c = generate()
    b = generate()
    ra = random.randint(1,2)
    if ra == 2:
      return c+" "+b
    else:
      ran = random.randint(1,2)
      if ran == 1:
          return c
      else:
          return b

@bot.message_handler(commands=['chance'])
def chance_func(message):
  if not os.path.exists(f"config/{message.chat.id}.txt"):
    with open(f"config/{message.chat.id}.txt", "w") as create_new_cfg:
      create_new_cfg.write(f"{DefaultGenChanceTG}")
      bot.send_message(message.chat.id, "*Чат добавлен в базу данных*")

  if " " in message.text:
    count = message.text.split(maxsplit=1)[1]
    try:
      int(count)
    except:
      bot.reply_to(message, "Цифры блядь нужны, а не та хуета что ты дал.")
      return 0
    else:
      count = int(count)
    count_before = open(f"config/{message.chat.id}.txt").read()
    if count == count_before:
      if count == 0:
        bot.reply_to(message, "Понос и так уже выключен")
        return 0
      else:
        bot.reply_to(message, f"У тебя и так уже стоит шанс {chance}")
    elif count > -1 and count < 101:
      if count == 0:
        bot.reply_to(message, "Понос выключен")
        with open(f"config/{message.chat.id}.txt", "w") as write_cfg:
          write_cfg.write(f"0")
      else:
        bot.reply_to(message, f"Понос установлен на {count}%")
        with open(f"config/{message.chat.id}.txt", "w") as write_cfg:
          write_cfg.write(f"{count}")
    else:
      bot.reply_to(message, "Твоё дерьмо выходит за все рамки ограничений (0-100)")
  else:
    count = open(f"config/{message.chat.id}.txt").read()
    bot.reply_to(message, f"Шанс в этом говночате составляет {count}%")



@bot.message_handler(commands=['start'])
def start_func(message):
  bot.send_message(message.chat.id, "Привет, я Габриель! Я могу генерировать рандомную хуйню на основе ваших сообщений!")



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "твиттер":
      bot.send_message(message.chat.id, "нигер")
    else:
      with open("GabrielDropoutDataBase.txt", 'a', encoding='utf8') as bfile:
        bfile.write((str(message.text).replace('·', '*')) + '·')

      a = random.randint(1, 100)
      if not os.path.exists(f"config/{message.chat.id}.txt"):
          with open(f"config/{message.chat.id}.txt", "w") as create_new_cfg:
              create_new_cfg.write(f"{DefaultGenChanceTG}")
              bot.send_message(message.chat.id, "*Чат добавлен в базу данных*")
      b = open(f"config/{message.chat.id}.txt")
      chance = b.read()
      try:
        int(chance)
      except:
        with open(f"config/{message.chat.id}.txt", "w") as create_new_cfg:
          create_new_cfg.write(f"{DefaultGenChanceTG}")
        chance = DefaultGenChanceTG
      if a <= int(chance):
          now = datetime.datetime.now()
          text = ale()
          bot.send_message(message.chat.id, str(text))
          print("[" + now.strftime("%H:%M") + "]","Chat", str(message.chat.id), "Chance a=", a, "Message: ", text)
      else:
          now = datetime.datetime.now()
          print("[" + now.strftime("%H:%M") + "]","Chat", str(message.chat.id), "Chance a=", a, "Message: ", "Not text.")
    
while True:
  try:      
    bot.polling(none_stop=True, interval=0)
  except Exception as e:
    print(str(e))
