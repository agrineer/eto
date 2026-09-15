#! /usr/bin/env python3

#  plot_pixels_hist.py Copyright (C) 2020-2026 Scott L. Williams.
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

plot_pixels_hist_copyright = 'plot_pixels_hist.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
from ezprint import eprint
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

outpath = '../../data/graphics/1D/2022/2022_0_hists_points.pdf'
csvfile = '../../data/graphics/1D/2022/2022_0_hists_points.csv'

# ------------------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
lut = [ 
    '#696969',  # dim gray         class 24
    '#8b0000',  # dark red         class 23
    '#808000',  # olive
    '#483d00',  # dark slate blue
    '#008000',  # green
    '#000080',  # navy
    '#9acd32',  # yellow green
    '#20b2aa',  # light sea green
    '#8b008b',  # dark magenta
    '#ff0000',  # red
    '#ffa500',  # orange
    '#ee82ee',  # violet
    '#7cfc00',  # lawn green
    '#8a2be2',  # blue violet
    '#deb887',  # burly wood
    '#00bfff',  # deep sky blue
    '#d8bfd8',  # thistle
    '#0000ff',  # blue
    '#ff7f50',  # coral
    '#ff00ff',  # fuchsia
    '#8a2be2',  # blue violet
    '#db7093',  # pale violet red
    '#f0e68c',  # khaki
    '#ff1493',  # deep pink
    '#ffff00' ] # yellow           class 0


def make_legend():
    
    # match jpg colors with a legend label
    handles = []
    count = 0
    rlut = reversed( lut )
    for c in rlut:

        c = c.strip()
        patch = mpatches.Patch( color=c, label=str( count ) )
        handles.append( patch )

        count = count + 1
       
    plt.legend( handles=handles,ncols=1,title='ETo\nWeather\nClasses',
                bbox_to_anchor=(-0.05,0.9),fontsize=7 )# bbox_to_anchor=(0.1,1.1), )

    
def read_data():

    infile = open( csvfile )                 # read the sample file
    srcfile = infile.readline()              # get source filename

    values = []                              # array of variable value arrays
    xpos = []                                # array of sampled pixel x positions
    for line in infile:
    
        items = line.split( ',' )            # parse out values from text line
        xpos.append( int( items[1] ) )       # grab pixel x position
    
        var_values = []                      # array of variable values 
        for i in range(2,len(items)):      
            var_values.append( int(items[i].strip()) )
        #var_values = reversed( var_values )
        #values.append( var_values )

        values.append( var_values[::-1] )     # reverse order of values to make
                                              # graph more intiutive when rotated
    return values, xpos, srcfile


def make_ticks( ax ):
    
    #ax.set_xlabel( '\nClases de Tiempo ETo', linespacing=1 )
    ax.set_xlabel( '\nETo Weather Classes', linespacing=1 )
    #xticks = [0,3,6,9,12,15,18,21,24]
    xticks = [0.14,3.14,6.14,9.14,12.14,15.14,18.14,21.14,24.14]
    xticks_labels = [24,21,18,15,12,9,6,3,0]

    ax.set_xticks( xticks )
    ax.set_xticklabels( xticks_labels )

    yticks = range(0,200,20)
    ax.set_yticks( yticks )
    ax.set_ylabel('\nPixel X Position\nY=0',linespacing=1)

    #ax.set_zlabel('\nNumero de Dias',linespacing=1)
    ax.set_zlabel('\nNumber of Days',linespacing=1)
    ax.set_box_aspect([1,1,0.35])

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])

    values, xpos, srcfile = read_data()
    
    npixels = len( xpos )
    nclasses = len( values[0] )
    
    # set up plot
    #fig = plt.figure()
    figure = plt.gcf()                # get current figure
    figure.set_size_inches( 8.5, 6.5 ) # set figure's size manually

    ax = figure.add_subplot(111, projection='3d')

    # populate the plot
    for i in range( npixels ):
        for j in range( nclasses ):
            v = values[i][j]
            ax.bar3d( j, xpos[i], 0, 0.75, 3.0, v,
                      shade=False, color=lut[j], alpha=0.5)
            '''
            if not v == 0:
                ax.bar3d( j, xpos[i], 0, 0.75, 3.0, v,
                          v, shade=False,color=lut[j], alpha=0.7)
            '''
                    
    ''' this uses 2d bar 
    # populate the plot
    for i in range( len(values) ):

        # plot the bar graph 
        xs = range( len(values[i]) )
        ax.bar( xs, values[i],  zs=xpos[i], zdir='y', color=lut, alpha=0.7, width=1.0)
    '''
    make_ticks( ax )
    make_legend()
    #plt.title( 'Histograma de Clases de Tiempo ETo\nComo Señal para Píxeles Seleccionados\nUbicación de Píxeles=(0,' + str(xpos[0]) + ') (0,' + str(xpos[1]) +') (0,' + str(xpos[2]) + ') (0,' + str(xpos[3]) + ')'+ '\nFuente: ' + srcfile, fontweight ="bold", y=1.0 )
    plt.title( 'ETo Weather Classes Histogram\nas Pixel Signal for SOM', fontweight ="bold", y=1.0 )
    #figure.text( 0.20, 0.775, 'Pre-processing:')
    #figure.text( 0.21, 0.750, thead, fontsize=9 )
    #figure.text( 0.69, 0.775, 'Pixel Location: (' + str(py) + ',' + str(px) +')',fontsize=9 )

    #figure.text( 0.69, 0.750, 'Coords:    (' + lat + ',' + lon + ')', fontsize=9 )
    figure.text( 0.20, 0.175, 'Source File: ' + os.path.basename( csvfile ), fontsize=7 )
    figure.text( 0.630, 0.175, 'ETo Project, Yachay Tech University, July 2026', fontsize=7 )
                 

    plt.savefig( outpath ) #, bbox_inches='tight' ) # removes extra white spaces

    #plt.show() # uncomment to show
