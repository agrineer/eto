#! /usr/bin/env python

'''
@file plot_class_image.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE
#  plot_class_image.py Copyright (C) 2020-2026 Scott L. Williams.
#                      In collaboration with Cristina Yanez and Israel Pineda
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
plot__class_image_copyright = 'plot_class_image.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import matplotlib.image as img
import matplotlib.pyplot as plt

from ezprint import eprint, eprints
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
# ---------------------------------------------------------------------

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -l color_lut_file_path, --lut=color_lut_file_path' )
    eprint( '       -t title_header, --thead=title_header ' )
    eprint( '       -i in_file_path, --inpath=in_file_path' )
    eprint( '       -o out_file_path, --outpath=out_file_path' )
    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):
    
    prefix = None
    thead = None
    lutpath = None
    inpath = None
    outpath = None

    try:                                
        opts, args = getopt.getopt( argv, 'hl:t:i:o:',
                                    ['help','lutpath=',
                                     'thead=','inpath=','outpath='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()
            
        if opt in ('-t', '--thead'):
            thead = arg

        if opt in ('-l', '--lutpath'):
            lutpath = arg
            if not os.path.isfile( lutpath ):
                eprint( myname + ': color lut input file: ' + lutpath + ' does not exist ... exiting' )
                usage()
    
        if opt in ('-i', '--inpath'):

            inpath = arg
            if not os.path.isfile( inpath ):
                eprint( myname + ': input file: ' + inpath + ' does not exist ... exiting' )
                usage()
                
        if opt in ('-o', '--outpath'):
            
            outpath = arg                     
            #if not outpath[-4] != '.pdf':
                #eprint( myname + ': Out filepath must be pdf type. Got: ' + outpath + ' ... exiting.' )
                
    if thead == None:
        eprint( myname + ': title header must be given .. exiting' )
        usage()

    if inpath == None:
        eprint( myname + ': must have an input file path ... exiting' )
        usage()
        
    if lutpath == None:
        eprint( myname + ': must have a color lut input file path ... exiting' )
        usage()
        
    if outpath == None:
        eprint( myname + ': must have an output file path ... exiting' )
        usage()

    eprint( myname + ': using parameters:' )
    eprint( '                  thead =', thead )
    eprint( '                 inpath =', inpath )
    eprint( '                outpath =', outpath )
    eprint( '                lutpath =', lutpath )

    # get directory path
    outdir = os.path.dirname( outpath )
    
    if not os.path.isdir( outdir ):
        eprint( myname + ': making directory: ' + outdir )
        os.makedirs( outdir )

    return inpath,outpath,thead,lutpath

# -----------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
 
    inpath,outpath,thead,lutpath = set_params( sys.argv[1:] )

    title = 'Imagen de las Clases Climáticas ETo en la Región de Investigación\nFuente: ' + inpath

    fig = plt.figure()
    ax = fig.add_subplot( 111 )
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')
 
    image = img.imread( inpath )
    ax.imshow( image, cmap=None,
               interpolation='nearest', origin='upper',
               extent = ( 0, 170, 170, 0 ) )

    # read the look up table file
    lut = open( lutpath, 'r' )
    
    # uncomment to define a cmap
    #clut = lut.read()
    #lut.seek( 0, 0 )

    #name = os.path.basename( lutpath )
    #name = name[:-4]
    #cmap = ListedColormap( name, clut, N=256 )

    # match jpg colors with a legend label
    handles = []
    count = 0
    for c in lut:

        c = c.strip()
        patch = mpatches.Patch( color=c, label=str( count ) )
        handles.append( patch )

        count = count + 1

        if count > 11:
            break
        
    plt.legend( handles=handles, bbox_to_anchor=(1.1925, 0.75),  title='Clases\nClimáticas ETo' )
    plt.title( title, fontweight ="bold" )

    figure = plt.gcf()                # get current figure
    figure.set_size_inches( 8.5, 11 ) # set figure's size manually

    plt.savefig( outpath, bbox_inches='tight' ) # removes extra white spaces

    #plt.show() # showing on screen does not always match pdf version
