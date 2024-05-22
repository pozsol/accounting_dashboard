import panel as pn
import datetime


class UI:
    __endpoints = None

    def __init__(self, endpoints):
        self.__endpoints = endpoints

        selector_mode = pn.widgets.Select(name='Select mode', options=self.__endpoints.get_modes())

        entities = pn.bind(self.__endpoints.get_entity_list, selector_mode)
        selector_entity = pn.widgets.Select(name='Select entity', options=entities)

        entity = pn.bind(self.__endpoints.get_entity_details, selector_mode, selector_entity)
        entity_details = pn.pane.DataFrame(entity, sizing_mode='stretch_both', name='TestName')

        date_picker_from = pn.widgets.DatePicker(name='Pick starting date', value=datetime.date(2023, 1, 1))
        date_picker_to = pn.widgets.DatePicker(name='Pick end date', value=datetime.date(2023, 12, 31))
        date_picker_prediction = pn.widgets.DatePicker(name='Pick prediction date', value=datetime.date(2024, 12, 31))

        radio_prediction = pn.widgets.RadioButtonGroup(name='Prediction selector',
                                                       options=['None', 'Model 1', 'Model 2'], button_type='success')

        fig = pn.bind(self.__endpoints.get_fig, selector_mode, selector_entity, date_picker_from, date_picker_to,
                      radio_prediction, date_picker_prediction)
        plot_pane = pn.pane.Matplotlib(fig, tight=True, format='svg', sizing_mode='stretch_width', fixed_aspect=False)

        slider = pn.widgets.EditableIntSlider(name='Number of rows', value=20, fixed_start=1, fixed_end=100)
        metrics = pn.bind(self.__endpoints.get_metrics_table, selector_mode)
        tabulator = pn.widgets.Tabulator(metrics, disabled=True, page_size=slider, pagination='remote',
                                         frozen_columns=[0])

        button = pn.widgets.Button(name='Generate Report', button_type='success')
        button.on_click(self.__endpoints.generate_report)

        grid_spec = pn.GridSpec(width=1900, height=950)

        grid_spec[0:25, 0:25] = pn.Spacer()
        grid_spec[925:950, 1875:1900] = pn.Spacer()

        grid_spec[25:75, 25:625] = selector_mode
        grid_spec[100:150, 25:625] = selector_entity
        grid_spec[150:450, 25:625] = entity_details
        grid_spec[450:500, 25:125] = date_picker_from
        grid_spec[450:500, 150:250] = date_picker_to
        grid_spec[467:500, 300:500] = radio_prediction
        grid_spec[450:500, 525:625] = date_picker_prediction
        grid_spec[500:925, 25:625] = plot_pane

        grid_spec[25:850, 675:1875] = tabulator
        grid_spec[875:925, 1675:1875] = slider
        grid_spec[875:925, 675:875] = button

        dashboard = grid_spec

        dashboard.servable('Accounting Dashboard')
