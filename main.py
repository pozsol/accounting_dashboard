from data.sample_data_generation.sample_data_generator import SampleDataGenerator
from data.database_mock.database_mock import DatabaseMock
from backend.endpoints import Endpoints
from frontend.ui import UI


generate_sample_data = False
display_ui = True


if generate_sample_data:
    sample_data_generator = SampleDataGenerator()

    '''sample_data_generator.generate_sample_data(
        number_of_patients=25000,
        number_of_departments=10,
        number_of_doctors=50,
        number_of_types=100,
        number_of_devices=100,
        number_of_examinations=100000
    )'''
    sample_data_generator.generate_sample_data(
        number_of_patients=10,
        number_of_departments=3,
        number_of_doctors=25,
        number_of_types=3,
        number_of_devices=3,
        number_of_examinations=100
    )

database_mock = DatabaseMock()

endpoints = Endpoints(database_mock)

if display_ui:
    ui = UI(endpoints)
