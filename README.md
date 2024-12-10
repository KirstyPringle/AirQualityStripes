# AirQualityStripes
Code repo for the Air Quality Stripes project https://airqualitystripes.info/ 

Data is available here:  https://zenodo.org/records/13361899

The Air Quality Stripes project plots outdoor particulate matter (PM2.5) concentrations for cities around the world as a series of bar charts with distinctive "stripes" to show the concentration.

Any questions? Contact: airqualitystripes@gmail.com

The project is a collaboration between the University of Edinburgh (EPCC), the University of Leeds (School of Earth and Environment), the Software Sustainability Institute, the UK Met Office and North Carolina State University.

These images were produced by: Kirsty Pringle, Jim McQuaid, Richard Rigby, Steve Turnock, Carly Reddington, Meruyert Shayakhmetova, Malcolm Illingworth, Denis Barclay, Douglas Hamilton and Ethan Brain.

**Code Summary (10/12/2024)**

List_of_Cities_Continent.txt 
- Contains the list of cities and lat / lon for the cities considered in V1.6

plotting_routines_cities.py  
- Python code that contains a number of plotting functions to produce the plots, all with a similar format.

e.g. plot_absolute_bar_plot(data_combined, years, custom_cmap, plot_title, continent) 

data_combined = data to plot (produced in Loop_Over_Cities.ipyn)
years = years to plot (x axis)
custom_cmap = colour scheme used (produced in Loop_Over_Cities.ipyn)
plot_title = city and country name 
continent = continent category


Loop_Over_Cities.ipyn
