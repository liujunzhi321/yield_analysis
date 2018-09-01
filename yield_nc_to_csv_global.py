#coding=utf-8

import numpy as np
import pandas as pd
import pylab
import sys
import glob
from netCDF4 import Dataset

def get_first_value(grid_data):
    for year in range(1961,2009):
        if year in grid_data.keys():
            return grid_data[year]

if __name__ == '__main__':
    base_dir = r'D:\data\crop\global\Maize_yield\*.nc'
    base_dir = r'D:\data\crop\global\Wheat_yield\*.nc'
    output_dir = '.'
    filelist = glob.glob(base_dir)

    grid_dic = {}
    for filename in filelist:
        print filename
        year = int(filename[-7:-3])
        ds = Dataset(filename)
        #print dir(ds)
        #print ds.dimensions.keys()
        #print ds.variables.keys()

        t = ds.variables['time']
        data = ds.variables['Data'][0][0]
        nrow,ncol = data.shape
        for i in range(nrow):
            for j in range(ncol):
                if not np.isnan(data[i][j]):
                    k = '%03d%03d' % (i, j)
                    grid_dic.setdefault(k,{})
                    grid_dic[k][year] = data[i][j]

        ds.close()

    for grid_id in grid_dic:
        grid_data = grid_dic[grid_id]
        if len(grid_data) <= 45:
            #print grid_id, len(grid_data)
            continue

        outputfile = '%s/data/uniform_global_wheat/%s.csv' % (output_dir, grid_id,)
        f = open(outputfile, 'w')
        f.write('Year,Value\n')
        last_value = None
        for year in range(1961,2009):
            if year in grid_data.keys():
                s = '%d,%f\n' % (year,grid_data[year])
                f.write(s)
                last_value = grid_data[year]
            else:
                if last_value == None:
                    last_value = get_first_value(grid_data)
                    print 'get_first_value', grid_id
                s = '%d,%f\n' % (year, last_value)
                f.write(s)
                
        f.close()

    print 'done!'
