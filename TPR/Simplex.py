import numpy as np


class LinearModel:
    # Инициализация параметров модели
    def __init__(self, A=np.empty([0, 0]), b=np.empty([0, 0]), c=np.empty([0, 0]), minmax="MAX"):
        self.A = A  # Матрица коэффициентов ограничений
        self.b = b  # Вектор правой части ограничений
        self.c = c  # Вектор коэффициентов целевой функции
        self.x = [float(0)] * len(c)  # Начальное решение (все переменные равны нулю)
        self.minmax = minmax  # Тип оптимизации (минимизация или максимизация)
        self.printIter = True  # Флаг для печати итераций
        self.optimalValue = None  # Оптимальное значение целевой функции
        self.transform = False  # Флаг для преобразования модели

    def addA(self, A):  # Установка матрицы коэффициентов ограничений
        self.A = A

    def addB(self, b):  # Установка вектора правой части ограничений
        self.b = b

    def addC(self, c):  # Установка вектора коэффициентов целевой функции
        self.c = c
        self.transform = False

    def setObj(self, minmax):  # Установка типа оптимизации
        self.minmax = minmax
        self.transform = False

    def setPrintIter(self, printIter):  # Установка флага для печати итераций
        self.printIter = printIter

    def printSoln(self):  # Печать решения и оптимального значения
        print(" Коэффициенты: ")
        print("", self.x)
        print("\n Оптимальное значение: ")
        print("", self.optimalValue)

    def getTableau(self):  # Создание симплекс-таблицы
        num_var = len(self.c)  # Получение количества переменных
        num_slack = len(self.A)  # Получение количества ограничений
        # Создание верхней строки таблицы
        t1 = np.hstack(([None], [0], self.c, [0] * num_slack))
        # Создание базисных переменных и расширение матрицы А, если необходимо
        basis = np.array([0] * num_slack)  # Создание массива для базисных переменных
        for i in range(0, len(basis)):
            basis[i] = num_var + i  # Установка индексов базисных переменных
        A = self.A
        if not ((num_slack + num_var) == len(self.A[0])):
            # Если матрица A не квадратная, добавляем единичную матрицу для расширения
            B = np.identity(num_slack)
            A = np.hstack((self.A, B))
        # Создание нижних строк таблицы
        t2 = np.hstack((np.transpose([basis]), np.transpose([self.b]), A))

        # Объединение верхней и нижней частей таблицы
        tableau = np.vstack((t1, t2))  # Слияние верхней и нижней частей таблицы
        tableau = np.array(tableau, dtype='float')  # Преобразование в массив NumPy
        return tableau  # Возвращение симплекс-таблицы

    def optimize(self): # Оптимизация симплекс-методом
        tableau = self.getTableau()  # Получение симплекс-таблицы

        if self.printIter:
            print(" Стартовая таблица:")
            self.print_table(tableau, True)  # Печать начальной симплекс-таблицы
        optimal = False  # Флаг для проверки на оптимальность
        iter = 0  # Счетчик итераций
        while 1:
            if self.printIter:
                if iter > 0:
                    print("\n=====================\n")
                    print(" Итерация :", iter)
                    self.print_table(tableau, False)  # Печать текущей симплекс-таблицы
            for profit in tableau[0, 2:]:
                if profit > 0:
                    optimal = False
                    break
                optimal = True
            if optimal:
                break
            n = tableau[0, 2:].tolist().index(np.amax(tableau[0, 2:])) + 2 # Выбор разрешающего столбца
            minimum = 99999  # Инициализация минимального значения
            r = -1  # Инициализация разрешающей строки
            for i in range(1, len(tableau)):
                if tableau[i, n] > 0:
                    val = tableau[i, 1] / tableau[i, n]
                    if val != 0 and val < minimum:
                        minimum = val  # Обновление минимального значения
                        r = i  # Обновление разрешающей строки
            pivot = tableau[r, n]  # Получение разрешающего элемента
            print("\n Разрешающий столбец:", n - 1)
            print(" Разрешающая строка:", r)
            print(" Разрешающий элемент: ", pivot)
            tableau[r, 1:] = tableau[r, 1:] / pivot  # Деление строки на разрешающий элемент
            for i in range(0, len(tableau)):
                if i != r:
                    mult = tableau[i, n] / tableau[r, n]  # Вычисление множителя
                    tableau[i, 1:] = tableau[i, 1:] - mult * tableau[r, 1:]  # Обновление строк
            tableau[r, 0] = n - 2  # Обновление индекса базисной переменной в таблице
            iter += 1  # Увеличение счетчика итераций
        if self.printIter:
            print("\n----------------------------------\n")
            print(" Финальная таблица была получена за", iter, "итерации")
            self.print_table(tableau, False)  # Печать финальной симплекс-таблицы
        else:
            print("Решено")
        self.x = np.array([0] * len(self.c), dtype=float)  # Создание массива для решения
        for key in range(1, (len(tableau))):
            if tableau[key, 0] < len(self.c):
                self.x[int(tableau[key, 0])] = tableau[key, 1]  # Обновление значений переменных
            self.optimalValue = -1 * tableau[0, 1]  # Установка оптимального значения

    def print_table(self, tableau, start):  # Функция для печати симплекс-таблицы
        print("ind A0\t\t ", end="")  # Печать заголовка столбца с индексом и A0

        for i in range(1, len(self.c) + 1):  # Печать заголовков столбцов переменных x
            print("x_" + str(i), end="\t ")

        for i in range(1, 5):  # Печать заголовков столбцов правой части ограничений
            print("b_" + str(i), end="\t ")
        print()  # Переход на новую строку после печати заголовка

        for j in range(0, len(tableau)):  # Перебор строк таблицы
            for i in range(0, len(tableau[0])):  # Перебор элементов в строке
                if not np.isnan(tableau[j, i]):  # Проверка, что элемент не NaN
                    if i == 0:  # Если это первый столбец (индекс базисной переменной)
                        print('x_' + str(int(tableau[j, i]) + 1), end="\t ")
                    else:
                        if j == 0 and start is False:  # Если это первая строка и start равно False
                            if round(tableau[j, i], 2) == 0:
                                print(round(tableau[j, i], 2),
                                      end="\t ")  # Если значение округленное до 2 знаков после запятой равно 0
                            else:
                                print((-1) * round(tableau[j, i], 2),
                                      end="\t ")  # В противном случае, печать отрицательного значения
                        else:
                            print(round(tableau[j, i], 2), end="\t ")  # Если не первая строка или start равно True
                else:
                    print('F', end="\t ")  # Если элемент NaN, печать символа 'F' вместо значения
            print()  # Переход на новую строку после печати строки таблицы
if __name__ == '__main__':
    model1 = LinearModel()
    A = np.array(
        [
            [16, 12],
            [0.2, 0.4],
            [6, 5],
            [3, 4]
        ]
    )
    b = np.array(
        [1200, 30, 600, 300]
    )
    c = np.array(
        [260, 300]
    )
    model1.addA(A)
    model1.addB(b)
    model1.addC(c)
    print("\n Дано:")
    print("> A =\n", A, "\n")
    print("> А0 =\n", b, "\n")
    print("> C =\n", c, "\n\n")
    model1.optimize()
    print("\n")
    model1.printSoln()
