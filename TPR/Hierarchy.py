import math

purpose = [[1, 6, 4, 8],
           [0.1666, 1, 0.5, 2],
           [0.25, 2, 1, 4],
           [0.125, 0.5, 0.25, 1],
           ]

Price = [[1, 4, 6, 2],
         [0.25, 1, 4, 0.5],
         [0.1666, 0.25, 1, 0.125],
         [0.5, 2, 8, 1], ]

Time = [[1, 2, 4, 2],
        [0.5, 1, 4, 2],
        [0.25, 0.25, 1, 2],
        [0.5, 0.5, 0.5, 1], ]

Rating = [[1, 2, 4, 2],
          [0.5, 1, 2, 2],
          [0.25, 0.5, 1, 2],
          [0.5, 0.5, 0.5, 1], ]

Exp = [[1, 1.5, 2, 0.6666],
       [0.6666, 1, 1.5, 0.6666],
       [0.5, 0.6666, 1, 1.5],
       [1.5, 1.5, 0.6666, 1], ]


def synthesis_of_priorities(matrix):
    sum_V = 0
    for line in matrix:
        V = round(math.pow(line[0] * line[1] * line[2] * line[3], 0.25), 3)
        line.append(V)
        sum_V = round(sum_V + V, 3)

    for line in matrix:
        W = round(line[4] / sum_V, 3)
        line.append(W)
    return matrix


def synthesis_of_local_priorities(matrix, id):
    S = [0] * 4
    for line in matrix:
        for i in range(4):
            S[i] += line[i]

    P = [S[i] * matrix[i][5] for i in range(4)]
    lamda = sum(P)
    index_sogl = (lamda - 4) / 3
    res_sogl = index_sogl / 0.9
    print(res_sogl)
    if res_sogl <= 0.10:
        print('\n> Matrix "' + id + '" is consistent!')
        print("\n------------------------------------------------------------")
    else:
        print('Inadmissible consistency', res_sogl)
        print("\n------------------------------------------------------------")


def print_matrix(matrix, id):
    print(f"{id} {'A1':>8} {'A2':>8} {'A3':>8} {'A4':>8} {'V':>8} {'W':>8}")
    for j, line in enumerate(matrix):
        print(f"{j + 1} {line[0]:>8} {line[1]:>8} {line[2]:>8} {line[3]:>8} {line[4]:>8} {line[5]:>8}")


if __name__ == '__main__':
    rez = []
    new_purpose = purpose
    main_matrix = synthesis_of_priorities(new_purpose)
    web = main_matrix
    print_matrix(main_matrix, 'Purpose')
    synthesis_of_local_priorities(main_matrix, 'Goal')

    new_price = Price
    K1 = synthesis_of_priorities(new_price)
    web1 = K1
    print_matrix(K1, 'Price')
    synthesis_of_local_priorities(K1, 'Price')

    new_rating = Time
    K2 = synthesis_of_priorities(new_rating)
    web2 = K2
    print_matrix(K2, 'Time')
    synthesis_of_local_priorities(K2, 'Time')

    new_delivery_price = Rating
    K3 = synthesis_of_priorities(new_delivery_price)
    web3 = K3
    print_matrix(K3, 'Rating')
    synthesis_of_local_priorities(K3, 'Rating')

    new_delivery_quality = Exp
    K4 = synthesis_of_priorities(new_delivery_quality)
    web4 = K4
    print_matrix(K4, 'Exp')
    synthesis_of_local_priorities(K4, 'Exp')
    s = web[0][5] * web1[0][5] + web[1][5] * web2[0][5] + web[2][5] * web3[0][5] + web[3][5] * web4[0][5]

    rez.append(s)
    s = web[0][5] * web1[1][5] + web[1][5] * web2[1][5] + web[2][5] * web3[1][5] + web[3][5] * web4[1][5]

    rez.append(s)
    s = web[0][5] * web1[2][5] + web[1][5] * web2[2][5] + web[2][5] * web3[2][5] + web[3][5] * web4[2][5]

    rez.append(s)
    s = web[0][5] * web1[3][5] + web[1][5] * web2[3][5] + web[2][5] * web3[3][5] + web[3][5] * web4[3][5]

    rez.append(s)

    print(f"Alternative 1 (Price) - {round(rez[0], 3)}\n"
          f"Alternative 2 (Time) - {round(rez[1], 3)}\n"
          f"Alternative 3 (Rating) - {round(rez[2], 3)}\n"
          f"Alternative 4 (Exp) - {round(rez[3], 3)}\n")
    j = max(rez)
    l = rez.index(j)
