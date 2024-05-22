import datetime


class DeviceMetrics:
    __database_mock = None

    def __init__(self, database_mock):
        self.__database_mock = database_mock

    def calculate_number_of_examinations(self):
        devices = self.__database_mock.get_all_devices()
        number_of_examinations = {}
        device_ids = devices.keys()
        for device_id in device_ids:
            device = devices[device_id]
            examination_ids = device['examination_ids']
            number_of_examinations[device_id] = len(examination_ids)
        return number_of_examinations

    def calculate_number_of_patients(self):
        devices = self.__database_mock.get_all_devices()
        patient_ids = {}
        device_ids = devices.keys()
        for device_id in device_ids:
            device = devices[device_id]
            examination_ids = device['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                patient_id = examination['patient_id']
                if device_id in patient_ids:
                    patient_ids[device_id].add(patient_id)
                else:
                    patient_ids[device_id] = {patient_id}
        number_of_patients = {}
        for device_id in patient_ids:
            number_of_patients[device_id] = len(patient_ids[device_id])
        return number_of_patients

    def calculate_number_of_doctors(self):
        devices = self.__database_mock.get_all_devices()
        doctor_ids = {}
        device_ids = devices.keys()
        for device_id in device_ids:
            device = devices[device_id]
            examination_ids = device['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                doctor_id = examination['doctor_id']
                if device_id in doctor_ids:
                    doctor_ids[device_id].add(doctor_id)
                else:
                    doctor_ids[device_id] = {doctor_id}
        number_of_doctors = {}
        for device_id in doctor_ids:
            number_of_doctors[device_id] = len(doctor_ids[device_id])
        return number_of_doctors

    def calculate_duration_of_examinations(self):
        devices = self.__database_mock.get_all_devices()
        duration_of_examinations = {}
        device_ids = devices.keys()
        for device_id in device_ids:
            device = devices[device_id]
            examination_ids = device['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                date_start = datetime.datetime.strptime(examination['date_start'], '%Y-%m-%d %H:%M:%S')
                date_end = datetime.datetime.strptime(examination['date_end'], '%Y-%m-%d %H:%M:%S')
                duration = date_end - date_start
                if device_id in duration_of_examinations:
                    duration_of_examinations[device_id] += duration
                else:
                    duration_of_examinations[device_id] = duration
        for device_id in duration_of_examinations:
            duration = duration_of_examinations[device_id].seconds / 3600
            duration_of_examinations[device_id] = duration
        return duration_of_examinations

    def calculate_generated_revenues(self):
        devices = self.__database_mock.get_all_devices()
        generated_revenues = {}
        device_ids = devices.keys()
        for device_id in device_ids:
            device = devices[device_id]
            examination_ids = device['examination_ids']
            for examination_id in examination_ids:
                examination = self.__database_mock.get_examination_by_id(str(examination_id))
                type_id = examination['type_id']
                type_ = self.__database_mock.get_type_by_id(str(type_id))
                price = type_['price']
                if device_id in generated_revenues:
                    generated_revenues[device_id] += price
                else:
                    generated_revenues[device_id] = price
        return generated_revenues

    def calculate_generated_revenues_per_examination(self):
        generated_revenues = self.calculate_generated_revenues()
        number_of_examinations = self.calculate_number_of_examinations()
        generated_revenues_per_examination = {}
        device_ids = generated_revenues.keys()
        for device_id in device_ids:
            revenue = generated_revenues[device_id]
            number = number_of_examinations[device_id]
            generated_revenues_per_examination[device_id] = revenue / number
        return generated_revenues_per_examination

    def calculate_generated_revenues_per_hour(self):
        generated_revenues = self.calculate_generated_revenues()
        duration_of_examinations = self.calculate_duration_of_examinations()
        generated_revenues_per_hour = {}
        device_ids = generated_revenues.keys()
        for device_id in device_ids:
            revenue = generated_revenues[device_id]
            hours = duration_of_examinations[device_id]
            generated_revenues_per_hour[device_id] = revenue / hours
        return generated_revenues_per_hour
