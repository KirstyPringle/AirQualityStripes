# AirQualityStripes
Code repo for the Air Quality Stripes project https://airqualitystripes.info/ 

Data is available here:  https://zenodo.org/records/13361899

The Air Quality Stripes project plots outdoor particulate matter (PM2.5) concentrations for cities around the world as a series of bar charts with distinctive "stripes" to show the concentration.

Any questions? Contact: airqualitystripes@gmail.com

The project is a collaboration between the University of Edinburgh (EPCC), the University of Leeds (School of Earth and Environment), the Software Sustainability Institute, the UK Met Office and North Carolina State University.

These images were produced by: Kirsty Pringle, Jim McQuaid, Richard Rigby, Steve Turnock, Carly Reddington, Meruyert Shayakhmetova, Malcolm Illingworth, Denis Barclay, Douglas Hamilton and Ethan Brain.

**Code Summary (10/12/2024)**

**List_of_Cities_Continent.txt**
- Contains the list of cities and lat / lon for the cities considered in V1.6
  

**plotting_routines_cities.py**  
- Python code that contains a number of plotting functions to produce the plots, all with a similar format.

  e.g. plot_absolute_bar_plot(data_combined, years, custom_cmap, plot_title, continent) 
  
    data_combined = data to plot (produced in Loop_Over_Cities.ipyn)
    years = years to plot (x axis)
    custom_cmap = colour scheme used (produced in Loop_Over_Cities.ipyn)
    plot_title = city and country name 
    continent = continent category



**Loop_Over_Cities.ipynb**

Input files
 - cmip_annual_mean_output.nc: Contains modeled PM2.5 concentrations (1850-2014).
 - vand_annual_mean_output.nc: Contains satellite-observed PM2.5 concentrations (1998-2022).
 - List_of_Cities_Continent.txt: A text file with metadata for each city, including: Latitude (lat), Longitude (lon), Continent (continent)

Workflow

1) Load Datasets:
   - Reads NetCDF files for model and satellite data.
   - Loads city metadata into a dictionary.

2) Process Each City in a Loop:

   - Interpolates model data (CMIP) to the city's latitude and longitude using linear interpolation.
   - Selects the nearest satellite data (VAND) for the city's location.
   - Averages model and satellite data over a specified time period (e.g., 2000–2002).

   Calculates the ratio of satellite to model data and classifies uncertainty as:
   - Low Uncertainty (ratio < 2)
   - Moderate Uncertainty (2 ≤ ratio < 4)
   - High Uncertainty (ratio ≥ 4)

   Combines model and satellite data into a single time series:
   - Uses weighted model data for years before 2000.
   - Uses satellite data for years from 2001 onward.
  
3) Visualization:

 - Generates time-series plots for each city in four different formats
 - Also generates plot comparing model and sattellite data (on Zenodo) for each city

4) Output Generation:

 - Saves individual city plots as PNG files in the output directory.
 - Data_Cities_F1_V1pt6.xlsx: A wide-format dataset with annual PM2.5 values for all cities.
 - Cities_Data_Ratios.xlsx: Ratio of the  3 year mean satellitte to 3 year mean model value for each city.

