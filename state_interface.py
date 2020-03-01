import json
#this abstract class describes user states

class UserState: 
    def process_message (self, usersStates, message, bot): 
        pass
    def process_button (self, usersStates, c, bot):
        pass

class LoggedAFKstate(UserState):
    def process_message(self, usersStates, message, bot):
        bot.send_message(message.chat.id,
            "Пока мой функционал поддерживает лишь то, что описано в /commands")

usersLoggedFlag = dict() # key - username, value bool that indicates logged or not
usersStates = {} # key - username, value state
emails = {} # key - username, value - email


SAVE_FILE_PATH = "./save.json"

def save_users_info_to_file():
    with open(SAVE_FILE_PATH, 'w') as outfile:
            json.dump({
                "usersLoggedFlag": usersLoggedFlag,
                "usersEmails": emails,
            }, outfile)

def load_saved():
    try:
        with open(SAVE_FILE_PATH) as json_file:
            global usersLoggedFlag, usersStates
            data = json.load(json_file)
            usersLoggedFlaglocal = data['usersLoggedFlag']
            for username, flag in usersLoggedFlaglocal.items():
                usersStates[username] = LoggedAFKstate()
                usersLoggedFlag[username] = flag

            loaded_emails = data['usersEmails']
            for username, email in loaded_emails.items():
                emails[username] = email

    except:
        print("error during reading of the save file")
        pass
