import telebot
from state_interface import UserState
from state_interface import usersStates
from telebot import types

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Общежитие', 'Учебный корпус', 'Другое')
dormitories = ['№1', '№2', "№3", "№4", "Зюзино", "№6", "№7", "№8", "№9", "№10", "№11", "№12", "ФАЛТ МФТИ"]
academic_buildings = ['НК', 'ГК', "ЛК", "АК", "Физтех-Био", "Радиокорпус", "Цифра", "Арктика", "КПМ", "СK №1", "СK №2", "СK Бассейн", "КСП"]
experts = ['Сантехник', 'Электрик', 'Плотник', 'Специалист по дезинсекции', 'Другое']
back = "Назад"

class ProblemState(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="Общежитие", callback_data="Общежитие")
        but_2 = types.InlineKeyboardButton(text="Учебный корпус", callback_data="Учебный корпус")
        but_3 = types.InlineKeyboardButton(text="Другое", callback_data="Другое")
        key.add(but_1, but_2, but_3)
        bot.send_message(message.chat.id, "Уточните, где произошла проблема", reply_markup=key)
    def process_button(self, usersStates, c, bot):
        if c.data == 'Общежитие':
            usersStates[c.message.chat.id] = DormitoriesStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        if c.data == 'Учебный корпус':
            usersStates[c.message.chat.id] = AcademicBuildingsStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        if c.data == 'Другое':
            bot.send_message(c.message.chat.id, 'Опишите вашу проблему')
            usersStates[c.message.chat.id] = OtherProblemStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)

class DormitoriesStates(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but = []
        for dom in dormitories:
            but.append(types.InlineKeyboardButton(text=dom, callback_data=dom))
        but.append(types.InlineKeyboardButton(text="Назад", callback_data="Назад"))
        for dom in but:
            key.add(dom)
        bot.send_message(message.chat.id, "Укажите общежитие", reply_markup=key)
    def process_button(self, usersStates, c, bot):
        if c.data == 'Назад':
            usersStates[c.message.chat.id] = ProblemState()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        else: 
            usersStates[c.message.chat.id] = Problems_expert()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)

class AcademicBuildingsStates(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but = []
        for academ in academic_buildings:
            but.append(types.InlineKeyboardButton(text=academ, callback_data=academ))
        but.append(types.InlineKeyboardButton(text="Назад", callback_data="Назад"))
        for academ in but:
            key.add(academ)
        bot.send_message(message.chat.id, "Укажите учебный корпус", reply_markup=key)
    def process_button(self, usersStates, c, bot):
        if c.data == 'Назад':
            usersStates[c.message.chat.id] = ProblemState()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        else: 
            usersStates[c.message.chat.id] = Problems_expert()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)

class Problems_expert(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but = []
        for exp in experts:
            but.append(types.InlineKeyboardButton(text=academ, callback_data=academ))
        but.append(types.InlineKeyboardButton(text="Назад", callback_data="Назад"))
        for exp in but:
            key.add(exp)
        bot.send_message(message.chat.id, "Выберите требуемого специалиста", reply_markup=key)
    def process_button(self, usersStates, c, bot):
        if c.data == 'Назад':
            usersStates[c.message.chat.id] = ProblemState()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        #else: 
            #Читаем комментарий/обращение и записываем в соотвествующее поле

#class OtherProblemStates(UserState):
#    def process_message(self, usersStates, message, bot):
        #Читаем комментарий/обращение и записываем в соотвествующее поле