import telebot
import re
from state_interface import UserState, usersLoggedFlag, usersStates, save_users_info_to_file, load_saved
from register_states import InitialRegisterState
import json
from report_a_problem_states import ProblemState

TOCKEN = '1068115374:AAGRpl9gJMcG4gow-QxHT5FplW2BMUZ2abg'
SAVE_FILE_PATH = "./save.json"


bot = telebot.TeleBot(TOCKEN)

################LOAD INFO ABOUT USERS########
load_saved()
############# COMANDS HANDLERS ##############

@bot.message_handler(commands=['start'])
def start_command(message):
    if str(message.from_user.username) in usersLoggedFlag and usersLoggedFlag[str(message.from_user.username)] == True:
        bot.send_message(message.chat.id,
            "Вы уже авторизованы")
        return

    usersLoggedFlag[message.from_user.username] = False
    usersStates[message.chat.id] = InitialRegisterState()
    usersStates[message.chat.id].process_message(usersStates, message, bot)
    save_users_info_to_file()

@bot.message_handler(commands=['report_a_problem'])
def report_problem_handler(message):
    usersStates[message.chat.id] = ProblemState()
    usersStates[message.chat.id].process_message(usersStates, message, bot)

#################### END ##################

#all text messages come here
@bot.message_handler(content_types=['text'])
def send_text(message):
    usersStates[message.chat.id].process_message(usersStates, message, bot)


@bot.callback_query_handler(func=lambda c:True)
def inlin(c):
    usersStates[c.message.chat.id].process_button(usersStates, c, bot)


#start infinity cycle of getting messages 
bot.polling()