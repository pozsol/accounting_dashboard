from backend.composition.department_metrics_composer import DepartmentMetricsComposer
from backend.composition.device_metrics_composer import DeviceMetricsComposer
from backend.composition.doctor_metrics_composer import DoctorMetricsComposer
from backend.composition.type_metrics_composer import TypeMetricsComposer
from backend.prediction.past_data_getter import PastDataGetter
from backend.prediction.models.linear_regression_model import LinearRegressionModel
from backend.prediction.models.facebook_prophet_model import FacebookProphetModel

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from PIL import ImageGrab
import datetime


class Endpoints:
    __database_mock = None
    __department_metrics_composer = None
    __device_metrics_composer = None
    __doctor_metrics_composer = None
    __type_metrics_composer = None
    __department_metrics = None
    __device_metrics = None
    __doctor_metrics = None
    __type_metrics = None
    __past_data_getter = None
    __linear_regression_model = None
    __facebook_prophet_model = None

    __DEPARTMENT_METRICS_LABELS = ['Grade', 'Number of examinations', 'Number of patients', 'Number of doctors',
                                   'Duration of examinations', 'Generated revenues',
                                   'Generated revenues per examination', 'Generated revenues per hour',
                                   'Generated revenues per number of doctors',
                                   'Generated revenues per number of doctors per hour']
    __DEVICE_METRICS_LABELS = ['Grade', 'Number of examinations', 'Number of patients', 'Number of doctors',
                               'Duration of examinations', 'Generated revenues', 'Generated revenues per examination',
                               'Generated revenues per hour']
    __DOCTOR_METRICS_LABELS = ['Grade', 'Number of examinations', 'Number of patients', 'Duration of examinations',
                               'Generated revenues', 'Generated revenues per examination',
                               'Generated revenues per hour']
    __TYPE_METRICS_LABELS = ['Grade', 'Number of examinations', 'Number of patients', 'Number of doctors',
                             'Duration of examinations', 'Generated revenues', 'Generated revenues per examination',
                             'Generated revenues per hour']

    def __init__(self, database_mock):
        self.__database_mock = database_mock
        self.__department_metrics_composer = DepartmentMetricsComposer(database_mock)
        self.__device_metrics_composer = DeviceMetricsComposer(database_mock)
        self.__doctor_metrics_composer = DoctorMetricsComposer(database_mock)
        self.__type_metrics_composer = TypeMetricsComposer(database_mock)
        self.__department_metrics = self.__department_metrics_composer.get_composed_department_metrics()
        self.__device_metrics = self.__device_metrics_composer.get_composed_device_metrics()
        self.__doctor_metrics = self.__doctor_metrics_composer.get_composed_doctor_metrics()
        self.__type_metrics = self.__type_metrics_composer.get_composed_type_metrics()
        self.__past_data_getter = PastDataGetter(database_mock)
        self.__linear_regression_model = LinearRegressionModel()
        self.__facebook_prophet_model = FacebookProphetModel()

    def get_modes(self):
        modes = ['Departments', 'Devices', 'Doctors', 'Types']
        return modes

    def get_entity_list(self, mode):
        match mode:
            case 'Departments':
                entities = self.__database_mock.get_all_departments()
            case 'Devices':
                entities = self.__database_mock.get_all_devices()
            case 'Doctors':
                entities = self.__database_mock.get_all_doctors()
            case 'Types':
                entities = self.__database_mock.get_all_types()
        entity_list = []
        entity_ids = entities.keys()
        for entity_id in entity_ids:
            entity = entities[entity_id]
            name = entity['name']
            entity_list.append(name + ' [id: ' + entity_id + ']')
        return entity_list

    def __extract_id(self, entity):
        id_ = str(entity).split('[')[1][4:-1]
        return id_

    def get_entity_details(self, mode, entity):
        id_ = self.__extract_id(entity)
        match mode:
            case 'Departments':
                department_metrics = self.__department_metrics[id_]
                entity_details = pd.DataFrame(
                    [
                        department_metrics['grade'],
                        department_metrics['number_of_examinations'],
                        department_metrics['number_of_patients'],
                        department_metrics['number_of_doctors'],
                        department_metrics['duration_of_examinations'],
                        department_metrics['generated_revenues'],
                        department_metrics['generated_revenues_per_examination'],
                        department_metrics['generated_revenues_per_hour'],
                        department_metrics['generated_revenues_per_number_of_doctors'],
                        department_metrics['generated_revenues_per_number_of_doctors_per_hour']
                    ],
                    self.__DEPARTMENT_METRICS_LABELS
                )
            case 'Devices':
                device_metrics = self.__device_metrics[id_]
                entity_details = pd.DataFrame(
                    [
                        device_metrics['grade'],
                        device_metrics['number_of_examinations'],
                        device_metrics['number_of_patients'],
                        device_metrics['number_of_doctors'],
                        device_metrics['duration_of_examinations'],
                        device_metrics['generated_revenues'],
                        device_metrics['generated_revenues_per_examination'],
                        device_metrics['generated_revenues_per_hour']
                    ],
                    self.__DEVICE_METRICS_LABELS
                )
            case 'Doctors':
                doctor_metrics = self.__doctor_metrics[id_]
                entity_details = pd.DataFrame(
                    [
                        doctor_metrics['grade'],
                        doctor_metrics['number_of_examinations'],
                        doctor_metrics['number_of_patients'],
                        doctor_metrics['duration_of_examinations'],
                        doctor_metrics['generated_revenues'],
                        doctor_metrics['generated_revenues_per_examination'],
                        doctor_metrics['generated_revenues_per_hour']
                    ],
                    self.__DOCTOR_METRICS_LABELS
                )
            case 'Types':
                type_metrics = self.__type_metrics[id_]
                entity_details = pd.DataFrame(
                    [
                        type_metrics['grade'],
                        type_metrics['number_of_examinations'],
                        type_metrics['number_of_patients'],
                        type_metrics['number_of_doctors'],
                        type_metrics['duration_of_examinations'],
                        type_metrics['generated_revenues'],
                        type_metrics['generated_revenues_per_examination'],
                        type_metrics['generated_revenues_per_hour']
                    ],
                    self.__TYPE_METRICS_LABELS
                )
        entity_details = entity_details.set_axis([''], axis=1)
        return entity_details

    def __format_past_data_for_plot(self, data_past):
        dates_past = data_past.keys()
        dates_past = sorted(dates_past)
        revenues_past = []
        for date in dates_past:
            revenues_past.append(data_past[date])
        return dates_past, revenues_past

    def get_fig(self, mode, entity, date_from, date_to, model, date_prediction):
        id_ = self.__extract_id(entity)
        data_past = self.__past_data_getter.get_past_data(mode, id_, date_from, date_to)
        matplotlib.use('agg')
        fig, ax = plt.subplots()
        dates_past, revenues_past = self.__format_past_data_for_plot(data_past)
        match model:
            case 'None':
                ax.plot(dates_past, revenues_past, color='green')
            case 'Model 1':
                dates_future, revenues_future = self.__linear_regression_model.get_prediction(data_past, date_prediction)
                ax.plot(dates_past, revenues_past, color='green')
                ax.plot(dates_future, revenues_future, color='orange')
            case 'Model 2':
                dates_future, revenues_future = self.__facebook_prophet_model.get_prediction(data_past, date_prediction)
                ax.plot(dates_past, revenues_past, color='green')
                ax.plot(dates_future, revenues_future, color='red')
        plt.xlabel('Date')
        plt.ylabel('Generated revenue')
        plt.close(fig)
        return fig

    def get_metrics_table(self, mode):
        match mode:
            case 'Departments':
                department_metrics = self.__department_metrics
                metrics = {}
                department_ids = department_metrics.keys()
                for department_id in department_ids:
                    department = self.__database_mock.get_department_by_id(department_id)
                    name = department['name']
                    new_key = name + ' [id: ' + department_id + ']'
                    metrics[new_key] = department_metrics[department_id]
                metrics_table = pd.DataFrame.from_dict(metrics)
                metrics_table = metrics_table.transpose()
                metrics_table.columns = self.__DEPARTMENT_METRICS_LABELS
                metrics_table.rename_axis('Name', inplace=True)
            case 'Devices':
                device_metrics = self.__device_metrics
                metrics = {}
                device_ids = device_metrics.keys()
                for device_id in device_ids:
                    device = self.__database_mock.get_device_by_id(device_id)
                    name = device['name']
                    new_key = name + ' [id: ' + device_id + ']'
                    metrics[new_key] = device_metrics[device_id]
                metrics_table = pd.DataFrame.from_dict(metrics)
                metrics_table = metrics_table.transpose()
                metrics_table.columns = self.__DEVICE_METRICS_LABELS
                metrics_table.rename_axis('Name', inplace=True)
            case 'Doctors':
                doctor_metrics = self.__doctor_metrics
                metrics = {}
                doctor_ids = doctor_metrics.keys()
                for doctor_id in doctor_ids:
                    doctor = self.__database_mock.get_doctor_by_id(doctor_id)
                    name = doctor['name']
                    new_key = name + ' [id: ' + doctor_id + ']'
                    metrics[new_key] = doctor_metrics[doctor_id]
                metrics_table = pd.DataFrame.from_dict(metrics)
                metrics_table = metrics_table.transpose()
                metrics_table.columns = self.__DOCTOR_METRICS_LABELS
                metrics_table.rename_axis('Name', inplace=True)
            case 'Types':
                type_metrics = self.__type_metrics
                metrics = {}
                type_ids = type_metrics.keys()
                for type_id in type_ids:
                    type = self.__database_mock.get_type_by_id(type_id)
                    name = type['name']
                    new_key = name + ' [id: ' + type_id + ']'
                    metrics[new_key] = type_metrics[type_id]
                metrics_table = pd.DataFrame.from_dict(metrics)
                metrics_table = metrics_table.transpose()
                metrics_table.columns = self.__TYPE_METRICS_LABELS
                metrics_table.rename_axis('Name', inplace=True)
        return metrics_table

    def generate_report(self, event):
        report = ImageGrab.grab()
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d_%H-%M-%S')
        path = './reports/report_' + now + '.png'
        report.save(path)
