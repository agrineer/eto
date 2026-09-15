#! /usr/bin/env python

'''
@file show_diff.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE
#  show_diff.py Copyright (C) 2020-2026 Scott L. Williams
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

# show the pixel difference between two differently labeled images

show_diff_copyright = 'show_diff.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import math
import getopt
import pickle
import itertools
import numpy as np

from render import render
from npy_src import npy_src
from ezprint import eprint, eprints

from scipy.sparse import csr_matrix
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------------------------

# some globals
myname = os.path.basename(__file__)
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) 

def render_image( image, lut, fpath ):

    rndr.source = image
    rndr.readlut( lut )      #'../data/luts/cetin.lut' )
    rndr.p.filepath = fpath  #first + '.jpg'
    eprint( myname + ': writing image to:', fpath )
    rndr.run()

# use a metric to measure closeness
def distance( neurons1, neurons2 ):

    nlabels = len( neurons1 )
    if nlabels != len( neurons2 ):
        eprint( myname + ': number of labels do not match ... exiting.' )

    ndims = len( neurons1[0] )
    if ndims != len( neurons2[0] ):
        eprint( myname+ ': number of neuron dimensions do not match ... exiting.' )
 
    # allocate array of all distance
    arr = [ [0 for i in range( nlabels ) ] for j in range( nlabels ) ]

    # array of vector distances
    for j in range( nlabels ):
        for i in range( nlabels ):
            
            # euclidean
            arr[j][i] = math.sqrt(sum(pow(a-b,2) for a, b in zip(neurons1[j],neurons2[i]) ) )

            # manhattan
            #arr[j][i] = sum(abs(a-b) for a,b in zip(neurons1[j], neurons2[i]) )
                
    labelmap = []

    for l in range( nlabels ):
    
        # find next minimum and unique indices
        mindist = math.inf
        for j in range( nlabels ):
            for i in range( nlabels ):
                
                found = False
                for k in range( l ):
                    
                    if i == labelmap[k][0]:
                        found = True
                        
                    if j == labelmap[k][1]:
                        found = True
                        
                if not found and arr[j][i] < mindist:
                    mindist = arr[j][i]
                    ij = j
                    ii = i

        labelmap.append( [ ii, ij, mindist ] )

    labelmap = sorted( labelmap )
    
    lut = np.empty( (nlabels), dtype=np.int8 )
    for i  in range(nlabels ):
        lut[i] = labelmap[i][1]

    return lut
'''
def my_cosine_similarity(matrix1, matrix2):
    
    dot_product = np.dot(matrix1, matrix2.T)
    norm_matrix1 = np.linalg.norm(matrix1, axis=1)
    norm_matrix2 = np.linalg.norm(matrix2, axis=1)
    similarity = dot_product / (norm_matrix1[:, np.newaxis] * norm_matrix2)
    return similarity

# use a metric to measure closeness
def distance( neurons1, neurons2 ):

    if (neurons1.shape != neurons2.shape ):
        eprint( myname + ': label shapes do not match ... exiting.' )
        sys.exit( 1 )

    nlabels = neurons1.shape[0]
    
    csim = my_cosine_similarity( neurons1, neurons2 )
    cslut = np.empty( (nlabels), dtype=np.int8 )
    for i  in range( nlabels ):
        cslut[i] = np.argmax( csim[:,i] )
    print( cslut )
    
    edist = DistanceMetric.get_metric( 'chebyshev' )
    A = edist.pairwise( neurons1, neurons2 )
    print( A )
    for i  in range( nlabels ):
        cslut[i] = np.argmin( csim[:,i] )
    print( cslut )

    return cslut
'''

def get_label_header( labels ):

    # read header
    found = False
    for line in labels:
        if line.find( 'NEURONS' ) != -1:
            found = True
            break
        
    if not found:
        return None, None

    # read next line for number of labels (neurons) and dimensions
    nlabels,ndims = labels.readline().split()
    nlabels = int( nlabels )
    ndims = int( ndims )

    return nlabels, ndims

def compare_files( filepath1, filepath2 ):
    
    eprint( myname + ': comparing files: ', filepath1,
            'and', filepath2 )

    # first labels file
    labels1 = open( filepath1, 'r' )
    nlabels1, ndims1 = get_label_header( labels1 )
    if nlabels1 == None:
        eprint( myname + ': could not find "NEURONS" flag in ',
                filepath1, ' exiting.')
        sys.exit( 2 )

    # second labels file
    labels2 = open( filepath2, 'r' )
    nlabels2, ndims2 = get_label_header( labels2 )
    if nlabels2 == None:
        eprint( myname + ': could not find "NEURONS" flag in ',
                filepath2, ' exiting.' )
        sys.exit( 2 )
    
    if nlabels1 != nlabels2:
        eprint( myname + ': number of labels do not match...exiting' )
        sys.exit( 2 )
     
    eprint( myname + ': reading label vectors... ' )

    # if vectors are different dimension size then extend the short one with zeros
    if ndims1 == ndims2:
        ndims = ndims1
        
    elif ndims1 > ndims2:
        ndims = ndims1
        eprint( myname + ': weight dimensions from: ' + filepath2 + ' will be extended with zeros' )

    else:
        ndims = ndims2
        eprint( myname + ': weight dimensions from: ' + filepath1 + ' will be extended with zeros' )

    #
    neurons1 = np.zeros( (nlabels1, ndims), dtype=np.float32 )
    neurons2 = np.zeros( (nlabels2, ndims), dtype=np.float32 )

    # populate arrays
    for i in range( nlabels1 ):

        # read and load the weights of first file
        line1 = labels1.readline().split()
 
        # get the neuron weights (vector feature space)
        for j in range( 1, ndims1+1 ):       # skip grey level label
            neurons1[i,j-1] = float( line1[j] )
     
        # second file
        line2 = labels2.readline().split()
        for j in range( 1, ndims2+1 ):       # skip grey level label
            neurons2[i,j-1] = float( line2[j] ) 
   
    # compare arrays

    # get vector similarities
    return distance( neurons1, neurons2 )

# ---------------------------------------------------------------------------

def usage():
        
    eprint( '\nusage: show_diff.py' )
    eprint( '       -h, --help' )
    eprint( '       -f prefix, --first=prefix  # file prefix for label and npy count' )
    eprint( '       -s prefix, --second=prefix' )
    eprint( '       -l lutpath, --lut=lutpath' )
    eprint( '' )
    sys.exit(0)
    
def set_params( argv ):
    first = None
    second = None
    lutpath = None
    
    try:                                
        opts, args = getopt.getopt( argv, 'hf:s:l:', ['help','first=','second=','lut='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            self.usage()                     
            sys.exit( 0 )

        if opt in ('-f', '--first'):
            if not os.path.isfile( arg + '.labels' ):
                eprint( myname + ': file ' + arg + '.labels' + ' not found ... exiting' )
                usage()
                
            if not os.path.isfile( arg + '.npy' ):
                eprint( myname + ': file ' + arg + '.npy' + ' not found ... exiting' )
                usage()

            first = arg

        if opt in ('-s', '--second'):
            if not os.path.isfile( arg + '.labels' ):
                eprint( myname + ': file ' + arg + '.labels' + ' not found ... exiting' )
                usage()
                
            if not os.path.isfile( arg + '.npy' ):
                eprint( myname + ': file ' + arg + '.npy' + ' not found ... exiting' )
                usage()

            second = arg
            
        if opt in ('-l', '--lut'):
            if not os.path.isfile( arg ):
                eprint( myname + ': lutfile: ' + arg + ' not found ... exiting' )
                usage()
            lutpath = arg
 
    if first == None:
        eprint( myname + ': first prefix not given ... exiting' )
        usage()
        
    if second == None:
        eprint( myname + ': second prefix not given ... exiting' )
        usage()

    if lutpath == None:
        eprint( myname + ': color lut path not given ... exiting' )
        usage()

    return first, second, lutpath

#------------------------------------------------

# some globals
myname = os.path.basename(__file__)
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

# instantiate source and render POLI classes
src = npy_src.npy_src()
src.p.verbose = False

rndr = render.render()
rndr.p.verbose = False
 
if __name__ == '__main__':

    first, second, lutpath = set_params( sys.argv[1:] )
    
    first_labels = first + '.labels'
    first_npy = first + '.npy'
    
    second_labels = second +'.labels' 
    second_npy = second + '.npy'
   
    # read cluster labels files and make similarity (lut) map
    lut = compare_files( first_labels, second_labels )
    eprint( myname + ': using lut: ' + str(lut) )

    # show the difference
    
    # first numpy source
    src.p.filepath = first_npy

    # read the first cluster image
    eprints( myname + ': reading first datafile:  '  + src.p.filepath + '...' )
    src.run()
    eprint( 'done' )
    first_buf = src.sink.astype( np.uint8 )

    # render the first image
    render_image( first_buf, lutpath,  first + '.jpg'  )
    
    # second numpy source
    src.p.filepath = second_npy

    # read the second cluster image
    eprints( myname + ': reading second datafile: ' + src.p.filepath + '...' )
    src.run()
    eprint( 'done' )
    second_buf = src.sink.astype( np.uint8 )
    
    # render the second image
    render_image( second_buf, lutpath,  second + '.jpg'  )
 
    # transcribe labels from first run for comparison
    trans_buf = lut[ src.sink ].astype( np.uint8 ) # transcribe classes

    render_image( trans_buf, '../data/luts/cetin.lut',
                  second + '_T.jpg' )

    # take the difference
    diff = trans_buf - first_buf  # wrap around ok
    mask = (diff != 0)            # mask is logical False, True

    # highlight pixels in white that are different
    out = np.zeros( src.sink.shape, dtype=np.uint8 )
    np.putmask( out, mask, 255 )

    count = np.count_nonzero( out )
        
    # number pixels =  ny*nx
    npix = src.sink.shape[0]*src.sink.shape[1]
    pcent = (count/float(npix))*100

    # put diff.jpg in first directory
    fdir = os.path.dirname( first )

    # find count number
    flist = first.split('_')
    size = len( flist )
    fcount = flist[size-1]

    slist = second.split('_')
    size = len( slist )
    scount = slist[size-1]

    fout = fdir + '/' + 'diff_' + scount + '-' + fcount + '.jpg'
    render_image( out, lutpath, fout  )
   
    # report to terminal
    ostr = myname + ': num of diff pixels=' + '%d,'%count + ' % diff=' + '%.2f'%pcent
    eprint( ostr + '\n' )
