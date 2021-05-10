import telebot 
import config

class Notifier:

	def __init__(self):
		self.TOKEN = config.TELEGRAM_KEY
		self.bot = telebot.TeleBot(self.TOKEN)
		self.chat_id = -537121416

	def prepare_text(self, data):
		pass

	def send_message(self, text):
		
		msg = self.bot.send_message(self.chat_id, text)

# n = Notifier()
# n.send_message("Ваша воля моими руками")