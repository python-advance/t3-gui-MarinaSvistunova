'''
3.1. Реализация графического интерфейса и функционала, позволяющего отображать графические примитивы для игры 
     «Крестики-нолики». Сформировать отчет по выполненной самостоятельной работе и опубликовать его в портфолио.
'''

from kivy.app import App
from kivy.config import Config
from kivy.graphics.vertex_instructions import Line
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', 0)

with open("third.kv", encoding='utf8') as f:
    Builder.load_string(f.read())

symbols = ['x', 'o']


def symbol_generator():
    while True:
        for symbol in symbols:
            yield symbol


class RootWidget(GridLayout):

    moves = None
    symbol = None

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.symbol = symbol_generator()

        self.cols = 3
        self.cells = []

        self.moves = 0

        for i in range(self.cols * self.cols):
            self.cells += ['']
            self.add_widget(Button(on_press=self.change, text=''))


    def change(self, instance):

        if instance.text == 'x' or instance.text == 'o':
            return None

        padding_draw = 10

        draw_symbol = self.symbol.__next__()
        if draw_symbol == 'x':
            with instance.canvas:
                Line(points=(instance.x + padding_draw, instance.y + padding_draw,
                             instance.x + instance.width - padding_draw, instance.y + instance.height - padding_draw),
                      width=3)
                Line(points=(instance.x + instance.width - padding_draw, instance.y + padding_draw,
                             instance.x + padding_draw, instance.y + instance.height - padding_draw),
                      width=3)

        else:
            with instance.canvas:
                Line(circle=(instance.center_x, instance.center_y, min(instance.width, instance.height)/2 - padding_draw),
                     width=3)

        if instance in self.children:
            self.cells[self.children.index(instance)] = draw_symbol
            instance.text = draw_symbol

        self.find_winner()

    def find_winner(self):

        self.moves += 1

        result = ''

        # rows
        row_numbers = 0
        row = 0
        while row_numbers < self.cols:
            for i in range(self.cols):
                result += str(self.cells[row + i])
            row += 3
            row_numbers += 1

            result = str(self.winner(result))

        # cols
        col_numbers = 0
        col = 0
        while col_numbers < self.cols:
            for i in range(self.cols):
                result += str(self.cells[col + i*3])
            print(type(self.cells[col + i*3]))
            print(result)
            col += 1
            col_numbers += 1

            result = str(self.winner(result))

        # direct diagonal
        for i in range(self.cols):
            result += str(self.cells[i*4])
        result = str(self.winner(result))

        # reverse diagonal
        cols_minus = self.cols - 1
        for i in range(cols_minus, self.cols*cols_minus + 1, cols_minus):
            result += str(self.cells[i])
        result = str(self.winner(result))

        if result == '' and self.moves == self.cols*self.cols:
            self.not_of_two()

    def winner(self, result):
        if result == 'xxx' or result == 'ooo':
            self.canvas.clear()
            self.clear_widgets()

            for i in range(4):
                self.add_widget(Label(text=''))
            self.add_widget(Label(text='%s won the game!' % result[0:1:1], color=(1, 1, 1, 1)))
            for i in range(2):
                self.add_widget(Label(text=''))
            self.add_widget(Button(text='Restart', on_press=self.restart_game, background_color=(1, 1, 1, 1), color=(1, 1, 1, 1)))
        else:
            return ''

    def not_of_two(self):
        self.canvas.clear()
        self.clear_widgets()

        for i in range(4):
            self.add_widget(Label(text=''))
        self.add_widget(Label(text='Nobody won the game!'))
        for i in range(2):
            self.add_widget(Label(text=''))
        self.add_widget(
            Button(text='Restart', on_press=self.restart_game, background_color=(1, 1, 1, 1), color=(1, 1, 1, 1)))

    def restart_game(self, instance):
        self.canvas.clear()
        self.clear_widgets()
        self.__init__()


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
