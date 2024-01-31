import kivy
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class PersonalCabinet(App):

    def build(self):
        self.connection = sqlite3.connect('users.db')
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (username TEXT, password TEXT)''')
        self.connection.commit()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        self.username_input = TextInput(hint_text='Имя пользователя', size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text='Пароль', password=True, size_hint_y=None, height=40)

        register_button = Button(text='Регистрация', size_hint_y=None, height=40)
        register_button.bind(on_press=self.register)

        login_button = Button(text='Вход', size_hint_y=None, height=40)
        login_button.bind(on_press=self.login)

        layout.add_widget(Label(text='ЛИЧНЫЙ КАБИНЕТ', size_hint_y=None, height=40))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(register_button)
        layout.add_widget(login_button)

        return layout

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()
        print("Пользователь зарегистрирован.")

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            print("Вход выполнен успешно.")
        else:
            print("Неверное имя пользователя или пароль.")


if __name__ == '__main__':
    PersonalCabinet().run()
