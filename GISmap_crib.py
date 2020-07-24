#!/usr/bin/env python
# coding: utf-8

# In[157]:


# packages
import folium
from folium import FeatureGroup
import json
import pandas as pd
import os
from folium.plugins import MarkerCluster

# create map object
m = folium.Map(location= [43.651070,-79.347015], zoom_start=10)


# In[58]:


# load geojson neighbourhood boundary data
with open(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Neighbourhoods.geojson') as json_file:
    nb = json.load(json_file)
# load ward boundary data
with open(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\City Wards Data.geojson') as json_file:
    wd = json.load(json_file)
    
# load covid-19 data by nb 
cv = pd.read_excel(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\CityofToronto_COVID-19_NeighbourhoodData.xlsx', sheet_name='All Cases and Rates by Neighbou')
# load 2011 nhs data by nb
nhs = pd.read_excel(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\demographics-nhs-indicators-2011.xlsx')

# homicide as markers
hmc = pd.read_csv(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Homicides_Open_Data.csv')
# with open(r'C:\Users\zhong\OneDrive\Documents\Research\CRIB\GIS\Homicide.geojson') as json_file:
    #hmc = json.load(json_file)


# In[20]:


nhs.head(5)


# In[32]:


# initiate colormap for folium.geojson
from branca.colormap import linear

colormap = linear.YlGn_09.scale(
    cv['Rate per 100,000 people'].min(),
    cv['Rate per 100,000 people'].max())

print(colormap(5.0))

colormap


# In[34]:


# dict for geojson
cv_dict = cv.set_index('Neighbourhood ID')['Rate per 100,000 people']
cv_dict[94]
nhs_dict = nhs.set_index('Hood#')['    Black'] #,'Chinese','Unemployed','No certificate, diploma or degree','Median after-tax household income $']
nhs_dict[94]


# In[158]:


# overlay choropleth
# covid cases
cvd=folium.Choropleth(
    geo_data=nb,
    data=cv,
    name='COVID19 cases per 100,000 people by Neighbourhood',
    columns=['Neighbourhood ID', 'Rate per 100,000 people'],
    key_on='feature.properties.AREA_SHORT_CODE',
    fill_color='Reds',
    fill_opacity=0.5,
    legend_name='COVID19 cases per 100,000 people',
    highlight=True
)

style_function = "font-size: 10px; font-weight: bold"
cvd.geojson.add_child(
    folium.features.GeoJsonTooltip(['AREA_NAME'], style=style_function, labels=False))

# black pop 2011
blk=folium.Choropleth(
    geo_data=nb,
    data=nhs,
    name='Black population by Neighbourhood 2011',
    columns=['Hood#', '    Black'],
    key_on='feature.properties.AREA_SHORT_CODE',
    fill_color='Blues',
    fill_opacity=0.5,
    legend_name='Black population',
    highlight=True
)

style_function = "font-size: 10px; font-weight: bold"
blk.geojson.add_child(
    folium.features.GeoJsonTooltip(['AREA_NAME'], style=style_function, labels=False))

# median income household 2011
mhi=folium.Choropleth(
    geo_data=nb,
    data=nhs,
    name='Median household income $ by Neighbourhood 2011',
    columns=['Hood#', '  Median after-tax household income $'],
    key_on='feature.properties.AREA_SHORT_CODE',
    fill_color='Greens',
    fill_opacity=0.5,
    legend_name='Median household income',
    highlight=True
)

style_function = "font-size: 10px; font-weight: bold"
mhi.geojson.add_child(
    folium.features.GeoJsonTooltip(['AREA_NAME'], style=style_function, labels=False))

# Unemployment 2011
unemp=folium.Choropleth(
    geo_data=nb,
    data=nhs,
    name='Unemployed population by Neighbourhood 2011',
    columns=['Hood#', '    Unemployed'],
    key_on='feature.properties.AREA_SHORT_CODE',
    fill_color='YlOrBr',
    fill_opacity=0.5,
    legend_name='Unemployed population',
    highlight=True
)

style_function = "font-size: 10px; font-weight: bold"
unemp.geojson.add_child(
    folium.features.GeoJsonTooltip(['AREA_NAME'], style=style_function, labels=False))

# Uneducated 2011
unedu=folium.Choropleth(
    geo_data=nb,
    data=nhs,
    name='Uneducated population by Neighbourhood 2011',
    columns=['Hood#', '  No certificate, diploma or degree'],
    key_on='feature.properties.AREA_SHORT_CODE',
    fill_color='Purples',
    fill_opacity=0.5,
    legend_name='Uneducated population',
    highlight=True
)

style_function = "font-size: 10px; font-weight: bold"
unedu.geojson.add_child(
    folium.features.GeoJsonTooltip(['AREA_NAME'], style=style_function, labels=False))

m.add_child(cvd).add_child(blk).add_child(mhi).add_child(unemp).add_child(unedu)
# m.add_child(folium.map.LayerControl())


# In[159]:


# plot homicides with popup, dot marker, put into a feature group
# marker_cluster = MarkerCluster(name='Homicide').add_to(m)
hmc_fg = FeatureGroup(name='Homicide',
                     overlay=True,
                     control=False)

for (index, row) in hmc.iterrows():
    folium.CircleMarker(location=[row.loc['Lat'], row.loc['Long']],
                        popup='Date: '+ str(row.loc['occurrence_date']) +' Type: '+ row.loc['homicide_type'] + ' Neighbourhood: '+ row.loc['Neighbourhood'],
                        radius=2,
                        color='black',
                        tooltip='click').add_to(hmc_fg)
    
# keep it always on top
m.keep_in_front(hmc_fg)
hmc_fg.add_to(m)
m.add_child(folium.map.LayerControl())

m


# In[160]:


m.save('TOneighbourhood.html')

