a = [
    [10, 5, 5, 10],
    [10, 5, 15, 10],
    [5, 10, 15, 5],
    [5, 5, 10, 5],
    [5, 10, 15, 5],
    [10, 5, 10, 10],
    [10, 10, 10, 5],
    [5, 10, 5, 5],
    [5, 5, 5, 10],
    [5, 5, 15, 10]
]

b = [' x '] * 10

c = [1, 3, 2, 4]

for i in range(10):
    b[i] = [' x '] * 10

countdominant = 0
countdominanted = 0

res = []
for i in range(10):
    for m in range(i + 1, 10):
        for j in range(4):
            if j == 0 or j == 1:
                if a[i][j] < a[m][j]:
                    countdominant += c[j]
                elif a[i][j] > a[m][j]:
                    countdominanted += c[j]
            else:
                if a[i][j] > a[m][j]:
                    countdominant += c[j]
                elif a[i][j] < a[m][j]:
                    countdominanted += c[j]
        if countdominant != 0 and countdominanted == 0:
            b[i][m] = 'inf'
            b[m][i] = ' - '
        elif countdominant == 0 and countdominanted != 0:
            b[m][i] = 'inf'
            b[i][m] = ' - '
        else:
            if countdominanted == 0:
                b[i][m] = ' - '
                b[m][i] = ' - '
            elif countdominant / countdominanted == 1:
                b[i][m] = ' - '
                b[m][i] = ' - '
            elif countdominant / countdominanted < 1:
                b[i][m] = ' - '
                b[m][i] = str(round(countdominanted / countdominant, 2))
            else:
                b[i][m] = str(round(countdominant / countdominanted, 2))
                b[m][i] = ' - '
        countdominant = 0
        countdominanted = 0

# Выравнивание
max_length = max(len(str(x)) for row in b for x in row)

# Вывод
for row in b:
    print(" ".join(str(x).rjust(max_length) for x in row))

# Определяем, сколько раз каждая альтернатива входит в другие альтернативы
alternative_counts = [0] * 10

for i in range(10):
    for j in range(10):
        if b[i][j] == ' - ':
            alternative_counts[i] += 1

# Сортировка по количеству вхождений
sorted_alternatives = sorted(range(len(alternative_counts)), key=lambda k: alternative_counts[k])

print("\nBest alternatives:")
for i in range(10):
    if i == 0:
        print(f"Alternative {sorted_alternatives[i] + 1}", end="")
    else:
        print(f" -> Alternative {sorted_alternatives[i] + 1}", end="")
print()

# Инициализируем списки для подсчета входов и выходов
in_counts = [0] * 10
out_counts = [0] * 10

for i in range(10):
    for m in range(10):
        if b[i][m] == 'inf':
            out_counts[i] += 1
            in_counts[m] += 1
        elif b[i][m] != ' - ' and b[i][m] != ' x ':
            if float(b[i][m]) > 1:
                out_counts[i] += 1
                in_counts[m] += 1
