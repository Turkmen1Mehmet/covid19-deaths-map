import pandas as pd
df_vaka = pd.read_csv("time_series_covid19_deaths_global.csv")

import pycountry
import pandas as pd

# Aggregate the dataset  
df_vaka = df_vaka.drop(columns=['Province/State','Lat', 'Long'])
df_vaka = df_vaka.groupby('Country/Region').agg('sum')
data_list = list(df_vaka.columns)

# Get the three-letter country codes for each country
def get_country_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None
df_vaka['country'] = df_vaka.index
df_vaka['iso_alpha_3'] = df_vaka['country'].apply(get_country_code)

# Transform the dataset in a long format
df_long = pd.melt(df_vaka, id_vars=['country','iso_alpha_3'], value_vars=data_list) 

import plotly.express as px

fig = px.choropleth(df_long,                            # Input Dataframe
                     locations="iso_alpha_3",           # identify country code column
                     color="value",                     # identify representing column
                     hover_name="country",              # identify hover name
                     animation_frame="variable",        # identify date column
                     projection="orthographic",         # select projection
                     color_continuous_scale = 'Peach',  # select prefer color scale
                     range_color=[0,50000]              # select range of dataset
                     )        
fig.show()          
fig.write_html("example_map.html")                      # write the result to HTML file 
