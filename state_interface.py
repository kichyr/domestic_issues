#this abstract class describes user states
class UserState: 
    def process_message (self, usersStates, message, bot): 
        pass
    def process_button (self, usersStates, c, bot):
        pass

usersStates = {} # key - chat_id, value state