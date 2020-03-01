
from state_interface import UserState, usersLoggedFlag, save_users_info_to_file, LoggedAFKstate, emails
from uuid import uuid4
from email_sender import send_verification_message

class InitialRegisterState(UserState):
    def process_message(self, usersStates, message, bot):
        bot.send_message(message.chat.id,
            "Привет, для начала диалога необходимо авторизироваться используя почту phystech.edu")
        usersStates[message.chat.id] = LoginWithPhystechEduState()

class LoginWithPhystechEduState(UserState):
    def process_message(self, usersStates, message, bot):
        verification_tocken = uuid4()
        try:
            if message.text.split('@', maxsplit=1)[1] == "phystech.edu":
                try:
                    send_verification_message(message.text, verification_tocken)
                except:
                    bot.send_message(message.chat.id,"Что-то пошло не так при отправке кода подтверждения")
                    return
            else:
                bot.send_message(message.chat.id, "Введите email phystech.edu")                
                return
        except: 
            bot.send_message(message.chat.id, "Введите корректный email")
            return
        bot.send_message(message.chat.id, "Проверьте ваш почтовый ящик")
        usersStates[message.chat.id] = WaitForRightTockenState(verification_tocken, message.text)

class WaitForRightTockenState(UserState):
    def __init__(self, tocken, email):
        self.tocken = tocken
        self.email = email
    def process_message(self, usersStates, message, bot):
        print(message.text)
        print(self.tocken)
        if message.text == str(self.tocken):
            bot.send_message(message.chat.id, """
            Ваш email успешно подтвержен!
            Теперь вы можете сообщать о проблемах в кампусе,
            администрация постарается как можно быстрее их обработать""")
            usersLoggedFlag[message.from_user.username] = True
            emails[message.from_user.username] = self.email
            save_users_info_to_file()
            usersStates[message.chat.id] = LoggedAFKstate()
        else: 
            bot.send_message(message.chat.id, "Неправильный токен")