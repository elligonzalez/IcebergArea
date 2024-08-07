import ice
from pixel_area import pixel_area
from download_data import tiffs
from download_data import downloadCSV
import os
import rasterio
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def download_and_areas(icebergname, output_location, coord1 = 'lat', coord2 = 'lon', timeRange=None):
    '''Function to download all NASA satelite images of an iceberg recorded from BYU and find it's daily area from the images
        Args:
           icebergname (string): iceberg name from BYU data
           output_location (string): output path
           coord1 (string): name of latitude column, optional if using BYU Stats Database
           coord2 (string): name of longitude column, optional if using BYU Stats Database
           timeRange (tuple): for select time ranges in csv file, optional
        Returns: Dictionary of daily areas from non-cloudy, non-cropped images of the iceberg from NASA. Basic scatter plot of data.'''
    downloadCSV('Stats Database/'+icebergname+'.csv', output_location, coord1, coord2,timeRange)
    directory = output_location
    areas_dict = {}
    for image in os.listdir(directory):
        name = image.rstrip('.tif')
        area = pixel_area(directory+image)
        areas_dict[str(name)] = area

    dates = []
    data = []
    for date in areas_dict:
        if type(areas_dict[date]) == float:
            dates.append(date)
            data.append(areas_dict[date])
        else:
            pass

    date = pd.to_datetime(dates)
    DF = pd.DataFrame()
    DF['value'] = data
    DF = DF.set_index(date)
    plt.scatter(DF.index, DF['value'], color='blue', s=16)
    plt.gcf().autofmt_xdate()
    
    
    plt.xlabel('Date')
    plt.ylabel('Area km2')
     
    plt.title(f'{icebergname} Area')
     
    plt.show()
    return areas_dict
