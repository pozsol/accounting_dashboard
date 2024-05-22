import datetime
import numpy as np
from sklearn.linear_model import LinearRegression


class LinearRegressionModel:

    def __process_past_data_for_model(self, data_past):
        dates = data_past.keys()
        dates = sorted(dates)
        x_past = []
        counter = 0
        revenues = []
        for date in dates:
            x_past.append(counter)
            counter += 1
            revenues.append(data_past[date])
        x_past = np.array(x_past).reshape(-1, 1)
        y_past = np.array(revenues).reshape(-1, 1)
        return x_past, y_past

    def __get_x_future_for_model(self, number_of_past_x, date_last, date_prediction):
        number_of_x_future = (date_prediction - date_last).days
        future_x = []
        sample = number_of_past_x
        for i in range(number_of_x_future):
            future_x.append(sample)
            sample += 1
        future_x = np.array(future_x).reshape(-1, 1)
        return future_x

    def __format_future_data_for_plot(self, y_future, date_last):
        dates_future = []
        revenues_future = []
        date_future = date_last
        for y in y_future:
            date_future = date_future + datetime.timedelta(days=1)
            dates_future.append(date_future)
            revenues_future.append(y)
        return dates_future, revenues_future

    def get_prediction(self, data_past, date_prediction):
        x_past, y_past = self.__process_past_data_for_model(data_past)
        model = LinearRegression()
        model.fit(x_past, y_past)
        number_of_past_x = len(data_past)
        date_last = sorted(data_past.keys())[-1]
        x_future = self.__get_x_future_for_model(number_of_past_x, date_last, date_prediction)
        y_future = model.predict(x_future)
        dates_future, revenues_future = self.__format_future_data_for_plot(y_future, date_last)
        return dates_future, revenues_future
