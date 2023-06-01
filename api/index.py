import os
from flask import Flask, request, jsonify
from package.index import *
import matplotlib

app = Flask(__name__)

matplotlib.pyplot.switch_backend('Agg')

os.environ["DISPLAY_PLOTS"] = "0"

@app.route('/first-step', methods=['POST'])
def first_step():
    request_data = request.get_json()
    mode = int(request_data["mode"])

    charts = []
    stats = []

    if (mode == 1):
        n = 5000
        iter = int(n)  
        coef_outliers = 3  
        outliers_percent = 5
        anomaly_count = int((iter * outliers_percent) / 100)
        sample_mean = 0
        sigma = 10  

        values = create_trend_model(n)  
        outlier_indices, html1, stats1 = uniform_distribution(n, iter, anomaly_count)
        sample, html2, stats2 = normal_distribution(sample_mean, sigma, iter)
        norm_model = create_randomvar_model(sample, values, n)
        html3 = plot_trend_graph(values, norm_model, 'Вибірка із зашумленими даними')
        stats3 = calculate_statistics(norm_model, 'Вибірка із зашумленими даними')
        model = create_random_outliers_model(values, norm_model, anomaly_count, coef_outliers, sigma, outlier_indices, sample_mean)
        html4 = plot_trend_graph(values, model, 'Вибірка із зашумленими та аномальними вимірами')
        stats4 = calculate_statistics(model, 'Вибірка із зашумленими та аномальними вимірами')

        charts = [html1, html2, html3, html4]
        stats = [stats1, stats2, stats3, stats4]

    if (mode == 2):

        print(request_data["sv_av"])
        model = np.array(request_data["sv_av"], dtype=np.float64)

        values = model
        n = len(values)
        iter = int(n)  
        html1 = plot_trend_graph(model, model, 'Коливання величин з імпортованого файлу')
        stats1 = calculate_statistics(
            model, 'Коливання величин з імпортованого файлу')
        
        charts = [html1]
        stats = [stats1]

    return jsonify(charts=charts, stats=stats, sv_av=model.tolist(), values=values.tolist()), 200


@app.route('/second-step', methods=['POST'])
def second_step():
    request_data = request.get_json()
    mode = int(request_data["mode"])

    model = np.array(request_data["sv_av"].split(','), dtype=np.float64)
    values= np.array(request_data["values"].split(','), dtype=np.float64)
    n = len(model)

    chart = ''
    stats2 = '';

    if (mode == 1):
        sliding_winsize = 5  
        standard_coef = 2.6
        filtered_sample_medium = detect_outliers_medium(
            model, sliding_winsize, standard_coef)
        stats1=calculate_statistics(filtered_sample_medium,
                             'Очищена від АВ вибірка: метод medium')
        Yout_SV_AV_Detect = smooth_mnk(filtered_sample_medium)
        stats2=calculate_statistics(
            Yout_SV_AV_Detect, 'Вибірка згладжена методом МНК та очищена від АВ методом medium')

        chart=plot_trend_graph(values, filtered_sample_medium,
                'Вибірка очищена від АВ алгоритм medium')

    if (mode == 2):
        window_size = 5  
        mnk_coef = 7  
        filtered_sample_mnk = filter_detect_mnk(model, mnk_coef, window_size, model)
        stats1=calculate_statistics(
            filtered_sample_mnk, 'Очищена від АВ вибірка: метод МНК')
        Yout_SV_AV_Detect_MNK = smooth_mnk(filtered_sample_mnk)
        stats2=calculate_statistics(Yout_SV_AV_Detect_MNK,
                             'Вибірка згладжена та очищена від АВ методом МНК')
        chart=plot_trend_graph(values, filtered_sample_mnk, 'Очищена від АВ вибірка: метод МНК')

    if (mode == 3):
        window_size = 5  
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        stats1=calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = smooth_mnk(filtered_sample_slidingwind)
        stats2=calculate_statistics(slidingwind_sample,
                             'Вибірка згладжена методом МНК та очищена від АВ методом ковзне вікно')
        chart=plot_trend_graph(values, filtered_sample_slidingwind,
                'Очищена від АВ вибірка: метод ковзне вікно')

    if (mode == 4):
        window_size = 5  
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        stats1=calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = alpha_beta_filter(filtered_sample_slidingwind)
        stats2=calculate_statistics(slidingwind_sample,
                             'Вибірка згладжена Alpha beta фільтром та очищена від АВ методом ковзне вікно')
        chart=plot_trend_graph(slidingwind_sample, filtered_sample_slidingwind,
                'Вибірка згладжена Alpha beta фільтром та очищена від АВ методом ковзне вікно')

    if (mode == 5):
        window_size = 5  
        prediction_value = 0.5
        prediction_interval = mt.ceil(n * prediction_value)
        filtered_sample_slidingwind = remove_outliers_sliding_window(
            model, window_size)
        stats1=calculate_statistics(filtered_sample_slidingwind,
                             'Очищена від АВ вибірка: метод ковзне вікно')
        slidingwind_sample = mnk_extrapolation(
            filtered_sample_slidingwind, prediction_interval)
        stats2=calculate_statistics(slidingwind_sample,
                             'Прогнозування методом МНК на очищеній від АВ вибірці методом ковзне вікно')
        chart=plot_trend_graph(slidingwind_sample, filtered_sample_slidingwind,
                'Прогнозування методом МНК на очищеній від АВ вибірці методом ковзне вікно')

    if (mode == 6):
        a = tietjen_outlier_removal(model, int(0.1 * len(model)))
        
        chart=plot_trend_graph(values, a, "Очищення від АВ критерієм Тітʼєна Мура")
        stats1=calculate_statistics(a, 'Очищена від АВ вибірка критерієм Тітʼєна Мура')

    stats=[stats1]

    if stats2 != '':
        stats.append(stats2)

    return jsonify(chart=chart, stats=stats, sv_av=model.tolist()), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
