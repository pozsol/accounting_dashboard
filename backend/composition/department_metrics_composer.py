from backend.metrics.department_metrics import DepartmentMetrics


class DepartmentMetricsComposer:
    __department_metrics = None
    __NUMBER_OF_METRICS = 9

    def __init__(self, database_mock):
        self.__department_metrics = DepartmentMetrics(database_mock)

    def __get_department_grades(self, number_of_examinations, number_of_patients, number_of_doctors,
                                duration_of_examinations, generated_revenues, generated_revenues_per_examination,
                                generated_revenues_per_hour, generated_revenues_per_number_of_doctors,
                                generated_revenues_per_number_of_doctors_per_hour):
        number_of_examinations_values = number_of_examinations.values()
        number_of_patients_values = number_of_patients.values()
        number_of_doctors_values = number_of_doctors.values()
        duration_of_examinations_values = duration_of_examinations.values()
        generated_revenues_values = generated_revenues.values()
        generated_revenues_per_examination_values = generated_revenues_per_examination.values()
        generated_revenues_per_hour_values = generated_revenues_per_hour.values()
        generated_revenues_per_number_of_doctors_values = generated_revenues_per_number_of_doctors.values()
        generated_revenues_per_number_of_doctors_per_hour_values\
            = generated_revenues_per_number_of_doctors_per_hour.values()

        number_of_examinations_average = sum(number_of_examinations_values) / len(number_of_examinations_values)
        number_of_patients_average = sum(number_of_patients_values) / len(number_of_patients_values)
        number_of_doctors_average = sum(number_of_doctors_values) / len(number_of_doctors_values)
        duration_of_examinations_average = sum(duration_of_examinations_values) / len(duration_of_examinations_values)
        generated_revenues_average = sum(generated_revenues_values) / len(generated_revenues_values)
        generated_revenues_per_examination_average\
            = sum(generated_revenues_per_examination_values) / len(generated_revenues_per_examination_values)
        generated_revenues_per_hour_average\
            = sum(generated_revenues_per_hour_values) / len(generated_revenues_per_hour_values)
        generated_revenues_per_number_of_doctors_average\
            = (sum(generated_revenues_per_number_of_doctors_values)
               / len(generated_revenues_per_number_of_doctors_values))
        generated_revenues_per_number_of_doctors_per_hour_average\
            = (sum(generated_revenues_per_number_of_doctors_per_hour_values)
               / len(generated_revenues_per_number_of_doctors_per_hour_values))

        department_grades = {}
        department_ids = number_of_examinations.keys()
        for department_id in department_ids:
            points = 0
            if number_of_examinations[department_id] >= number_of_examinations_average:
                points += 1
            if number_of_patients[department_id] >= number_of_patients_average:
                points += 1
            if number_of_doctors[department_id] >= number_of_doctors_average:
                points += 1
            if duration_of_examinations[department_id] >= duration_of_examinations_average:
                points += 1
            if generated_revenues[department_id] >= generated_revenues_average:
                points += 1
            if generated_revenues_per_examination[department_id] >= generated_revenues_per_examination_average:
                points += 1
            if generated_revenues_per_hour[department_id] >= generated_revenues_per_hour_average:
                points += 1
            if (generated_revenues_per_number_of_doctors[department_id]
                    >= generated_revenues_per_number_of_doctors_average):
                points += 1
            if (generated_revenues_per_number_of_doctors_per_hour[department_id]
                    >= generated_revenues_per_number_of_doctors_per_hour_average):
                points += 1
            grade = round(points / self.__NUMBER_OF_METRICS * 5, 2)
            department_grades[department_id] = grade
        return department_grades

    def get_composed_department_metrics(self):
        number_of_examinations = self.__department_metrics.calculate_number_of_examinations()
        number_of_patients = self.__department_metrics.calculate_number_of_patients()
        number_of_doctors = self.__department_metrics.calculate_number_of_doctors()
        duration_of_examinations = self.__department_metrics.calculate_duration_of_examinations()
        generated_revenues = self.__department_metrics.calculate_generated_revenues()
        generated_revenues_per_examination = self.__department_metrics.calculate_generated_revenues_per_examination()
        generated_revenues_per_hour = self.__department_metrics.calculate_generated_revenues_per_hour()
        generated_revenues_per_number_of_doctors\
            = self.__department_metrics.calculate_generated_revenues_per_number_of_doctors()
        generated_revenues_per_number_of_doctors_per_hour\
            = self.__department_metrics.calculate_generated_revenues_per_number_of_doctors_per_hour()

        department_grades = self.__get_department_grades(number_of_examinations, number_of_patients, number_of_doctors,
                                                         duration_of_examinations, generated_revenues,
                                                         generated_revenues_per_examination,
                                                         generated_revenues_per_hour,
                                                         generated_revenues_per_number_of_doctors,
                                                         generated_revenues_per_number_of_doctors_per_hour)

        department_metrics = {}
        department_ids = number_of_examinations.keys()
        for department_id in department_ids:
            department_metrics[department_id] = {
                'grade': department_grades[department_id],
                'number_of_examinations': number_of_examinations[department_id],
                'number_of_patients': number_of_patients[department_id],
                'number_of_doctors': number_of_doctors[department_id],
                'duration_of_examinations': duration_of_examinations[department_id],
                'generated_revenues': generated_revenues[department_id],
                'generated_revenues_per_examination': generated_revenues_per_examination[department_id],
                'generated_revenues_per_hour': generated_revenues_per_hour[department_id],
                'generated_revenues_per_number_of_doctors': generated_revenues_per_number_of_doctors[department_id],
                'generated_revenues_per_number_of_doctors_per_hour':
                    generated_revenues_per_number_of_doctors_per_hour[department_id]
            }
        return department_metrics
