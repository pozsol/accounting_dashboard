import datetime


class DoctorMetrics:
    __database_mock = None

    def __init__(self, database_mock):
        self.__database_mock = database_mock

    def calculate_number_of_examinations(self):
        doctors = self.__database_mock.get_all_doctors()
        number_of_examinations = {}
        doctor_ids = doctors.keys()
        for doctor_id in doctor_ids:
            doctor = doctors[doctor_id]
            examination_ids = doctor['examination_ids']
            number_of_examinations[doctor_id] = len(examination_ids)
        return number_of_examinations

    def calculate_number_of_patients(self):
        doctors = self.__database_mock.get_all_doctors()
        patient_ids = {}
        doctor_ids = doctors.keys()
        for doctor_id in doctor_ids:
            doctor = doctors[doctor_id]
            examination_ids = doctor['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                patient_id = examination['patient_id']
                if doctor_id in patient_ids:
                    patient_ids[doctor_id].add(patient_id)
                else:
                    patient_ids[doctor_id] = {patient_id}
        number_of_patients = {}
        for doctor_id in patient_ids:
            number_of_patients[doctor_id] = len(patient_ids[doctor_id])
        return number_of_patients

    def calculate_duration_of_examinations(self):
        doctors = self.__database_mock.get_all_doctors()
        duration_of_examinations = {}
        doctor_ids = doctors.keys()
        for doctor_id in doctor_ids:
            doctor = doctors[doctor_id]
            examination_ids = doctor['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
                date_end = datetime.datetime.strptime(examination['date_end'], '%Y-%m-%d %H:%M:%S')
                duration = date_end - date_start
                if doctor_id in duration_of_examinations:
                    duration_of_examinations[doctor_id] += duration
                else:
                    duration_of_examinations[doctor_id] = duration
        for doctor_id in duration_of_examinations:
            duration = duration_of_examinations[doctor_id].seconds / 3600
            duration_of_examinations[doctor_id] = duration
        return duration_of_examinations

    def calculate_generated_revenues(self):
        doctors = self.__database_mock.get_all_doctors()
        generated_revenues = {}
        doctor_ids = doctors.keys()
        for doctor_id in doctor_ids:
            doctor = doctors[doctor_id]
            examination_ids = doctor['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                type_id = examination['type_id']
                type_ = self.__database_mock.get_type_by_id(str(type_id))
                price = type_['price']
                if doctor_id in generated_revenues:
                    generated_revenues[doctor_id] += price
                else:
                    generated_revenues[doctor_id] = price
        return generated_revenues

    def calculate_generated_revenues_per_examination(self):
        generated_revenues = self.calculate_generated_revenues()
        number_of_examinations = self.calculate_number_of_examinations()
        generated_revenues_per_examination = {}
        doctor_ids = generated_revenues.keys()
        for doctor_id in doctor_ids:
            revenue = generated_revenues[doctor_id]
            number = number_of_examinations[doctor_id]
            generated_revenues_per_examination[doctor_id] = revenue / number
        return generated_revenues_per_examination

    def calculate_generated_revenues_per_hour(self):
        generated_revenues = self.calculate_generated_revenues()
        duration_of_examinations = self.calculate_duration_of_examinations()
        generated_revenues_per_hour = {}
        doctor_ids = generated_revenues.keys()
        for doctor_id in doctor_ids:
            revenue = generated_revenues[doctor_id]
            hours = duration_of_examinations[doctor_id]
            generated_revenues_per_hour[doctor_id] = revenue / hours
        return generated_revenues_per_hour
