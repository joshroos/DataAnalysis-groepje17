from bokeh.plotting import figure, show, output_file
#from bokeh.models import ColumnDataSource, LabelSet
import boxplot_rice

output_file('hbar.html', title="barchart.py Median Average of Rice Price West Africa and Middle East")

# value of median averages
median_i_range = boxplot_rice.calculate_median_i()
median_j_range = boxplot_rice.calculate_median_j()

# y axis
regions = ['Middle_East', 'West_Africa']

# plot figure
p = figure(tools=["save", "hover", "box_zoom"], y_range = regions, plot_width=800, background_fill_color = "#E8F8F5", plot_height=250, title = "Average Median of Rice Price from 1992-2016")

# design barchart
p.hbar(y = regions, height=0.5, left=0,
       right=[median_i_range, median_j_range],fill_color="#ff6699", line_color = "black")
p.xaxis.major_label_text_font_size="14pt"
p.xaxis.axis_label = "Dollars per KG"
p.yaxis.major_label_text_font_size= "14pt"
# for i,v in enumerate(regions):
#     p.text(v + 3, i + .25, str(i), color='blue')
show(p)

#data = {'Middle_East':median_i_range, 'West_Africa':median_j_range}
#source = ColumnDataSource(data=dict(Middle_East = [median_i_range], West_Africa = [median_j_range]))
#labels = LabelSet(text="symbol",text_font_size="8pt", text_color="#555555",source = source,
                  #text_align='center')
#hoi.add_layout(labels)
