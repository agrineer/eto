#! /usr/bin/env python

'''
@file plot_pixel_image.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  plot_pixel_image.py Copyright (C) 2020-2026 Scott L. Williams.
#                       In collaboration with Cristina Yanez and Israel Pineda
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
plot__pixel_image_copyright = 'plot_pixel_image.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import matplotlib.image as img
import matplotlib.pyplot as plt
from ezprint import eprint, eprints

# ---------------------------------------------------------------------

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -s start_day, --sday=start_day # index value not a date' ) 
    eprint( '       -e end_day, --eday=end_day     # index value not a date' )
    eprint( '       -l y,x , --loc=y,x             # comma separated coordinates for pixels' )
    eprint( '       -c lat,lon --coord=lat,lon     # comma separated latitude, longitude' )
    eprint( '       -p file_prefix, --prefix=file_prefix # eg. binary_' )
    eprint( '       -t title_header, --thead=title_header ' )
    eprint( '       -i in_dir, -indir=indir' )
    eprint( '       -o out_dir, -outdir=outdir' )
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
                eprint( myname + \
                        ': start day index cannot be < zero ... exiting.' )
                usage()
                
            if sday > 364:
                eprint( myname + \
                        ': start day index cannot be > 364 ... exiting.' )
                usage()
                
        if opt in ( '-e', '--eday' ):
            eday = int(arg)
            if eday < 0:
                eprint( myname + \
                        ': end day index cannot be < 0 ... exiting.' )
                usage()
                
            if eday > 364:
                eprint( myname + \
                        ': end day index cannot be > 364 ... exiting.' )
                usage()

        if opt in ( '-l', '--loc' ):
            l = arg.split(',')
            
            py = int( l[0] )
            if py < 0:
                eprint( myname + \
                        ': pixel y index cannot be < zero ... exiting.' )
                usage()
                
            if py > 170:
                eprint( myname + \
                        ': pixel y index cannot be > 170 ... exiting.' )
                usage()
                
            px = int( l[1] )

            if px < 0:
                eprint( myname + \
                        ': pixel x index cannot be < zero ... exiting.' )
                usage()
                
            if px > 170:
                eprint( myname + \
                        ': pixel x index cannot be > 170 ... exiting.' )
                usage()

        if opt in ( '-c', '--coord' ):
            c = arg.split(',')
            lat = c[0]
            lon = c[1]

        if opt in ( '-p', '--prefix' ):
            prefix = arg
            if prefix not in ['binary_', 'col_hamming_9_', 'row_hamming_5_']:
                eprint( myname + \
                        ': unknown prefix: ' + prefix + ' ... exiting.' )
                usage()

        if opt in ('-t', '--thead'):
            thead = arg

        if opt in ('-i', '--indir'):

            indir = arg
            if not os.path.isdir( indir ):
                eprint( myname + \
                        'input directory: ' + indir + ' does not exists ... exiting' )
                usage()
                
        if opt in ('-o', '--outdir'):
            outdir = arg  # gets created later if needed
 
    if py == None:
        eprint( myname + \
                ': must have pixel y location: use -l option ... exiting' )
        usage()

    if px == None:
        eprint( myname + \
                ': must have pixel x location: use -l option ... exiting' )
        usage()

    if lat == None:
        eprint( myname + \
                ': must have pixel latitude: use -c option ... exiting' )
        usage()

    if lon == None:
        eprint( myname + \
                ': must have pixel longitude: use -c option ... exiting' )
        usage()
  
    if sday == None:
        eprint( myname + \
                ': must have start day index: use -s option ... exiting' )
        usage()
        
    if eday == None:
        eprint( myname + \
                ': must have end day index: use -e option ... exiting' )
        usage()

    if sday > eday:
        eprint( myname + \
                ': start day index must be < end day index .. exiting' )
        usage()

    if prefix == None:
        eprint( myname + \
                ': file prefix must be given .. exiting' )
        usage()
        
    if thead == None:
        eprint( myname + \
                ': title header must be given .. exiting' )
        usage()

    if indir == None:
        eprint( myname + \
                ': must have an input directory ... exiting' )
        usage()
        
    if outdir == None:
        eprint( myname + \
                ': must have an output directory ... exiting' )
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

# -----------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
 
    py,px,sday,eday,indir,outdir,thead,prefix,lat,lon = set_params( sys.argv[1:] )

    ndays = eday-sday + 1
    fname = prefix + str(py) + '_' + str(px) + '.png'
    fpath = indir + fname

    outpath = outdir + fname[:-4] + '_' + str(sday) + '_' + str(eday) + '.pdf'

    figure = plt.figure()
    ax = figure.add_subplot( 111 )

    # set axis labels and tick marks
    ax.set_xlabel('\n\n\nETo Weather Class',linespacing=1)
    ax.set_ylabel('\nDays',linespacing=1)

    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')
    xticks = [0.5, 3.5, 6.5, 9.5, 12.5, 15.5, 18.5, 21.5, 24.5]
    xticks_labels = [ '0', '3', '6', '9', '12', '15', '18', '21', '24' ]
    ax.set_xticks( xticks )

    # set tick marks
    # adjust tick marks if many days
    if ndays > 100:
        dely = 20
    else:
        dely = 10

    yticks = [] 
    yticks_labels = []
    count = 0
    for y in range(sday, sday+ndays, dely):
        yticks.append( count*dely + 0.5 )
        yticks_labels.append( y )
        count += 1
        
    ax.set_yticks( yticks )

    # set tick labels
    ax.set( xticklabels=xticks_labels,
            yticklabels=yticks_labels )

    image = img.imread( fpath )
    modimage = image[sday:eday+1, :, 1]

    ax.imshow( modimage, cmap='gray', aspect=25*3/ndays,
               interpolation='nearest', origin='upper',
               extent = ( 0, 25, ndays, 0 ) )

    path = os.path.basename( fpath )
    path = path.replace('.png','.npy', 1 )
    title = thead + \
        '\n\nNumber of days: ' + str( ndays ) + \
        '\nPixel location: (' + str(py) + ',' + str(px) +')' + \
        '\nCoord: (' + lat + ',' + lon + ')' 

    figure.text( 0.71, 0.175, 'Source File: ' + os.path.basename(path),
                 rotation=90, fontsize=7 )
    #figure.text( 0.71, 0.380, 'Presented By: Cristina Yánez',
    #             rotation=90, fontsize=7 )
    figure.text( 0.71, 0.575, 'ETo Project, Yachay Tech University, July 2026',
                  rotation=90, fontsize=7 )
    plt.title( title, fontweight ="bold" )

    figure = plt.gcf()                # get current figure
    figure.set_size_inches( 8.5, 11 ) # set figure's size manually

    plt.savefig( outpath, bbox_inches='tight' ) # removes extra white spaces

    #plt.show() # showing on screen does not match pdf version
