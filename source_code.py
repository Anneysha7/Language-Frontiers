import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import geopandas as gpd
from shapely import wkt
from shapely.geometry import Polygon

import json

from bokeh.models import ColumnDataSource, HoverTool, GeoJSONDataSource
from bokeh.plotting import figure, save, curdoc
from bokeh.io import output_file, show, export_svg
from bokeh.layouts import column

world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

asia_df = world_df[world_df['continent'] == 'Asia']

asia_languages = pd.read_csv('data/asian_languages_profile.csv')

asia_languages = pd.merge(left=asia_languages, right=asia_df,
                          how='inner',
                          left_on='Country',
                          right_on='name',
                          suffixes=('', '_remove'))
asia_languages.drop([i for i in asia_languages.columns if 'remove' in i],
                    axis=1,
                    inplace=True)
asia_languages.drop([i for i in asia_languages if '_y' in i],
                    axis=1,
                    inplace=True)

asia_languages_gpd = gpd.GeoDataFrame(asia_languages, geometry='geometry')

asia_lang_geosource = GeoJSONDataSource(geojson = asia_languages_gpd.to_json())

TOOLTIPS = [('Country',"@Country"),
            ('Language', '@Language'),
            ('Search', '@Keyword')]

p = figure(title='Google Search: Asian Languages',
           tooltips=TOOLTIPS,
           x_range=(-180,180),
           y_range=(-90,90),
           x_axis_location=None,
           y_axis_location=None)

p.patches('xs', 'ys',
          fill_alpha=1,
          fill_color='yellow',
          line_color='black',
          line_width=0.5,
          source=asia_lang_geosource)

p.background_fill_color = "aqua"

curdoc().add_root(column(p))