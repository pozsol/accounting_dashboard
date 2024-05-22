import json


class DatabaseMock:
    __departments = {}
    __devices = {}
    __doctors = {}
    __examinations = {}
    __patients = {}
    __types = {}

    def __init__(self):
        with open('./database_mock_tables/departments.json') as file:
            self.__departments = json.load(file)
        with open('./database_mock_tables/devices.json') as file:
            self.__devices = json.load(file)
        with open('./database_mock_tables/doctors.json') as file:
            self.__doctors = json.load(file)
        with open('./database_mock_tables/examinations.json') as file:
            self.__examinations = json.load(file)
        with open('./database_mock_tables/patients.json') as file:
            self.__patients = json.load(file)
        with open('./database_mock_tables/types.json') as file:
            self.__types = json.load(file)

    def get_all_departments(self):
        return self.__departments

    def get_all_devices(self):
        return self.__devices

    def get_all_doctors(self):
        return self.__doctors

    def get_all_examinations(self):
        return self.__examinations

    def get_all_patients(self):
        return self.__patients

    def get_all_types(self):
        return self.__types

    def get_department_by_id(self, id_):
        return self.__departments[id_]

    def get_device_by_id(self, id_):
        return self.__devices[id_]

    def get_doctor_by_id(self, id_):
        return self.__doctors[id_]

    def get_examination_by_id(self, id_):
        return self.__examinations[id_]

    def get_patient_by_id(self, id_):
        return self.__patients[id_]

    def get_type_by_id(self, id_):
        return self.__types[id_]
