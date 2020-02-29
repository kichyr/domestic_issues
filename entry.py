import telebot
import re
from state_interface import UserState, usersStates
from register_states import *
from report_a_problem_states import ProblemState
TOCKEN = '1068115374:AAGRpl9gJMcG4gow-QxHT5FplW2BMUZ2abg'


bot = telebot.TeleBot(TOCKEN)

################### COMANDS HANDLERS #############

@bot.message_handler(commands=['start'])
def show_comand_list(message):
    usersStates[message.chat.id] = InitialRegisterState()
    usersStates[message.chat.id].process_message(usersStates, message, bot)

@bot.message_handler(commands=['report_a_problem'])
def show_comand_list(message):
    usersStates[message.chat.id] = ProblemState()
    usersStates[message.chat.id].process_message(usersStates, message, bot)


#################### END ##################

#all text messages come here
@bot.message_handler(content_types=['text'])
def send_text(message): 
    usersStates[message.chat.id].process_message(usersStates, message, bot)


@bot.callback_query_handler(func=lambda c:True)
def inlin(c):
    #print(c)
    usersStates[c.message.chat.id].process_button(usersStates, c, bot)



#start infinity cycle of getting messages 
bot.polling()