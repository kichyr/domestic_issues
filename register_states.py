
from state_interface import UserState

class InitialRegisterState(UserState):
    def process_message(self, usersStates, message, bot):
        bot.send_message(message.chat.id,
            "Привет, для начала диалога необходимо авторизироваться используя почту phystech.edu")
        usersStates[message.chat.id] = LoginWithPhystechEduState()

class LoginWithPhystechEduState(UserState):
    def process_message(self, usersStates, message, bot):
        print("ждем логина")