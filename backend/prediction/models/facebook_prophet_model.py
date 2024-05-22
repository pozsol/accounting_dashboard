import pandas as pd
from prophet import Prophet


class FacebookProphetModel:

    def __process_past_data_for_model(self, data_past):
        dates = data_past.keys()
        dates = sorted(dates)
        revenues = []
        for date in dates:
            revenues.append(data_past[date])
        data_processed = {'ds': dates, 'y': revenues}
        data_processed = pd.DataFrame(data_processed)
        return data_processed

    def __format_future_data_for_plot(self, data_future, periods):
        dates = data_future['ds'].tolist()
        revenues = data_future['yhat'].tolist()
        dates_future = dates[-periods:]
        revenues_future = revenues[-periods:]
        return dates_future, revenues_future

    def get_prediction(self, data_past, date_prediction):
        data_processed = self.__process_past_data_for_model(data_past)
        periods = date_prediction - data_processed.iloc[-1]['ds']
        periods = periods.days
        model = Prophet()
        model.fit(data_processed)
        future_dataframe = model.make_future_dataframe(periods=periods)
        data_future = model.predict(future_dataframe)
        dates_future, revenues_future = self.__format_future_data_for_plot(data_future, periods)
        return dates_future, revenues_future
