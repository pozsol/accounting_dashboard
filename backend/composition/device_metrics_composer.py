from backend.metrics.device_metrics import DeviceMetrics


class DeviceMetricsComposer:
    __device_metrics = None
    __NUMBER_OF_METRICS = 7

    def __init__(self, database_mock):
        self.__device_metrics = DeviceMetrics(database_mock)

    def __get_device_grades(self, number_of_examinations, number_of_patients, number_of_doctors,
                            duration_of_examinations, generated_revenues, generated_revenues_per_examination,
                            generated_revenues_per_hour):
        number_of_examinations_values = number_of_examinations.values()
        number_of_patients_values = number_of_patients.values()
        number_of_doctors_values = number_of_doctors.values()
        duration_of_examinations_values = duration_of_examinations.values()
        generated_revenues_values = generated_revenues.values()
        generated_revenues_per_examination_values = generated_revenues_per_examination.values()
        generated_revenues_per_hour_values = generated_revenues_per_hour.values()

        number_of_examinations_average = sum(number_of_examinations_values) / len(number_of_examinations_values)
        number_of_patients_average = sum(number_of_patients_values) / len(number_of_patients_values)
        number_of_doctors_average = sum(number_of_doctors_values) / len(number_of_doctors_values)
        duration_of_examinations_average = sum(duration_of_examinations_values) / len(duration_of_examinations_values)
        generated_revenues_average = sum(generated_revenues_values) / len(generated_revenues_values)
        generated_revenues_per_examination_average \
            = sum(generated_revenues_per_examination_values) / len(generated_revenues_per_examination_values)
        generated_revenues_per_hour_average \
            = sum(generated_revenues_per_hour_values) / len(generated_revenues_per_hour_values)

        device_grades = {}
        device_ids = number_of_examinations.keys()
        for device_id in device_ids:
            points = 0
            if number_of_examinations[device_id] >= number_of_examinations_average:
                points += 1
            if number_of_patients[device_id] >= number_of_patients_average:
                points += 1
            if number_of_doctors[device_id] >= number_of_doctors_average:
                points += 1
            if duration_of_examinations[device_id] >= duration_of_examinations_average:
                points += 1
            if generated_revenues[device_id] >= generated_revenues_average:
                points += 1
            if generated_revenues_per_examination[device_id] >= generated_revenues_per_examination_average:
                points += 1
            if generated_revenues_per_hour[device_id] >= generated_revenues_per_hour_average:
                points += 1
            grade = round(points / self.__NUMBER_OF_METRICS * 5, 2)
            device_grades[device_id] = grade
        return device_grades

    def get_composed_device_metrics(self):
        number_of_examinations = self.__device_metrics.calculate_number_of_examinations()
        number_of_patients = self.__device_metrics.calculate_number_of_patients()
        number_of_doctors = self.__device_metrics.calculate_number_of_doctors()
        duration_of_examinations = self.__device_metrics.calculate_duration_of_examinations()
        generated_revenues = self.__device_metrics.calculate_generated_revenues()
        generated_revenues_per_examination = self.__device_metrics.calculate_generated_revenues_per_examination()
        generated_revenues_per_hour = self.__device_metrics.calculate_generated_revenues_per_hour()

        device_grades = self.__get_device_grades(number_of_examinations, number_of_patients, number_of_doctors,
                                                 duration_of_examinations, generated_revenues,
                                                 generated_revenues_per_examination, generated_revenues_per_hour)

        device_metrics = {}
        device_ids = number_of_examinations.keys()
        for device_id in device_ids:
            device_metrics[device_id] = {
                'grade': device_grades[device_id],
                'number_of_examinations': number_of_examinations[device_id],
                'number_of_patients': number_of_patients[device_id],
                'number_of_doctors': number_of_doctors[device_id],
                'duration_of_examinations': duration_of_examinations[device_id],
                'generated_revenues': generated_revenues[device_id],
                'generated_revenues_per_examination': generated_revenues_per_examination[device_id],
                'generated_revenues_per_hour': generated_revenues_per_hour[device_id],
            }
        return device_metrics
