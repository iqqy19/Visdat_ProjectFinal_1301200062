import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import column
from bokeh.models import Slider, Select

data = pd.read_csv('https://github.com/iqqy19/Visdat/blob/main/Data_Tanaman_Padi_Sumatera_version_1.csv?raw=true')
data.set_index('Tahun', inplace=True)

prov_list = data.Provinsi.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=prov_list, palette=Spectral6)

data.rename(columns={'Suhu rata-rata':'suhu_rata','Curah hujan':'curah_hujan','Luas Panen':'luas_panen'}, inplace=True)

# Create the figure: plot
plot = figure(title='1993', x_axis_label='Jumlah Produksi', y_axis_label='Luas Panen',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@provinsi')])

# Create the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.loc[1993].Produksi,
    'y'       : data.loc[1993].luas_panen,
    'provinsi'  : data.loc[1993].Provinsi,
})

# Create the scatter plot
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='provinsi', transform=color_mapper), legend='provinsi')

# Set the legend and axis attributes
plot.legend.location = 'top_right'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Update the data of the ColumnDataSource
    source.data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'provinsi': data.loc[yr].Provinsi,
    }
    # Update the plot title
    plot.title.text = str(yr)

# Create a slider object: slider
slider = Slider(start=1993, end=2020, step=1, value=1993, title='Year')
slider.on_change('value', update_plot)

# Create dropdown menus for x and y axis
x_select = Select(
    options=['Produksi', 'luas_panen', 'curah_hujan', 'Kelembapan', 'suhu_rata'],
    value='Produksi',
    title='x-axis data'
)
x_select.on_change('value', update_plot)

y_select = Select(
    options=['Produksi', 'luas_panen', 'curah_hujan', 'Kelembapan', 'suhu_rata'],
    value='luas_panen',
    title='y-axis data'
)
y_select.on_change('value', update_plot)

# Create the layout
layout = column(slider, x_select, y_select, plot)

# Display the layout using Streamlit
st.bokeh_chart(layout)
