import matplotlib.pyplot as plt

import numpy as np
def difference_quotient(args, values, order):
    if order == 3:
        return values
    else:
        res = []
        for i in range(len(values) - 1):
            res.append((values[i+1] - values[i])/(args[i+order] - args[i]))
        return difference_quotient(args, res, order + 1)

def Q_and_U(ts, ys, M):
    ds = [6 * i for i in difference_quotient(ts, ys, 1)]
    # [0, q1, ..., q_n-1]
    Q = [0] * M
    U = [0] * M

    for i in range(1, M):
        lambda_i = (ts[i] - ts[i-1])/(ts[i+1] - ts[i-1])
        p = lambda_i * Q[i-1] + 2
        Q[i] = (lambda_i - 1) / p
        U[i] = (ds[i-1] - lambda_i*U[i-1]) / p

    return Q,U

def count_moment(Q, U, k, moments):
    if k == 0:
        return
    else:
        moments[k] = U[k] + Q[k] * moments[k+1]
        count_moment(Q, U, k-1, moments)


def create_formula(M, ys):
    moments = [0] * (M+1)
    ts = [i/M for i in range(M+1)]
    Q,U = Q_and_U(ts, ys, M)
    count_moment(Q,U,M-1,moments)
    S = []

    for k in range(1, M + 1):
        hk = ts[k] - ts[k - 1]
        S.append(lambda t, k=k, moments=moments, ts=ts, ys=ys, hk=hk: (1 / hk) * (
                ((1 / 6) * moments[k - 1] * (ts[k] - t) ** 3) + (1 / 6) * moments[k] * ((t - ts[k - 1]) ** 3) +
                (ys[k - 1] - (1 / 6) * moments[k - 1] * (hk ** 2)) * (ts[k] - t) + (
                            ys[k] - (1 / 6) * moments[k] * hk ** 2) * (t - ts[k - 1])
        ))

    return S

def draw(M, values_x, values_y, ts_x, ts_y, quality = 500):
    formulas_x = create_formula(M, values_x)
    formulas_y = create_formula(M, values_y)

    draw_args = [i / quality for i in range(quality + 1)]

    x_points = []
    y_points = []
    # for every generated argument we find backups.txt suitable function
    # from the generated functions, based on ranges of each function
    for a in draw_args:
        for i, t in enumerate(ts_x):
            if a < t:
                x_points.append(formulas_x[i - 1](a))
                break
        for i, t in enumerate(ts_y):
            if a < t:
                y_points.append(formulas_y[i - 1](a))
                break

    plt.plot(x_points, y_points, marker='o', linestyle='-', color='#ea6193', markersize=0.1)



def getCoords(filename):
    # x arguments for x-axis and y-axis points
    with open(filename, 'r') as file:
        text = file.readline()
        strokes = text.split('|')

        res = [[int(c) for c in s.split(',') if c != ''] for s in strokes]
        return [elem for elem in res if elem != []]

def forge():
    # get list of list of strokes
    strokes_x = getCoords('clicked_x.txt')
    strokes_y = getCoords('clicked_y.txt')



    for i in range(len(strokes_x)):
        M = len(strokes_x[i]) - 1
        # for dot, interpolation is backups.txt dot
        if M != 0:
            ts = [i / M for i in range(M + 1)]
            with open('args.txt', 'a') as f:
                f.write(str(ts) + '\n')
            draw(M, strokes_x[i], strokes_y[i], ts, ts)
        else:
            plt.plot(strokes_x[i], strokes_y[i], marker='o', linestyle='-', color='r', markersize=0.5)

    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.savefig("result.jpg")
    plt.savefig("result.png")
    plt.show()


if __name__ == '__main__':
    forge()