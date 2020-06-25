'''

3.2 Разработать программу, позволяющую решать систему уравнений.
    Программа должна позволять вводить коэффициенты при неизвестных,
    а также должна учитывать возможность несовместного решения системы.
    Графический интерфейс реализовать с помощью PyQt или TKinter.
    Требуется протестировать программу с помощью библиотеки.
    Сформировать отчет по выполненной самостоятельной работе и опубликовать его в портфолио.
'''

import math

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config
from kivy.uix.textinput import TextInput

Config.set('graphics', 'minimum_width', '100')
Config.set('graphics', 'minimum_height', '150')
# Config.set('graphics', 'resizable', 0)

with open("second.kv", encoding='utf8') as f:
    Builder.load_string(f.read())


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.matrix = []

    def mply(self, a=[], b=[]):
        c = []
        for i in range(len(a)):
            c.append([])
            for j in range(len(b[0])):
                c[i].append(0)
                for i1 in range(len(a[0])):
                    ci = a[i][i1] * b[i1][j]
                    c[i][j] += ci
        return c

    def printMatrix(self, a=[]):
        for i in range(len(a)):
            for j in range(len(a[0])):
                print('%10f' % a[i][j], end=" ")
            print()

    def changeMatrix(self, k, M=[]):
        for j in range(0, len(M) + 1):
            (M[k][j], M[len(M) - k - 1][j]) = (M[len(M) - k - 1][j], M[k][j])

    def factorV1(self, a=[]):

        L = [[0 for j in range(len(a))] for i in range(len(a))]
        R = [[0 for j in range(len(a))] for i in range(len(a))]

        n = len(L) - 1

        for i in range(len(L)):
            L[i][0] = a[i][0]

        R[0][0] = 1

        for j in range(1, n + 1):
            R[0][j] = a[0][j] / (L[0][0])

        for j in range(1, n + 1):
            R[j][j] = 1
            for i in range(j, n + 1):
                S = 0
                for k in range(0, j):
                    S += L[i][k] * R[k][j]
                L[i][j] = a[i][j] - S
            i = j
            for t in range(j + 1, n + 1):
                S = 0
                for k in range(0, i):
                    S += L[i][k] * R[k][t]
                R[i][t] = (a[i][t] - S) / L[i][i]

        L1 = []
        R1 = []

        for i in range(len(L)):
            L1.append([])
            for j in range(len(L[0])):
                L1[i].append(round(L[i][j], 5))
        for i in range(len(R)):
            R1.append([])
            for j in range(len(R[0])):
                R1[i].append(round(R[i][j], 5))

        Z = [0 for i in range(len(a))]
        X = [0 for i in range(len(a))]

        Z[0] = a[0][-1] / L[0][0]
        for i in range(1, n + 1):
            S = 0
            for k in range(0, i):
                S += L[i][k] * Z[k]
            Z[i] = (a[i][-1] - S) / L[i][i]

        X[n] = Z[n] / (R[n][n])
        for i in range(n - 1, -1, -1):
            S = 0
            for k in range(i + 1, n + 1):
                S += R[i][k] * X[k]
            X[i] = (Z[i] - S) / R[i][i]

        X1 = []
        for i in range(len(X)):
            X1.append([])
            X1[i].append(round(X[i], 5))

        print(X1)
        return (X1)

    def solve(self):
        cols = int(self.ids.num_col.text)
        matrix = []
        for row in range(cols):
            row_in_matrix = []
            for col in range(cols + 1):
                cell_id = 'c' + str(row) + str(col)
                cell = self.ids[cell_id]
                row_in_matrix += [float(cell.text)]
            matrix += [row_in_matrix]
        x_matrix = self.factorV1(matrix)
        x_answer = ''
        for row in range(len(x_matrix)):
            if row == (len(x_matrix) - 1):
                x_answer += 'x' + str(row + 1) + ' = ' + str(x_matrix[row][0])
            else:
                x_answer += 'x' + str( row + 1 ) + ' = ' + str(x_matrix[row][0]) + ', '
        self.ids.answer.text = x_answer

    def cells_create(self, cols):
        self.ids.matrix.clear_widgets()
        self.ids.matrix.cols = cols + 1
        for row_cell in range(cols):
            for col_cell in range(cols + 1):
                cell_id = 'c'+str(row_cell)+str(col_cell)
                input_cell = TextInput(id=cell_id, text='0', input_filter='float', multiline=False)
                self.ids.matrix.add_widget(input_cell)
                self.ids[cell_id] = input_cell

    def down(self):
        num_col = int(self.ids.num_col.text)
        if num_col > 0:
            self.ids.num_col.text = str(num_col - 1)
            self.cells_create(num_col - 1)

    def up(self):
        num_col = int(self.ids.num_col.text)
        if num_col < 10:
            self.ids.num_col.text = str(num_col + 1)
            self.cells_create(num_col + 1)


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
