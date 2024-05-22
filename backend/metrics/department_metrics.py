import datetime


class DepartmentMetrics:
    __database_mock = None

    def __init__(self, database_mock):
        self.__database_mock = database_mock

    def calculate_number_of_examinations(self):
        departments = self.__database_mock.get_all_departments()
        number_of_examinations = {}
        department_ids = departments.keys()
        for department_id in department_ids:
            department = departments[department_id]
            doctor_ids = department['doctor_ids']
            for doctor_id in doctor_ids:
                doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
                examination_ids = doctor['examination_ids']
                if department_id in number_of_examinations:
                    number_of_examinations[department_id] += len(examination_ids)
                else:
                    number_of_examinations[department_id] = len(examination_ids)
        return number_of_examinations

    def calculate_number_of_patients(self):
        departments = self.__database_mock.get_all_departments()
        patient_ids = {}
        department_ids = departments.keys()
        for department_id in department_ids:
            department = departments[department_id]
            doctor_ids = department['doctor_ids']
            for doctor_id in doctor_ids:
                doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
                examination_ids = doctor['examination_ids']
                for examination_id in examination_ids:
                    examination = self.__database_mock.get_examination_by_id(str(examination_id))
                    patient_id = examination['patient_id']
                    if department_id in patient_ids:
                        patient_ids[department_id].add(patient_id)
                    else:
                        patient_ids[department_id] = {patient_id}
        number_of_patients = {}
        for department_id in patient_ids:
            number_of_patients[department_id] = len(patient_ids[department_id])
        return number_of_patients

    def calculate_number_of_doctors(self):
        departments = self.__database_mock.get_all_departments()
        number_of_doctors = {}
        department_ids = departments.keys()
        for department_id in department_ids:
            department = departments[department_id]
            doctor_ids = department['doctor_ids']
            number_of_doctors[department_id] = len(doctor_ids)
        return number_of_doctors

    def calculate_duration_of_examinations(self):
        departments = self.__database_mock.get_all_departments()
        duration_of_examinations = {}
        department_ids = departments.keys()
        for department_id in department_ids:
            department = departments[department_id]
            doctor_ids = department['doctor_ids']
            for doctor_id in doctor_ids:
                doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
                examination_ids = doctor['examination_ids']
                for examination_id in examination_ids:
                    examination = self.__database_mock.get_examination_by_id(str(examination_id))
                    date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
                    date_end = datetime.datetime.strptime(examination['date_end'], '%Y-%m-%d %H:%M:%S')
                    duration = date_end - date_start
                    if department_id in duration_of_examinations:
                        duration_of_examinations[department_id] += duration
                    else:
                        duration_of_examinations[department_id] = duration
        for department_id in duration_of_examinations:
            duration = duration_of_examinations[department_id].seconds / 3600
            duration_of_examinations[department_id] = duration
        return duration_of_examinations

    def calculate_generated_revenues(self):
        departments = self.__database_mock.get_all_departments()
        generated_revenues = {}
        department_ids = departments.keys()
        for department_id in department_ids:
            department = departments[department_id]
            doctor_ids = department['doctor_ids']
            for doctor_id in doctor_ids:
                doctor = self.__database_mock.get_doctor_by_id(str(doctor_id))
                examination_ids = doctor['examination_ids']
                for examination_id in examination_ids:
                    examination = self.__database_mock.get_examination_by_id(str(examination_id))
                    type_id = examination['type_id']
                    type_ = self.__database_mock.get_type_by_id(str(type_id))
                    price = type_['price']
                    if department_id in generated_revenues:
                        generated_revenues[department_id] += price
                    else:
                        generated_revenues[department_id] = price
        return generated_revenues

    def calculate_generated_revenues_per_examination(self):
        generated_revenues = self.calculate_generated_revenues()
        number_of_examinations = self.calculate_number_of_examinations()
        generated_revenues_per_examination = {}
        department_ids = generated_revenues.keys()
        for department_id in department_ids:
            revenue = generated_revenues[department_id]
            number = number_of_examinations[department_id]
            generated_revenues_per_examination[department_id] = revenue / number
        return generated_revenues_per_examination

    def calculate_generated_revenues_per_hour(self):
        generated_revenues = self.calculate_generated_revenues()
        duration_of_examinations = self.calculate_duration_of_examinations()
        generated_revenues_per_hour = {}
        department_ids = generated_revenues.keys()
        for department_id in department_ids:
            revenue = generated_revenues[department_id]
            hours = duration_of_examinations[department_id]
            generated_revenues_per_hour[department_id] = revenue / hours
        return generated_revenues_per_hour

    def calculate_generated_revenues_per_number_of_doctors(self):
        generated_revenues = self.calculate_generated_revenues()
        number_of_doctors = self.calculate_number_of_doctors()
        generated_revenues_per_number_of_doctors = {}
        department_ids = generated_revenues.keys()
        for department_id in department_ids:
            revenue = generated_revenues[department_id]
            doctors = number_of_doctors[department_id]
            generated_revenues_per_number_of_doctors[department_id] = revenue / doctors
        return generated_revenues_per_number_of_doctors

    def calculate_generated_revenues_per_number_of_doctors_per_hour(self):
        generated_revenues = self.calculate_generated_revenues()
        number_of_doctors = self.calculate_number_of_doctors()
        duration_of_examinations = self.calculate_duration_of_examinations()
        generated_revenues_per_number_of_doctors_per_hour = {}
        department_ids = generated_revenues.keys()
        for department_id in department_ids:
            revenue = generated_revenues[department_id]
            doctors = number_of_doctors[department_id]
            hours = duration_of_examinations[department_id]
            generated_revenues_per_number_of_doctors_per_hour[department_id] = revenue / doctors / hours
        return generated_revenues_per_number_of_doctors_per_hour
