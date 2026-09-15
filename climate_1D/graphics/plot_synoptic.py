#! /usr/bin/env python

'''
@file plot_synoptic.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  plot_synoptic.py Copyright (C) 2020-2026 Scott L. Williams.
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

plot_synopitic_copyright = 'plot_synoptic.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

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
    eprint( '       -c cramer_value, --cramer=cramer_value' )
    eprint( '       -p percent, --percent=Percent_value ' )
    eprint( '       -f first_in_filepath, --fpath=first_in_filepath' )
    eprint( '       -s second_in_filepath, --spath=second_in_filepath' )
    eprint( '       -t transcribed_file_path, --tpath=transcribed_file_path' )
    eprint( '       -d diff_in_filepath, --dpath=diff_in_filepath' )
    eprint( '       -o out_file_path, --out=out_file_path' )
    eprint( '       -k comment, --komment=comment' )
    eprint( '       -i srcfile, --insrc=srcfile' )

    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):

    cramer = None
    percent = None    
    lpath = None
    fpath = None
    spath = None
    dpath = None
    tpath = None
    opath = None
    komment = ''
    srcfile = ''

    try:                                
        opts, args = getopt.getopt( argv, 'hp:l:f:s:d:o:c:t:k:i:',
                                    ['help','percent=','lpath=',
                                     'cramer=','fpath=','spath=',
                                     'dpath=','opath=','tpath=',
                                     'komment=', 'insrc='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()

        if opt in ('-c', '--cramer'):
            cramer = float(arg)
            if cramer < 0:
                eprint( myname + ': cramer cannot be < 0 ... exiting' )
                usage()

            if cramer > 1:
                eprint( myname + ': cramer cannot be > 1 ... exiting' )
                usage()

            cramer = arg # back to string
            
        if opt in ('-p', '--percent'):
            percent = float(arg)
            if percent < 0:
                eprint( myname + ': percent cannot be < 0 ... exiting' )
                usage()

            if percent > 100:
                eprint( myname + ': percent cannot be > 100 ... exiting' )
                usage()
                
            percent = arg # keep it as string
            
        if opt in ('-l', '--lpath'):
            lpath = arg
            if not os.path.isfile( lpath ):
                eprint( myname + ': lut input file: ' + lpath + ' does not exist ... exiting' )
                usage()
    
        if opt in ('-f', '--fpath'):

            fpath = arg
            if not os.path.isfile( fpath ):
                eprint( myname + ': first input file: ' + fpath + ' does not exist ... exiting' )
                usage()
                
        if opt in ('-s', '--spath'):

            spath = arg
            if not os.path.isfile( spath ):
                eprint( myname + ': second input file: ' + spath + ' does not exist ... exiting' )
                usage()
                
        if opt in ('-t', '--tpath'):

            tpath = arg
            if not os.path.isfile( tpath ):
                eprint( myname + ': transcribed input file: ' + tpath + ' does not exist ... exiting' )
                usage()
                
        if opt in ('-d', '--dpath'):

            dpath = arg
            if not os.path.isfile( spath ):
                eprint( myname + ':differnce input file: ' + dpath + ' does not exist ... exiting' )
                usage()
                 
        if opt in ('-o', '--opath'):
            opath = arg

        if opt in ('-k', '--komment'):
            komment = arg                     

        if opt in ('-i', '--insrc'):
            srcfile = arg                     

    if percent == None:
        eprint( myname + ': percent difference must be given .. exiting' )
        usage()
        
    if cramer == None:
        eprint( myname + ': cramer similarity  must be given .. exiting' )
        usage()

    if fpath == None:
        eprint( myname + ': must have an first input filepath ... exiting' )
        usage()

    if spath == None:
        eprint( myname + ': must have an second input filepath ... exiting' )
        usage()
        
    if tpath == None:
        eprint( myname + ': must have an transcribed input filepath ... exiting' )
        usage()

    if dpath == None:
        eprint( myname + ': must have an difference filepath ... exiting' )
        usage()

    if lpath == None:
        eprint( myname + ': must have a color lut input filepath ... exiting' )
        usage()
        
    if opath == None:
        eprint( myname + ': must have an output file path ... exiting' )
        usage()

    eprint( myname + ': using parameters:' )
    eprint( '                  fpath =', fpath )
    eprint( '                  spath =', spath )
    eprint( '                  tpath =', tpath )
    eprint( '                  dpath =', dpath )
    eprint( '                  opath =', opath )
    eprint( '                  lpath =', lpath )
    eprint( '                 cramer =', cramer )
    eprint( '                percent =', percent )
    eprint( '                komment =', komment )
    eprint( '                  insrc =', srcfile )

    # get directory path
    outdir = os.path.dirname( opath )
    
    if not os.path.isdir( outdir ):
        eprint( myname + ': making directory: ' + outdir )
        os.makedirs( outdir )

    return cramer,percent,fpath,spath,tpath,dpath,opath,lpath,komment,srcfile

# -----------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
 
    cramer,percent,fpath,spath,tpath,dpath,opath,lpath,komment,srcfile = set_params( sys.argv[1:] )

    # read in images
    first = img.imread( fpath )
    second = img.imread( spath )
    transcribed = img.imread( tpath )
    diff = img.imread( dpath )

    title = 'Comparing 2 Classifications of ETo Climate (1-D Histogram)'

    fig,ax = plt.subplots(2,2)
    plt.subplots_adjust(wspace=0.15, hspace=-0.2)
    #ax[1,1].axis('off')
    
    ax[0,0].xaxis.set_label_position('top')
    ax[0,0].xaxis.set_ticks_position('top')
    ax[0,0].set_title( 'Run #: ' + os.path.basename( spath )[:-4] )
    ax[0,0].imshow( second, cmap=None,
                    interpolation='nearest', origin='upper',
                    extent = ( 0, 170, 170, 0 ) )
    
    ax[0,1].xaxis.set_label_position('top')
    ax[0,1].xaxis.set_ticks_position('top')
    ax[0,1].set_title( 'Run #: ' + os.path.basename( fpath )[:-4] )
    ax[0,1].imshow( first, cmap=None,
                    interpolation='nearest', origin='upper',
                    extent = ( 0, 170, 170, 0 ) )
    
    ax[1,1].xaxis.set_label_position('top')
    ax[1,1].xaxis.set_ticks_position('top')
    ax[1,1].set_title( 'Transcribed: ' + os.path.basename( tpath )[:-4] )
    ax[1,1].imshow( transcribed, cmap=None,
                    interpolation='nearest', origin='upper',
                    extent = ( 0, 170, 170, 0 ) )


    ax[1,0].xaxis.set_label_position('top')
    ax[1,0].xaxis.set_ticks_position('top')
    ax[1,0].set_title( 'Pixel Diff: %' + percent + ' Cramer: ' + cramer )
    ax[1,0].imshow( diff, cmap=None,
                    interpolation='nearest', origin='upper',
                    extent = ( 0, 170, 170, 0 ) )

    '''
    # read the look up table file
    lut = open( lpath, 'r' )
    
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
    '''
    #
    #plt.legend( handles=handles, bbox_to_anchor=(0.989, 0.875),  title='Clases\nClimáticas ETo' )

    #figure.text( 0.71, 0.380, 'Presented By: Cristina Yánez',
    #             rotation=90, fontsize=7 )
 
    plt.suptitle( title, size=12, fontweight ="bold", y=0.9 )
    figure = plt.gcf()                # get current figure
    figure.text( 0.91, 0.225, 'ETo Project, Yachay Tech University, July 2026',
                 rotation=90, fontsize=7 )
    
    figure.text( 0.91, 0.58, 'Source: '+ srcfile, rotation=90, fontsize=7 )

    figure.text( 0.20, 0.860, komment, fontsize=9 )

    figure.set_size_inches( 8.5, 11 ) # set figure's size manually

    plt.savefig( opath, bbox_inches='tight' ) # removes extra white spaces

    #plt.show() # showing on screen does not always match pdf version
