import telebot
import re
from state_interface import UserState, usersLoggedFlag
from register_states import *
TOCKEN = '1068115374:AAGRpl9gJMcG4gow-QxHT5FplW2BMUZ2abg'


bot = telebot.TeleBot(TOCKEN)

usersStates = {} # key - chat_id, value state

################### COMANDS HANDLERS #############

@bot.message_handler(commands=['start'])
def show_comand_list(message):
    usersLoggedFlag[message.chat.id] = False
    usersStates[message.chat.id] = InitialRegisterState()
    usersStates[message.chat.id].process_message(usersStates, message, bot)

#################### END ##################

#all text messages come here
@bot.message_handler(content_types=['text'])
def send_text(message):
    usersStates[message.chat.id].process_message(usersStates, message, bot)


#start infinity cycle of getting messages 
bot.polling()