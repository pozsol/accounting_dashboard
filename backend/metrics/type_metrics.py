import datetime


class TypeMetrics:
    __database_mock = None

    def __init__(self, database_mock):
        self.__database_mock = database_mock

    def calculate_number_of_examinations(self):
        types = self.__database_mock.get_all_types()
        number_of_examinations = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            examination_ids = type_['examination_ids']
            number_of_examinations[type_id] = len(examination_ids)
        return number_of_examinations

    def calculate_number_of_patients(self):
        types = self.__database_mock.get_all_types()
        patient_ids = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            examination_ids = type_['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                patient_id = examination['patient_id']
                if type_id in patient_ids:
                    patient_ids[type_id].add(patient_id)
                else:
                    patient_ids[type_id] = {patient_id}
        number_of_patients = {}
        for type_id in patient_ids:
            number_of_patients[type_id] = len(patient_ids[type_id])
        return number_of_patients

    def calculate_number_of_doctors(self):
        types = self.__database_mock.get_all_types()
        doctor_ids = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            examination_ids = type_['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                doctor_id = examination['doctor_id']
                if type_id in doctor_ids:
                    doctor_ids[type_id].add(doctor_id)
                else:
                    doctor_ids[type_id] = {doctor_id}
        number_of_doctors = {}
        for type_id in doctor_ids:
            number_of_doctors[type_id] = len(doctor_ids[type_id])
        return number_of_doctors

    def calculate_duration_of_examinations(self):
        types = self.__database_mock.get_all_types()
        duration_of_examinations = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            examination_ids = type_['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
                date_end = datetime.datetime.strptime(examination['date_end'], '%Y-%m-%d %H:%M:%S')
                duration = date_end - date_start
                if type_id in duration_of_examinations:
                    duration_of_examinations[type_id] += duration
                else:
                    duration_of_examinations[type_id] = duration
        for type_id in duration_of_examinations:
            duration = duration_of_examinations[type_id].seconds / 3600
            duration_of_examinations[type_id] = duration
        return duration_of_examinations

    def calculate_generated_revenues(self):
        types = self.__database_mock.get_all_types()
        number_of_examinations = self.calculate_number_of_examinations()
        generated_revenues = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            price = type_['price']
            generated_revenues[type_id] = price * number_of_examinations[type_id]
        return generated_revenues

    def calculate_generated_revenues_per_examination(self):
        types = self.__database_mock.get_all_types()
        generated_revenues_per_examination = {}
        type_ids = types.keys()
        for type_id in type_ids:
            type_ = types[type_id]
            price = type_['price']
            generated_revenues_per_examination[type_id] = price
        return generated_revenues_per_examination

    def calculate_generated_revenues_per_hour(self):
        generated_revenues = self.calculate_generated_revenues()
        duration_of_examinations = self.calculate_duration_of_examinations()
        generated_revenues_per_hour = {}
        type_ids = generated_revenues.keys()
        for type_id in type_ids:
            revenue = generated_revenues[type_id]
            hours = duration_of_examinations[type_id]
            generated_revenues_per_hour[type_id] = revenue / hours
        return generated_revenues_per_hour
