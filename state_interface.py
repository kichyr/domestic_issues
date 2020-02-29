#this abstract class describes user states
class UserState: 
    def process_message (self, usersStates, message, bot): 
        pass

usersLoggedFlag = {} # key - chat_id, value bool that indicates logged or not