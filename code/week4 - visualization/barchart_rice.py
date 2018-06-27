from bokeh.plotting import figure, show, output_file
#from bokeh.models import ColumnDataSource, LabelSet
import boxplot_rice

output_file('hbar.html', title="barchart.py Median Average of Rice Price Eastern Africa, West Africa and Middle East")

# value of median averages in Middle East, West Africa, East Africa, South Asia
median_ME_range = boxplot_rice.calculate_median_ME()
median_WA_range = boxplot_rice.calculate_median_WA()
median_EA_range = boxplot_rice.calculate_median_EA()
median_SA_range = boxplot_rice.calculate_median_SA()

# y axis
regions = ['Middle East', 'Eastern Africa', 'West Africa', 'South Asia']

# plot figure
e = figure(tools=["save", "hover", "box_zoom"], y_range = regions, plot_width=800, background_fill_color = "#E8F8F5", plot_height=250, title = "Average Median of Rice Price from 1992-2016")

# design barchart
e.hbar(y = regions, height=0.5, left=0,
       right=[median_ME_range, median_EA_range, median_WA_range, median_SA_range],fill_color="#ff6699", line_color = "black")
e.xaxis.major_label_text_font_size="14pt"
e.xaxis.axis_label = "Dollars per KG"
e.yaxis.major_label_text_font_size= "14pt"
# for i,v in enumerate(regions):
#     p.text(v + 3, i + .25, str(i), color='blue')
show(e)

#data = {'Middle_East':median_i_range, 'West_Africa':median_j_range}
#source = ColumnDataSource(data=dict(Middle_East = [median_i_range], West_Africa = [median_j_range]))
#labels = LabelSet(text="symbol",text_font_size="8pt", text_color="#555555",source = source,
                  #text_align='center')
#hoi.add_layout(labels)
