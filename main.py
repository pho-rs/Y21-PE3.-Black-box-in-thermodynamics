import random as rnd
import matplotlib.pyplot as plt

T10 = 15.0
T1Q = 22.5
Q = 40.0
C1_under = 0.6
C1_upon = 1.4
C2 = 1
d_tau = 0.0001
number_or_unchecked = 1000
alpha = 0.1
t_end = 100

wrong_ansers = ["Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз",
                "Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз", "Некорректный ввод",
                "Некорректный ввод", "Некорректный ввод", "Некорректный ввод", "Некорректный ввод", "Некорректный ввод",
                "Некорректный ввод", "Нет", "Нет", "Нет", "Нет", "Нет", "Бронза и забвение", "Глупости",
                "Я сейчас перестану работать", "Вон из сборной!", "Нет", "Press \"Ctrl+C\" to continue",
                "Пользовательская ошибка. Замените пользователя"]

def melting_sim(T1Q_curr, Q_curr, C2_curr, T20_curr, t0_curr, t_end_curr):
    T2_arr = []
    t_arr = []
    T2_curr = T20_curr
    t_curr = t0_curr
    Q_left = Q_curr
    melted = False
    unchecked = number_or_unchecked
    end_cim = False
    while (not melted) and (T2_curr > T1Q_curr) and (not end_cim):
        Q_left = Q_left + alpha * (T1Q_curr - T2_curr) * d_tau
        T2_curr = T2_curr + alpha * (T1Q_curr - T2_curr) * d_tau / (1.0 * C2_curr)
        t_curr += d_tau
        unchecked += 1
        if unchecked >= number_or_unchecked:
            T2_arr.append(T2_curr)
            t_arr.append(t_curr)
            unchecked = 0
        if t_curr>t_end_curr:
            end_cim = True
        if Q_left <= 0:
            melted = True
    if melted:
        return "melted", (t_curr, t_arr, T2_arr, T2_curr)
    elif end_cim:
        return "end sim", (t_arr, T2_arr)
    else:
        while(t_curr < t_end_curr):
            t_curr += d_tau
            unchecked += 1
            if unchecked >= number_or_unchecked:
                T2_arr.append(T2_curr)
                t_arr.append(t_curr)
                unchecked = 0
        return "end sim", (t_arr, T2_arr)


def heating_after_sim(T20_curr, T10_curr, t_start, C1_curr, C2_curr, t_end_curr):
    T2_arr = []
    t_arr = []
    T2_curr = T20_curr
    T1_curr = T10_curr
    t_curr = t_start
    unchecked = number_or_unchecked
    while (t_curr < t_end_curr):
        T2_curr = T2_curr + (alpha * (T1_curr - T2_curr) * d_tau) / (1.0 * C2_curr)
        T1_curr = T1_curr - (alpha * (T1_curr - T2_curr) * d_tau) / (1.0 * C1_curr)
        t_curr = t_curr + d_tau
        unchecked += 1
        if unchecked >= number_or_unchecked:
            T2_arr.append(T2_curr)
            t_arr.append(t_curr)
            unchecked = 0

    return t_arr, T2_arr


def heating_between_sim(T20_curr, T10_curr, T1Q_curr, t0_curr, C1_curr, C2_curr, t_end_curr):
    T2_arr = []
    t_arr = []
    T2_curr = T20_curr
    T1_curr = T10_curr
    t_curr = t0_curr
    unchecked = number_or_unchecked
    while True:
        T2_curr = T2_curr + (alpha * (T1_curr - T2_curr) * d_tau) / (1.0 * C2_curr)
        T1_curr = T1_curr - (alpha * (T1_curr - T2_curr) * d_tau) / (1.0 * C1_curr)
        t_curr = t_curr + d_tau
        unchecked += 1
        if unchecked >= number_or_unchecked:
            T2_arr.append(T2_curr)
            t_arr.append(t_curr)
            unchecked = 0
        if t_curr>t_end_curr:
            return "end sim", (t_arr, T2_arr)
        if T1_curr >= T1Q_curr:
            return "st melt", (t_curr, t_arr, T2_arr, T2_curr)
        if T2_curr <=T1Q_curr:
            return "av melt", (t_curr, t_arr, T2_arr, T2_curr, T1_curr)


def simple_sim(Q_curr, C1_under_curr, C1_upon_curr, T10_curr, T1Q_curr, C2_curr, T20_curr, t_end_curr):
    T1_curr = T10_curr
    T2_curr = T20_curr
    t_curr = 0
    if T1_curr > T1Q_curr:
        return heating_after_sim(T2_curr,T1_curr, t_curr, C1_upon_curr, C2_curr, t_end_curr)
    elif T2_curr < T1Q_curr:
        return heating_after_sim(T2_curr,T1_curr, t_curr, C1_under_curr, C2_curr, t_end_curr)
    else:
        react, ans = heating_between_sim(T2_curr, T1_curr, T1Q_curr, 0, C1_under_curr, C2_curr, t_end_curr)
        if react == "end sim":
            return ans
        elif react == "av melt":
            t_curr, t_arr, T2_arr, T2_curr, T1_curr = ans
            new_ans = heating_after_sim(T2_curr, T1_curr, t_curr, C1_under_curr, C2_curr, t_end_curr)
            return t_arr + new_ans[0], T2_arr + new_ans[1]
        else:
            t_curr, t_arr, T2_arr, T2_curr = ans
            react, ans = melting_sim(T1Q_curr, Q_curr, C2_curr, T2_curr, t_curr, t_end_curr)
            if react == "melted":
                t_arr = t_arr + ans[1]
                T2_arr = T2_arr + ans[2]
                t_curr = ans[0]
                T2_curr = ans[3]
                T1_curr = T1Q_curr
                new_ans = heating_after_sim(T2_curr, T1_curr, t_curr, C1_upon_curr, C2_curr, t_end_curr)
                return t_arr + new_ans[0], T2_arr + new_ans[1]
            else:
                return t_arr+ans[0], T2_arr+ans[1]


def T2infT20(end):
    T2 = range(0, end, 1)
    T_end = []
    for T20q in T2:
        t_sim, T_sim = simple_sim(Q, C1_under, C1_upon, T10, T1Q, C2, T20q, t_end)
        T_end.append(T_sim[len(T_sim) - 1])
    plt.grid()
    plt.plot(T2, T_end)
    plt.xlabel("Начальная температура")
    plt.ylabel("Установившаяся температура")
    plt.show()
    return T2, T_end


def evol_of_Temp(T222):
    t_sim, T_sim = simple_sim(Q, C1_under, C1_upon, T10, T1Q,C2, T222, t_end)
    i = 10
    while(abs(T_sim[i]-T_sim[len(T_sim)-1])>=0.01) and (i<len(T_sim)-1):
        i+=1
    return t_sim[0:i], T_sim[0:i]


def incorrect_ans():
    str = wrong_ansers[rnd.randint(0, len(wrong_ansers)-1)]
    return str


def is_num(st):
    if st.isdigit():
        return True
    else:
        try:
            float(st)
            return True
        except ValueError:
            return False


while True:
    print("\nВведите начальную температуру: \n")

    temp_0 = input()
    if is_num(temp_0):
        if (float(temp_0) >= 0) and (float(temp_0) <= 100):
            temp = float(temp_0)
            t, T = evol_of_Temp(temp)
            file_obj = open("anwser" + str(round(temp, 2)) + ".txt", 'w')
            for i in range(len(t)):
                file_obj.write("Время: | " + str(round(t[i], 1)) + " | Температура: | " + str(round(T[i], 2)) + " |\n")
            file_obj.close()
        else:
            print("\n"+incorrect_ans())
    else:
        print("\n" + incorrect_ans())