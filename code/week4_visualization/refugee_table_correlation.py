# datatable which shows correlation between incoming refugees and rice price
# for countries with highest refugee income
from datetime import date
from random import randint

from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show

output_file("data_table_refugees.html")

data = dict(
        countries=['Lebanon', 'Pakistan', 'Ethiopia', 'Chad', 'Jordan', 'Uganda', 'Burundi', 'Somalia', 'Iraq', 'Mali', 'Turkey', "Cote d'Ivoire"],
        correlation=[0.403,0.684,0.379,0.826,0.979,0.421,0.792,0.995,0.881,0.443,-0.603,-0.693],
    )
source = ColumnDataSource(data)

columns = [
        TableColumn(field="countries", title="Country Name"),
        TableColumn(field="correlation", title="Correlation Rice Price and Incoming Refugees"),
    ]
data_table = DataTable(source=source, columns=columns)

show(data_table)
