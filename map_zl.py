# packages
import folium
import json
import pandas as pd
import os
import numpy

# create map object
m = folium.Map(location=[43.651070, -79.347015], zoom_start=12)

# load json neighbourhood boundary data
with open(r"C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Neighbourhoods.geojson") as json_file:
    nb = json.load(json_file)

# load homicide data
hmc = pd.read_csv(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Homicides_Open_Data.csv')
# with open(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Homicide.geojson') as json_file:
# hmc = json.load(json_file)

# add to map
folium.GeoJson(nb).add_to(m)

# plot homicides with popup
for (index, row) in hmc.iterrows():
    folium.Marker(location=[row.loc['Lat'], row.loc['Long']],
                  popup="Date: " + str(row.loc['occurrence_date']) + ' Type: ' + row.loc[
                      'homicide_type'] + ' Neighbourhood: ' + row.loc['Neighbourhood'],
                  icon=folium.Icon(color='black', icon_shape_types='circle', prefix='fa'),
                  tooltip='click').add_to(m)

m.save('hmc_nb.html')
