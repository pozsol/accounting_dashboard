from backend.metrics.type_metrics import TypeMetrics


class TypeMetricsComposer:
    __type_metrics = None
    __NUMBER_OF_METRICS = 7

    def __init__(self, database_mock):
        self.__type_metrics = TypeMetrics(database_mock)

    def __get_type_grades(self, number_of_examinations, number_of_patients, number_of_doctors, duration_of_examinations,
                          generated_revenues, generated_revenues_per_examination, generated_revenues_per_hour):
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

        type_grades = {}
        type_ids = number_of_examinations.keys()
        for type_id in type_ids:
            points = 0
            if number_of_examinations[type_id] >= number_of_examinations_average:
                points += 1
            if number_of_patients[type_id] >= number_of_patients_average:
                points += 1
            if number_of_doctors[type_id] >= number_of_doctors_average:
                points += 1
            if duration_of_examinations[type_id] >= duration_of_examinations_average:
                points += 1
            if generated_revenues[type_id] >= generated_revenues_average:
                points += 1
            if generated_revenues_per_examination[type_id] >= generated_revenues_per_examination_average:
                points += 1
            if generated_revenues_per_hour[type_id] >= generated_revenues_per_hour_average:
                points += 1
            grade = round(points / self.__NUMBER_OF_METRICS * 5, 2)
            type_grades[type_id] = grade
        return type_grades

    def get_composed_type_metrics(self):
        number_of_examinations = self.__type_metrics.calculate_number_of_examinations()
        number_of_patients = self.__type_metrics.calculate_number_of_patients()
        number_of_doctors = self.__type_metrics.calculate_number_of_doctors()
        duration_of_examinations = self.__type_metrics.calculate_duration_of_examinations()
        generated_revenues = self.__type_metrics.calculate_generated_revenues()
        generated_revenues_per_examination = self.__type_metrics.calculate_generated_revenues_per_examination()
        generated_revenues_per_hour = self.__type_metrics.calculate_generated_revenues_per_hour()

        type_grades = self.__get_type_grades(number_of_examinations, number_of_patients, number_of_doctors,
                                             duration_of_examinations, generated_revenues,
                                             generated_revenues_per_examination, generated_revenues_per_hour)

        type_metrics = {}
        type_ids = number_of_examinations.keys()
        for type_id in type_ids:
            type_metrics[type_id] = {
                'grade': type_grades[type_id],
                'number_of_examinations': number_of_examinations[type_id],
                'number_of_patients': number_of_patients[type_id],
                'number_of_doctors': number_of_doctors[type_id],
                'duration_of_examinations': duration_of_examinations[type_id],
                'generated_revenues': generated_revenues[type_id],
                'generated_revenues_per_examination': generated_revenues_per_examination[type_id],
                'generated_revenues_per_hour': generated_revenues_per_hour[type_id],
            }
        return type_metrics
