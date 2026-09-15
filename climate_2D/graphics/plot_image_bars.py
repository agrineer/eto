#! /usr/bin/env python

'''
@file plot_image_bars.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  plot_image_bars.py Copyright (C) 2020-2026 Scott L. Williams
#                    In collaboration with Cristina Yanez and Israel Pineda
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
'''
plot_image_bars_copyright = 'plot_image_bars.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt

from npy_src import npy_src
import matplotlib.pyplot as plt
from ezprint import eprint, eprints
import matplotlib.patches as mpatches
from matplotlib.patches import Shadow
from mpl_toolkits.mplot3d import Axes3D

# TODO: find angles to display
# -------------------------------------------------------------------------

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -s start_day, --sday=start_day # index value not a date' ) 
    eprint( '       -e end_day, --eday=end_day     # index value not a date' )
    eprint( '       -l y,x , --loc=y,x             # comma separated cordinates for pixels' )
    eprint( '       -c lat,lon , --coord=lat,lon   # comma separated latitude, longitude' )
    eprint( '       -p file_prefix, --prefix=file_prefix # eg. binary_' )
    eprint( '       -t title_header, --thead=title_header ' )
    eprint( '       -i in_dir, --indir=indir' )
    eprint( '       -o out_dir, --outdir=outdir' )
    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):
    
    # pixel location NOTE: numpy order is Y,X
    py = None
    px = None

    lat = None
    lon = None
    
    # start and end days
    sday = None
    eday = None

    prefix = None
    thead = None
    indir = None
    outdir = None

    try:                                
        opts, args = getopt.getopt( argv, 'hs:e:l:p:t:i:o:c:',
                                    ['help','sday=','end=','loc=','prefix= ',
                                     'thead=','indir=','outdir=','coord='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()
            
        if opt in ( '-s', '--sday' ):
            sday = int(arg)
            if sday < 0:
                eprint( myname + ': start day index cannot be < zero ... exiting.' )
                usage()
                
            if sday > 364:
                eprint( myname + ': start day index cannot be > 364 ... exiting.' )
                usage()
                
        if opt in ( '-e', '--eday' ):
            eday = int(arg)
            if eday < 0:
                eprint( myname + ': end day index cannot be < zero ... exiting.' )
                usage()
                
            if eday > 364:
                eprint( myname + ': end day index cannot be > 364 ... exiting.' )
                usage()

        if opt in ( '-l', '--loc' ):
            l = arg.split(',')
            
            py = int( l[0] )
            if py < 0:
                eprint( myname + ': pixel y index cannot be < zero ... exiting.' )
                usage()
                
            if py > 170:
                eprint( myname + ': pixel y index cannot be > 170 ... exiting.' )
                usage()
                
            px = int( l[1] )

            if px < 0:
                eprint( myname + ': pixel x index cannot be < zero ... exiting.' )
                usage()
                
            if px > 170:
                eprint( myname + ': pixel x index cannot be > 170 ... exiting.' )
                usage()
                
        if opt in ( '-c', '--coord' ):
            c = arg.split(',')
            
            lat = float( c[0] ) # casting checks for real values
            lon = float( c[1] )

            lat = c[0]  # keep string versions
            lon = c[1]
     
        if opt in ( '-p', '--prefix' ):
            prefix = arg
            if prefix not in ['binary_', 'col_hamming_9_', 'row_hamming_5_']:
                eprint( myname + ': unknown prefix: ' + prefix + ' ... exiting.' )
                usage()

        if opt in ('-t', '--thead'):
            thead = arg

        if opt in ('-i', '--indir'):

            indir = arg
            if not os.path.isdir( indir ):
                eprint( myname + ': input directory: ' + indir + \
                        ' does not exists ... exiting' )
                usage()
                
            if not indir[-1] == '/':
                indir = indir + '/'
                               
        if opt in ('-o', '--outdir'):
            
            outdir = arg  # gets created later if needed
            if not outdir[-1] == '/':
                outdir = outdir + '/'
 
    if py == None:
        eprint( myname + ': must have pixel y location: use -l option ... exiting' )
        usage()

    if px == None:
        eprint( myname + ': must have pixel x location: use -l option ... exiting' )
        usage()
        
    if sday == None:
        eprint( myname + ': must have start day index: use -s option ... exiting' )
        usage()
        
    if eday == None:
        eprint( myname + ': must have end day index: use -e option ... exiting' )
        usage()

    if sday > eday:
        eprint( myname + ': start day index must be < end day index .. exiting' )
        usage()

    if prefix == None:
        eprint( myname + ': file prefix must be given .. exiting' )
        usage()
        
    if thead == None:
        eprint( myname + ': title header must be given .. exiting' )
        usage()

    if indir == None:
        eprint( myname + ': must have an input directory ... exiting' )
        usage()
        
    if outdir == None:
        eprint( myname + ': must have an output directory ... exiting' )
        usage()

    if lat == None:
        eprint( myname + ': must have a latitude ... exiting' )
        usage()

    if lat == None:
        eprint( myname + ': must have a longitude ... exiting' )
        usage()

    eprint( myname + ': using parameters:' )
    eprint( '                    py =', py )
    eprint( '                    px =', px )
    eprint( '                   lat =', lat )
    eprint( '                   lon =', lon )   
    eprint( '                  sday =', sday )
    eprint( '                  eday =', eday )
    eprint( '                 indir =', indir )
    eprint( '                 thead =', thead )
    eprint( '                outdir =', outdir )
    eprint( '                prefix =', prefix )

    if not os.path.isdir( outdir ):
        eprint( myname + ': making directory: ' + outdir )
        os.makedirs( outdir )

    return py,px,sday,eday,indir,outdir,thead,prefix,lat,lon

#----------------------------------------------------
# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
lut = [ 
    '#696969',  # dim gray
    '#8B0000',  # dark red
    '#808000',  # olive
    '#483D00',  # dark slate blue
    '#008000',  # green
    '#000080',  # navy
    '#9ACD32',  # yellow green
    '#20B2AA',  # light sea green
    '#8B008B',  # dark magenta
    '#FF0000',  # red
    '#FFA500',  # orange
    '#EE82EE',  # violet
    '#7CFC00',  # lawn green
    '#8A2BE2',  # blue violet
    '#DEB887',  # burly wood
    '#00BFFF',  # deep sky blue
    '#D8BFD8',  # thistle
    '#0000FF',  # blue
    '#FF7F50',  # coral
    '#FF00FF',  # fuchsia
    '#8A2BE2',  # blue violet
    '#DB7093',  # pale violet red
    '#F0E68C',  # khaki
    '#FF1493',  # deep pink
    '#FFFF00' ] # yellow


def make_ticks( ax ):
    
    # set axis labels
    ax.set_xlabel('\nETo Weather Classes',linespacing=1)
    #ax.set_ylabel('\nDías',linespacing=1)
    ax.set_ylabel('\nDays',linespacing=1)
    #ax.set_zlabel('\nValor',linespacing=1)
    ax.set_zlabel('\nData Value',linespacing=1)

    # adjust tick marks if many days
    if ndays > 100:
        dely = 30
    else:
        dely = 10

    # set tick marks
    yticks = range(sday, sday+ndays+dely, dely)
    ax.set_yticks( yticks )

    # work-around for class axis
    #xticks = [ 0,3,6,9,12,15,18,21,24]
    xticks = [0.14,3.14,6.14,9.14,12.14,15.14,18.14,21.14,24.14]
    xticks_labels = [24,21,18,15,12,9,6,3,0]
    ax.set_xticks( xticks )

    zticks = [0.0, 0.5, 1.0]
    ax.set_zticks( zticks )

    # set tick labels
    ax.set( xticklabels=xticks_labels,
            yticklabels=yticks,
            zticklabels=zticks )

    ax.set_box_aspect([1,1,0.25])

    
def read_data( fpath ):
    
    # read the numpy file
    src = npy_src.npy_src()
    src.p.filepath = fpath
    src.run()

    image = src.sink
    ny, nx, nbands = image.shape
    eprint( myname + ': source file: ' + fpath + ' shape:', image.shape )

    return image


def make_legend():
    
    # match jpg colors with a legend label
    handles = []
    count = 0
    rlut = reversed( lut )
    for c in rlut:

        c = c.strip()
        patch = mpatches.Patch( color=c, label=str( count ) )
        #patch = Shadow( patch, -0.01, -0.01, shade=0.4 )
        handles.append( patch )

        count = count+1
       
    plt.legend( handles=handles,ncols=1,title='ETo\nWeather\nClasses',
                bbox_to_anchor=(-0.05,0.9),fontsize=7 )# bbox_to_anchor=(0.1,1.1), )

    
if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
 
    py,px,sday,eday,indir,outdir,thead,prefix,lat,lon = set_params( sys.argv[1:] )
    
    ndays = eday-sday + 1
    fname = prefix + str(py) + '_' + str(px) + '.npy'
    fpath = indir + fname

    title = 'Pixel Image Showing 2-D Sample Data'
    '''
    title = # thead + \
        '\nNúmero de Días=' + str( ndays ) + \
        '\nUbicación de Píxel=(' + str(py) + ',' + str(px) +')' + \
        '\nLatitud = ' + lat + ' Longitud = ' + lon # + \
#        '\nFuente: ' + fpath
    '''
    outpath = outdir + fname[:-4] + '_' + str(sday) + '_' + str(eday) + '.pdf'

    image = read_data( fpath )
    
    # set up plot
    #figure = plt.gcf()  # get current figure
    figure = plt.figure()
    figure.set_size_inches( 8.5, 6.5 ) # set figure's size manually

    ax = figure.add_subplot(111, projection='3d')
    #ax = figure.gca(projection='3d')
    
    # shade the panes
    ax.xaxis.set_pane_color((0.8, 0.8, 0.8, 0.5))
    ax.yaxis.set_pane_color((0.8, 0.8, 0.8, 0.5))
    ax.zaxis.set_pane_color((0.8, 0.8, 0.8, 0.5))

    # populate the plot with image values
    for j in range( ndays ):
        for i in range( 25 ):

            v = image[sday+j,24-i,0] # subtraction addresses origin issue
                                     # and x,y are swapped !!
                                     # FIXME
            #'''
            ax.bar3d( i, j+sday, 0, 0.5, 0.5,
                      v, shade=False, color=lut[i], alpha=0.5)
 
            '''
            if not v == 0:
                ax.bar3d( i, sday+j, 0, 0.5, 0.5,
                          v, shade=False, color=lut[i], alpha=0.5)
            #'''
            
    make_legend()   
    make_ticks( ax )
    plt.title( title, y=1.0, fontweight ="bold" )

    figure.text( 0.20, 0.775, 'Pre-processing:')
    figure.text( 0.21, 0.750, thead, fontsize=9 )
    figure.text( 0.69, 0.775, 'Pixel Location: (' + str(py) + ',' + str(px) +')',
                 fontsize=9 )

    figure.text( 0.69, 0.750, 'Coords:    (' + lat + ',' + lon + ')', fontsize=9 )
    #figure.text( 0.69, 0.750, 'Latitude:  ' + lat, fontsize=9 ) 
    #figure.text( 0.69, 0.725, 'Longitude: ' + lon, fontsize=9 )
    figure.text( 0.69, 0.700, 'Number of Days: ' + str( ndays ), fontsize=9 )
    figure.text( 0.20, 0.175, 'Source File: ' + os.path.basename(fpath),
                 fontsize=7 )
    #figure.text( 0.675, 0.200, 'Presented By: Cristina Yánez', fontsize=7 )
    figure.text( 0.630, 0.175, 'ETo Project, Yachay Tech University, July 2026',
                 fontsize=7 )
 
    #plt.tight_layout()
    plt.savefig( outpath ) #, bbox_inches='tight' ) # bbox_inches removes extra white spaces
    #plt.show() # uncomment to see plot on screen

