from backend.metrics.doctor_metrics import DoctorMetrics


class DoctorMetricsComposer:
    __doctor_metrics = None
    __NUMBER_OF_METRICS = 6

    def __init__(self, database_mock):
        self.__doctor_metrics = DoctorMetrics(database_mock)

    def __get_doctor_grades(self, number_of_examinations, number_of_patients, duration_of_examinations,
                            generated_revenues, generated_revenues_per_examination, generated_revenues_per_hour):
        number_of_examinations_values = number_of_examinations.values()
        number_of_patients_values = number_of_patients.values()
        duration_of_examinations_values = duration_of_examinations.values()
        generated_revenues_values = generated_revenues.values()
        generated_revenues_per_examination_values = generated_revenues_per_examination.values()
        generated_revenues_per_hour_values = generated_revenues_per_hour.values()

        number_of_examinations_average = sum(number_of_examinations_values) / len(number_of_examinations_values)
        number_of_patients_average = sum(number_of_patients_values) / len(number_of_patients_values)
        duration_of_examinations_average = sum(duration_of_examinations_values) / len(duration_of_examinations_values)
        generated_revenues_average = sum(generated_revenues_values) / len(generated_revenues_values)
        generated_revenues_per_examination_average\
            = sum(generated_revenues_per_examination_values) / len(generated_revenues_per_examination_values)
        generated_revenues_per_hour_average\
            = sum(generated_revenues_per_hour_values) / len(generated_revenues_per_hour_values)

        doctor_grades = {}
        doctor_ids = number_of_examinations.keys()
        for doctor_id in doctor_ids:
            points = 0
            if number_of_examinations[doctor_id] >= number_of_examinations_average:
                points += 1
            if number_of_patients[doctor_id] >= number_of_patients_average:
                points += 1
            if duration_of_examinations[doctor_id] >= duration_of_examinations_average:
                points += 1
            if generated_revenues[doctor_id] >= generated_revenues_average:
                points += 1
            if generated_revenues_per_examination[doctor_id] >= generated_revenues_per_examination_average:
                points += 1
            if generated_revenues_per_hour[doctor_id] >= generated_revenues_per_hour_average:
                points += 1
            grade = round(points / self.__NUMBER_OF_METRICS * 5, 2)
            doctor_grades[doctor_id] = grade
        return doctor_grades

    def get_composed_doctor_metrics(self):
        number_of_examinations = self.__doctor_metrics.calculate_number_of_examinations()
        number_of_patients = self.__doctor_metrics.calculate_number_of_patients()
        duration_of_examinations = self.__doctor_metrics.calculate_duration_of_examinations()
        generated_revenues = self.__doctor_metrics.calculate_generated_revenues()
        generated_revenues_per_examination = self.__doctor_metrics.calculate_generated_revenues_per_examination()
        generated_revenues_per_hour = self.__doctor_metrics.calculate_generated_revenues_per_hour()

        doctor_grades = self.__get_doctor_grades(number_of_examinations, number_of_patients, duration_of_examinations,
                                                 generated_revenues, generated_revenues_per_examination,
                                                 generated_revenues_per_hour)

        doctor_metrics = {}
        doctor_ids = number_of_examinations.keys()
        for doctor_id in doctor_ids:
            doctor_metrics[doctor_id] = {
                'grade': doctor_grades[doctor_id],
                'number_of_examinations': number_of_examinations[doctor_id],
                'number_of_patients': number_of_patients[doctor_id],
                'duration_of_examinations': duration_of_examinations[doctor_id],
                'generated_revenues': generated_revenues[doctor_id],
                'generated_revenues_per_examination': generated_revenues_per_examination[doctor_id],
                'generated_revenues_per_hour': generated_revenues_per_hour[doctor_id],
            }
        return doctor_metrics
