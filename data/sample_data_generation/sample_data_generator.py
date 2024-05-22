import random
import calendar
import datetime
import json


class SampleDataGenerator:

    __FIRST_NAMES = [
        'Maria', 'Ruth', 'Ursula', 'Elizabeth', 'Monika', 'Beat', 'Marianne', 'Barbara', 'Margit', 'Christine', 'Heidi',
        'Sandra', 'Brigitte', 'Andrea', 'Claudia', 'Susanne', 'Silvia', 'Karin', 'Nicole', 'Verena', 'Rita', 'Doris',
        'Erika', 'Esther', 'Daniela',

        'Peter', 'Hans', 'Daniel', 'Thomas', 'Walter', 'Markus', 'Martin', 'Christian', 'Urs', 'Andreas', 'Werner',
        'Bruno', 'René', 'Kurt', 'Roland', 'Paul', 'Josef', 'Heinz', 'Stefan', 'Marcel', 'Ernst', 'Rolf', 'Michael',
        'Patrick', 'Robert'
    ]

    __LAST_NAMES = [
        'Müller', 'Meier', 'Schmid', 'Keller', 'Weber', 'Schneider', 'Huber', 'Meyer', 'Steiner', 'Fischer', 'Baumann',
        'Frei', 'Brunner', 'Gerber', 'Widmer', 'Zimmermann', 'Moser', 'Graf', 'Wyss', 'Roth', 'Suter', 'Baumgartner',
        'Bachmann', 'Studer', 'Bucher'
    ]

    __DEPARTMENTS = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z'
    ]

    __patients = {}
    __departments = {}
    __doctors = {}
    __types = {}
    __devices = {}
    __examinations = {}

    def __generate_patients(self, number_of_patients):
        patients = {}
        for i in range(number_of_patients):
            id_ = i + 1
            first_name = random.choice(self.__FIRST_NAMES)
            last_name = random.choice(self.__LAST_NAMES)
            full_name = first_name + ' ' + last_name
            examination_ids = []
            patients[id_] = {'name': full_name, 'examination_ids': examination_ids}
        self.__patients = patients

    def __generate_departments(self, number_of_departments):
        departments = {}
        if number_of_departments > 26:
            number_of_departments = 26
        for i in range(number_of_departments):
            id_ = i + 1
            name = self.__DEPARTMENTS[i]
            full_name = 'Department ' + name
            doctor_ids = []
            departments[id_] = {'name': full_name, 'doctor_ids': doctor_ids}
        self.__departments = departments

    def __generate_doctors(self, number_of_doctors):
        doctors = {}
        for i in range(number_of_doctors):
            id_ = i + 1
            first_name = random.choice(self.__FIRST_NAMES)
            last_name = random.choice(self.__LAST_NAMES)
            full_name = 'Dr. med. ' + first_name + ' ' + last_name
            department_id = random.choice(list(self.__departments.keys()))
            examination_ids = []
            doctors[id_] = {'name': full_name, 'department_id': department_id, 'examination_ids': examination_ids}
            self.__departments[department_id]['doctor_ids'].append(id_)
        self.__doctors = doctors

    def __generate_types(self, number_of_types):
        types = {}
        min_price = 10
        max_price = 250
        for i in range(number_of_types):
            id_ = i + 1
            name = 'Type ' + str(id_)
            price = random.randint(min_price, max_price)
            examination_ids = []
            types[id_] = {'name': name, 'price': price, 'examination_ids': examination_ids}
        self.__types = types

    def __generate_devices(self, number_of_devices):
        devices = {}
        for i in range(number_of_devices):
            id_ = i + 1
            name = 'Device ' + str(id_)
            examination_ids = []
            devices[id_] = {'name': name, 'examination_ids': examination_ids}
        self.__devices = devices

    def __generate_examinations(self, number_of_examinations):
        examinations = {}
        for i in range(number_of_examinations):
            id_ = i + 1
            year = 2023
            month = random.randint(1, 12)
            day = random.randint(1, calendar.monthrange(year, month)[1])
            hour = random.randint(8, 18)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            date_start = datetime.datetime(year, month, day, hour, minute, second)
            duration = random.randint(600, 3600)
            date_end = date_start + datetime.timedelta(seconds=duration)
            patient_id = random.choice(list(self.__patients.keys()))
            doctor_id = random.choice(list(self.__doctors.keys()))
            type_id = random.choice(list(self.__types.keys()))
            device_id = random.choice(list(self.__devices.keys()))
            examinations[id_] = {'date_start': date_start, 'date_end': date_end, 'patient_id': patient_id,
                                 'doctor_id': doctor_id, 'type_id': type_id, 'device_id': device_id}
            self.__patients[patient_id]['examination_ids'].append(id_)
            self.__doctors[doctor_id]['examination_ids'].append(id_)
            self.__types[type_id]['examination_ids'].append(id_)
            self.__devices[device_id]['examination_ids'].append(id_)
        self.__examinations = examinations

    def __write_to_file(self):
        with open('./database_mock_tables/patients.json', 'w') as file:
            json.dump(self.__patients, file, default=str, indent=4)
        with open('./database_mock_tables/departments.json', 'w') as file:
            json.dump(self.__departments, file, default=str, indent=4)
        with open('./database_mock_tables/doctors.json', 'w') as file:
            json.dump(self.__doctors, file, default=str, indent=4)
        with open('./database_mock_tables/types.json', 'w') as file:
            json.dump(self.__types, file, default=str, indent=4)
        with open('./database_mock_tables/devices.json', 'w') as file:
            json.dump(self.__devices, file, default=str, indent=4)
        with open('./database_mock_tables/examinations.json', 'w') as file:
            json.dump(self.__examinations, file, default=str, indent=4)

    def generate_sample_data(self, number_of_patients, number_of_departments, number_of_doctors,
                             number_of_types, number_of_devices, number_of_examinations):
        self.__generate_patients(number_of_patients)
        self.__generate_departments(number_of_departments)
        self.__generate_doctors(number_of_doctors)
        self.__generate_types(number_of_types)
        self.__generate_devices(number_of_devices)
        self.__generate_examinations(number_of_examinations)
        self.__write_to_file()
