import datetime


class PastDataGetter:
    __database_mock = None

    def __init__(self, database_mock):
        self.__database_mock = database_mock

    def __get_department_data(self, department_id):
        department_data = {}
        department = self.__database_mock.get_department_by_id(str(department_id))
        doctor_ids = department['doctor_ids']
        for doctor_id in doctor_ids:
            doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
            examination_ids = doctor['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
                date = date_start.date()
                type_id = examination['type_id']
                type_ = self.__database_mock.get_type_by_id(str(type_id))
                price = type_['price']
                if date in department_data:
                    department_data[date] += price
                else:
                    department_data[date] = price
        return department_data

    def __get_device_data(self, device_id):
        device_data = {}
        device = self.__database_mock.get_device_by_id(str(device_id))
        examination_ids = device['examination_ids']
        for examination_id in examination_ids:
            examination = self.__database_mock.get_examination_by_id(str(examination_id))
            date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
            date = date_start.date()
            type_id = examination['type_id']
            type_ = self.__database_mock.get_type_by_id(str(type_id))
            price = type_['price']
            if date in device_data:
                device_data[date] += price
            else:
                device_data[date] = price
        return device_data

    def __get_doctor_data(self, doctor_id):
        doctor_data = {}
        doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
        examination_ids = doctor['examination_ids']
        for examination_id in examination_ids:
            examination = self.__database_mock.get_examination_by_id(str(examination_id))
            date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
            date = date_start.date()
            type_id = examination['type_id']
            type_ = self.__database_mock.get_type_by_id(str(type_id))
            price = type_['price']
            if date in doctor_data:
                doctor_data[date] += price
            else:
                doctor_data[date] = price
        return doctor_data

    def __get_type_data(self, type_id):
        type_data = {}
        type_ = self.__database_mock.get_type_by_id(str(type_id))
        price = type_['price']
        examination_ids = type_['examination_ids']
        for examination_id in examination_ids:
            examination = self.__database_mock.get_examination_by_id(str(examination_id))
            date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
            date = date_start.date()
            if date in type_data:
                type_data[date] += price
            else:
                type_data[date] = price
        return type_data

    def __filter_data(self, data_unfiltered, date_from, date_to):
        data_filtered = {}
        dates = data_unfiltered.keys()
        for date in dates:
            if date_from <= date <= date_to:
                data_filtered[date] = data_unfiltered[date]
        return data_filtered

    def get_past_data(self, mode, id_, date_from, date_to):
        match mode:
            case 'Departments':
                past_data_unfiltered = self.__get_department_data(id_)
            case 'Devices':
                past_data_unfiltered = self.__get_device_data(id_)
            case 'Doctors':
                past_data_unfiltered = self.__get_doctor_data(id_)
            case 'Types':
                past_data_unfiltered = self.__get_type_data(id_)
        past_data_filtered = self.__filter_data(past_data_unfiltered, date_from, date_to)
        return past_data_filtered
