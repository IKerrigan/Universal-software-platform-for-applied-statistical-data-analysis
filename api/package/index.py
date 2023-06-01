import sys
import os
import numpy as np
import math as mt
import matplotlib.pyplot as plt
from scipy.stats import t
import mpld3
import pandas as pd
import scikit_posthocs as sp
from typing import Union, List


def parse_file(file_name, column_name):
    ex_data = pd.read_excel(file_name)
    return ex_data[column_name].values.tolist()


def uniform_distribution(n, iter, anomaly_count):
    fig = plt.figure()
    outlier_indices = np.zeros((anomaly_count))
    sample = np.zeros((n))
    for i in range(n):
        sample[i] = np.random.randint(0, iter)
    mean = np.median(sample)
    variance = np.var(sample)
    standard_deviation = mt.sqrt(variance)
    for i in range(anomaly_count):
        outlier_indices[i] = mt.ceil(np.random.randint(1, iter))

    print('номери АВ: outlier_indices=', outlier_indices)
    print('----- Статистичні характеристики рівномірного закону розподілу випадкової величини -----')
    print('Матиматичне сподівання =', mean)
    print('Дисперсія =', variance)
    print('Середнє квадратичне відхилення =', standard_deviation)
    print('-----------------------------------------------------------------------')

    plt.hist(sample, bins=20, facecolor="blue", alpha=0.5)

    if os.environ["DISPLAY_PLOTS"] == "1":
        plt.show()

    return outlier_indices, mpld3.fig_to_html(fig), {'mean': mean, 'variance': variance, 'standard_deviation': standard_deviation, 'text': 'Статистичні характеристики рівномірного закону розподілу випадкової величини'}


def normal_distribution(sample_mean, sigma, iter):
    fig = plt.figure()
    sample = np.random.normal(sample_mean, sigma, iter)
    mean = np.median(sample)
    variance = np.var(sample)
    standard_deviation = mt.sqrt(variance)
    print('------- Статистичні характеристики нормального закону розподілу випадкової величини -----')
    print('Матиматичне сподівання =', mean)
    print('Дисперсія =', variance)
    print('Середнє квадратичне відхилення =', standard_deviation)
    print('------------------------------------------------------------------')
    plt.hist(sample, bins=20, facecolor="blue", alpha=0.5)

    if os.environ["DISPLAY_PLOTS"] == "1":
        plt.show()

    return sample, mpld3.fig_to_html(fig), {'mean': mean, 'variance': variance, 'standard_deviation': standard_deviation, 'text': 'Статистичні характеристики нормальної похибки вимірів'}


def create_trend_model(n):
    values = np.zeros((n))
    for i in range(n):
        values[i] = (0.0000005*i*i)
    return values


def create_randomvar_model(SN, S0N, n):
    norm_model = np.zeros((n))
    for i in range(n):
        norm_model[i] = S0N[i]+SN[i]
    return norm_model


def create_random_outliers_model(values, norm_model, anomaly_count, coef_outliers, sigma, outlier_indices, sample_mean):
    model = norm_model
    normal_error = np.random.normal(sample_mean, (coef_outliers * sigma), anomaly_count)
    for i in range(anomaly_count):
        k = int(outlier_indices[i])
        model[k] = values[k] + normal_error[i]
    return model


def calculate_statistics(SL, Text):
    Yout = smooth_mnk(SL)
    iter = len(Yout)
    SL0 = np.zeros((iter))
    for i in range(iter):
        SL0[i] = SL[i] - Yout[i, 0]
    mean = np.median(SL0)
    variance = np.var(SL0)
    standard_deviation = mt.sqrt(variance)
    print('------------', Text, '-------------')
    print('Математичне сподівання =', mean)
    print('Дисперсія =', variance)
    print('Середнє квадратичне відхилення =', standard_deviation)
    print('-----------------------------------------------------')
    return {'mean': mean, 'variance': variance, 'standard_deviation': standard_deviation, 'text': Text}


def plot_trend_graph(S0_L, SV_L, Text):
    fig = plt.figure()

    plt.clf()

    plt.plot(SV_L)
    plt.plot(S0_L)

    plt.ylabel(Text)

    if os.environ["DISPLAY_PLOTS"] == "1":
        plt.show()

    return mpld3.fig_to_html(fig)


def smooth_mnk(values):
    iter = len(values)
    Yin = np.zeros((iter, 1))
    F = np.ones((iter, 3))
    for i in range(iter):
        Yin[i, 0] = float(values[i])
        F[i, 1] = float(i)
        F[i, 2] = float(i * i)
    FT = F.T
    FFT = FT.dot(F)
    FFTI = np.linalg.inv(FFT)
    FFTIFT = FFTI.dot(FT)
    C = FFTIFT.dot(Yin)
    Yout = F.dot(C)
    return Yout


def remove_outliers_mnk(values):
    iter = len(values)
    Yin = np.zeros((iter, 1))
    F = np.ones((iter, 3))
    for i in range(iter):
        Yin[i, 0] = float(values[i])
        F[i, 1] = float(i)
        F[i, 2] = float(i * i)
    FT = F.T
    FFT = FT.dot(F)
    FFTI = np.linalg.inv(FFT)
    FFTIFT = FFTI.dot(FT)
    C = FFTIFT.dot(Yin)
    return C[1, 0]


def mnk_extrapolation(values, prediction_interval):
    iter = len(values)
    Yout_Extrapol = np.zeros((iter+prediction_interval, 1))
    Yin = np.zeros((iter, 1))
    F = np.ones((iter, 3))
    for i in range(iter):
        Yin[i, 0] = float(values[i])
        F[i, 1] = float(i)
        F[i, 2] = float(i * i)
    FT = F.T
    FFT = FT.dot(F)
    FFTI = np.linalg.inv(FFT)
    FFTIFT = FFTI.dot(FT)
    C = FFTIFT.dot(Yin)
    print('Регресійна модель:')
    print('y(t) = ', C[0, 0], ' + ', C[1, 0], ' * t', ' + ', C[2, 0], ' * t^2')
    for i in range(iter+prediction_interval):
        Yout_Extrapol[i, 0] = C[0, 0]+C[1, 0]*i+(C[2, 0]*i*i)
    return Yout_Extrapol


def tietjen_outlier_removal(
            x: Union[List, np.ndarray],
            k: int,
            hypo: bool = False,
            alpha: float = 0.05) -> Union[np.ndarray, bool]:
        arr = np.copy(x)
        n = arr.size

        def tietjen(x_, k_):
            x_mean = x_.mean()
            r = np.abs(x_ - x_mean)
            z = x_[r.argsort()]
            E = np.sum((z[:-k_] - z[:-k_].mean()) ** 2) / np.sum((z - x_mean) ** 2)
            return E

        e_x = tietjen(arr, k)
        e_norm = np.zeros(5000)

        for i in np.arange(5000):
            norm = np.random.normal(size=n)
            e_norm[i] = tietjen(norm, k)

        CV = np.percentile(e_norm, alpha * 100)
        result = e_x < CV

        if hypo:
            return result
        else:
            if result:
                ind = np.argpartition(np.abs(arr - arr.mean()), -k)[-k:]
                return np.delete(arr, ind)
            else:
                return arr


def alpha_beta_filter(values):
    iter = len(values)
    Yin = np.zeros((iter, 1))
    YoutAB = np.zeros((iter, 1))
    T0 = 1
    for i in range(iter):
        Yin[i, 0] = float(values[i])
    Yspeed_retro = (Yin[1, 0]-Yin[0, 0])/T0
    Yextra = Yin[0, 0]+Yspeed_retro
    alfa = 2*(2*1-1)/(1*(1+1))
    beta = (6/1)*(1+1)
    YoutAB[0, 0] = Yin[0, 0]+alfa*(Yin[0, 0])
    for i in range(1, iter):
        YoutAB[i, 0] = Yextra+alfa*(Yin[i, 0] - Yextra)
        Yspeed = Yspeed_retro+(beta/T0)*(Yin[i, 0] - Yextra)
        Yspeed_retro = Yspeed
        Yextra = YoutAB[i, 0] + Yspeed_retro
        alfa = (2 * (2 * i - 1)) / (i * (i + 1))
        beta = 6 / (i * (i + 1))
    return YoutAB


def detect_outliers_medium(values, window_size, standard_coef):
    iter = len(values)
    j_Wind = mt.ceil(iter-window_size)+1
    S0_Wind = np.zeros((window_size))
    j = 0
    for i in range(window_size):
        l = (j + i)
        S0_Wind[i] = values[l]
        dS_standart = np.var(S0_Wind)
        scvS_standart = mt.sqrt(dS_standart)
    for j in range(j_Wind):
        for i in range(window_size):
            l = (j+i)
            S0_Wind[i] = values[l]
        mean = np.median(S0_Wind)
        variance = np.var(S0_Wind)
        standard_deviation = mt.sqrt(variance)
        if standard_deviation > (standard_coef*scvS_standart):
            values[l] = mean
    return values


def filter_detect_mnk(values, standard_coef, window_size, model):
    iter = len(values)
    j_Wind = mt.ceil(iter-window_size)+1
    S0_Wind = np.zeros((window_size))
    Speed_standart = remove_outliers_mnk(model)
    Yout_S0 = smooth_mnk(model)
    for j in range(j_Wind):
        for i in range(window_size):
            l = (j+i)
            S0_Wind[i] = values[l]
        variance = np.var(S0_Wind)
        standard_deviation = mt.sqrt(variance)
        Speed_standart_1 = abs(Speed_standart * mt.sqrt(iter))
        Speed_1 = abs(standard_coef * Speed_standart * mt.sqrt(window_size) * standard_deviation)
        if Speed_1 > Speed_standart_1:
            values[l] = Yout_S0[l, 0]
    return values


def remove_outliers_sliding_window(values, window_size):
    iter = len(values)
    j_Wind = mt.ceil(iter-window_size)+1
    S0_Wind = np.zeros((window_size))
    Midi = np.zeros((iter))
    for j in range(j_Wind):
        for i in range(window_size):
            l = (j+i)
            S0_Wind[i] = values[l]
        Midi[l] = np.median(S0_Wind)
    S0_Midi = np.zeros((iter))
    for j in range(iter):
        S0_Midi[j] = Midi[j]
    for j in range(window_size):
        S0_Midi[j] = values[j]
    return S0_Midi


if __name__ == '__main__':
    os.environ["DISPLAY_PLOTS"] = "1"

    print('Оберіть джерело вхідних даних та подальші дії:')
    print('1 - Експериментальна вибірка')
    print('2 - Реальні дані')
    Data_mode = int(input('mode:'))

    if (Data_mode == 1):
        n = 5000
        iter = int(n)
        coef_outliers = 3
        outliers_percent = 5
        anomaly_count = int((iter * outliers_percent) / 100)
        sample_mean = 0
        sigma = 10

        values = create_trend_model(n)
        outlier_indices, *o = uniform_distribution(n, iter, anomaly_count)
        sample, *o = normal_distribution(sample_mean, sigma, iter)
        norm_model = create_randomvar_model(sample, values, n)
        plot_trend_graph(values, norm_model, 'Вибірка із зашумленими даними')
        calculate_statistics(norm_model, 'Вибірка із зашумленими даними')
        model = create_random_outliers_model(values, norm_model, anomaly_count, coef_outliers, sigma, outlier_indices, sample_mean)
        plot_trend_graph(values, model, 'Вибірка з зашумленими та аномальними вимірами')
        calculate_statistics(
            model, 'Вибірка з зашумленими та аномальними вимірами')

    if (Data_mode == 2):
        file_name = input('file name:')
        column_name = input('column name:')
        model = parse_file(file_name, column_name)

        values = model
        n = len(values)
        iter = int(n)
        plot_trend_graph(model, model, 'Коливання даних з імпортованого файлу')
        calculate_statistics(
            model, 'Коливання даних з імпортованого файлу')

    print('Оберіть функціонал процесів статистиного аналізу:')

    print('1 - Фільтрація від АВ: метод medium')
    print('2 - Фільтрація від АВ: метод МНК')
    print('3 - Фільтрація від АВ: метод sliding window')
    print('4 - Рекурентне згладжування: Alpha beta фільтр')
    print('5 - Екстраполяція: метод МНК')
    print('6 - Очищення від АВ: критерій Тітʼєна Мура')

    mode = int(input('mode:'))

    if (mode == 1):
        print('Фільтрація від АВ: метод medium')
        sliding_winsize = 5
        standard_coef = 2.6
        filtered_sample_medium = detect_outliers_medium(
            model, sliding_winsize, standard_coef)
        calculate_statistics(filtered_sample_medium,
                             'Очищена від АВ вибірка: метод medium')
        Yout_SV_AV_Detect = smooth_mnk(filtered_sample_medium)
        calculate_statistics(
            Yout_SV_AV_Detect, 'Вибірка згладжена методом МНК та очищена від АВ методом medium')
        plot_trend_graph(values, filtered_sample_medium,
                'Вибірка очищена від АВ алгоритм medium')

    if (mode == 2):
        print('Фільтрація від АВ: метод МНК')
        window_size = 5
        mnk_coef = 7
        filtered_sample_mnk = filter_detect_mnk(
            model, mnk_coef, window_size, model)
        calculate_statistics(
            filtered_sample_mnk, 'Очищена від АВ вибірка: метод МНК')
        Yout_SV_AV_Detect_MNK = smooth_mnk(filtered_sample_mnk)
        calculate_statistics(Yout_SV_AV_Detect_MNK,
                             'Вибірка згладжена та очищена від АВ методом МНК')
        plot_trend_graph(values, filtered_sample_mnk, 'Очищена від АВ вибірка: метод МНК')

    if (mode == 3):
        print('Фільтрація від АВ: метод ковзне вікно')
        window_size = 5
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = smooth_mnk(filtered_sample_slidingwind)
        calculate_statistics(slidingwind_sample,
                             'Вибірка згладжена методом МНК та очищена від АВ методом ковзне вікно')
        plot_trend_graph(values, filtered_sample_slidingwind,
                'Очищена від АВ вибірка: метод ковзне вікно')

    if (mode == 4):
        print('Рекурентне згладжування: Alpha beta фільтр')
        window_size = 5
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = alpha_beta_filter(filtered_sample_slidingwind)
        calculate_statistics(slidingwind_sample,
                             'Вибірка згладжена Alpha beta фільтром та очищена від АВ методом ковзне вікно')
        plot_trend_graph(slidingwind_sample, filtered_sample_slidingwind,
                'Вибірка згладжена Alpha beta фільтром та очищена від АВ методом ковзне вікно')

    if (mode == 5):
        print('Прогнозування методом МНК')
        window_size = 5
        prediction_value = 0.5
        prediction_interval = mt.ceil(n * prediction_value)
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = mnk_extrapolation(
            filtered_sample_slidingwind, prediction_interval)
        calculate_statistics(slidingwind_sample,
                             'Прогнозування методом МНК на очищеній від АВ вибірці методом ковзне вікно')
        plot_trend_graph(slidingwind_sample, filtered_sample_slidingwind,
                'Прогнозування методом МНК на очищеній від АВ вибірці методом ковзне вікно')

    if (mode == 6):
        print('Очищення від АВ: критерій Тітʼєна Мура')
        a = tietjen_outlier_removal(model, int(0.1 * len(model)))
        print('-------- Кількість данних без аномалій ----------')
        print(len(a))
        print('-------- Аномальні виміри будуть відкинуті ----------')
        plot_trend_graph(values, a, "Очищення від АВ критерієм Тітʼєна Мура")
        calculate_statistics(a, 'Вибірка очищенна від АВ критерієм Тітʼєна Мура')
