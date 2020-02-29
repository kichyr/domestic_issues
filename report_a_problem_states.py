import telebot
from state_interface import UserState
from state_interface import usersStates
from telebot import types

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Общежитие', 'Учебный корпус', 'Другое')

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
            bot.send_message(c.message.chat.id, 'Уточните общежитие')
            usersStates[c.message.chat.id] = DormitoriesStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
            #print("1")
        if c.data == 'Учебный корпус':
            bot.send_message(c.message.chat.id, 'Уточните учебный корпус')
            usersStates[c.message.chat.id] = AcademicBuildingsStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)
        if c.data == 'Другое':
            bot.send_message(c.message.chat.id, 'Опишите вашу проблему')
            usersStates[c.message.chat.id] = OtherStates()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)


class DormitoriesStates(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="№1", callback_data="№1")
        but_2 = types.InlineKeyboardButton(text="№2", callback_data="№2")
        but_3 = types.InlineKeyboardButton(text="№3", callback_data="№3")
        but_4 = types.InlineKeyboardButton(text="№4", callback_data="№4")
        but_5 = types.InlineKeyboardButton(text="Зюзино", callback_data="Зюзино")
        but_6 = types.InlineKeyboardButton(text="№6", callback_data="№6")
        but_7 = types.InlineKeyboardButton(text="№7", callback_data="№7")
        but_8 = types.InlineKeyboardButton(text="№8", callback_data="№8")
        but_9 = types.InlineKeyboardButton(text="№9", callback_data="№9")
        but_10 = types.InlineKeyboardButton(text="№10", callback_data="№10")
        but_11 = types.InlineKeyboardButton(text="№11", callback_data="№11")
        but_12 = types.InlineKeyboardButton(text="№12", callback_data="№12")
        but_13 = types.InlineKeyboardButton(text="Общежитие ФАЛТ", callback_data="Общежитие ФАЛТ")        
        but_13 = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        key.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_10, but_11, but_12, but_13, but_14)
        bot.send_message(message.chat.id, "Укажите общежитие", reply_markup=key)
    def process_button(self, usersStates, c, bot):
        if c.data == 'Назад':
            bot.send_message(c.message.chat.id, 'Уточните, где произошла проблема')
            usersStates[c.message.chat.id] = ProblemState()
            usersStates[c.message.chat.id].process_message(usersStates, c.message, bot)

class AcademicBuildingsStates(UserState):
    def process_message(self, usersStates, message, bot):
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="НК", callback_data="НК")
        but_2 = types.InlineKeyboardButton(text="ГК", callback_data="ГК")
        but_3 = types.InlineKeyboardButton(text="ЛК", callback_data="ЛК")
        but_4 = types.InlineKeyboardButton(text="АК", callback_data="АК")
        but_5 = types.InlineKeyboardButton(text="Физтех-Био", callback_data="Физтех-Био")
        but_6 = types.InlineKeyboardButton(text="КПМ", callback_data="КПМ")
        but_7 = types.InlineKeyboardButton(text="Радиокорпус", callback_data="Радиокорпус")
        but_8 = types.InlineKeyboardButton(text="Цифра", callback_data="Цифра")
        but_9 = types.InlineKeyboardButton(text="Арктика", callback_data="Арктика  ")
        but_10 = types.InlineKeyboardButton(text="№10", callback_data="№10")
        but_11 = types.InlineKeyboardButton(text="№11", callback_data="№11")
        but_12 = types.InlineKeyboardButton(text="№12", callback_data="№12")
        but_13 = types.InlineKeyboardButton(text="Общежитие ФАЛТ", callback_data="Общежитие ФАЛТ")
        key.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_10, but_11, but_12, but_13)
        bot.send_message(message.chat.id, "Укажите общежитие", reply_markup=key)