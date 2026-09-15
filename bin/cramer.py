#! /usr/bin/env python

'''
@file cramer.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@brief POLI batch implementation to compare two SOMs using a modified Cramer-V similarity measure.
@LICENSE
# 
#  cramer.py Copyright (C) 2020-2026 Scott L. Williams.
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

# compare two SOMs using a modified Cramer-V similaririty measure

cramer_copyright = 'cramer.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import math
import itertools
import numpy as np
from npy_src import npy_src
from ezprint import eprint, eprints

# -------------------------------------------------------------
myname = os.path.basename(__file__) # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars

# read a som file for weights
def readsom( somfile ):

    wfile = open( somfile, 'r' ) 

    eprint( myname + ': reading ', somfile )
    
    # print header and look for flag
    found = False
    for line in wfile:
        if line.find( 'NEURONS' ) != -1:
            found = True
            break
        eprint( line.strip() )
                
    if not found:
        eprint( myname + ': cramer:could not find flag in:', somfile,
                '...exiting' )
        sys.exit( 1 )
                
    nneurons,ndim = wfile.readline().split()
    nneurons = int( nneurons )
    ndim = int( ndim )

    # get the neuron weights
    
    # allocate buffer
    neurons = np.empty( (nneurons,ndim), dtype=np.float32 )

    # retrieve neurons from file
    for i in range( nneurons):            
        line = wfile.readline().split()    # get line components:
        
        for j in range( 1, ndim+1 ):       # skip grey level label
            neurons[i,j-1] = float( line[j] )
            
    wfile.close()

    return neurons

def find_BMU( num, neurons, sample ):

    # just find the closest vector

    # initialize
    diff = sample - neurons[0]
    diff = np.abs( diff )
    min_dist = np.sum( diff, axis=0 )
    label = 0
    
    for i in range(1,num):
        diff = sample - neurons[i]
        diff = np.abs( diff )
        tmp = np.sum( diff, axis=0 )
        if tmp < min_dist:
            min_dist = tmp
            label = i

    return label

def cramer( datafile, som1file, som2file, lutfile, mmap ):
    
    # get the soms
    som1 = readsom( som1file )
    som2 = readsom( som2file )

    # check dimensions
    if som1.shape != som2.shape:
        eprint( myname + ': som maps do not have same shape...exiting' )
        sys.exit( 1 )
    
    # get the training data
    src = npy_src.npy_src()
    src.p.mmap = mmap
    src.p.filepath = datafile

    eprints( myname + ': reading datafile: ' + src.p.filepath + '...' )
    src.run()
    eprint( 'done' )

    data = src.sink
    ny,nx,ndim = data.shape

    # check if vector dimensions match
    nlabels, ndim_som = som1.shape
    ny, nx, ndim_data = data.shape
    if ndim_som != ndim_data:
        eprint( 'cramer: vector dimensions are mismatched...exiting' )
        sys.exit( 2 )

    # allocate observable matrix and set to zero
    obs = [[0 for i in range(nlabels)] for j in range(nlabels)]

    # construct observable matrix
    eprints( myname + ': constructing observable matrix...' )

    # assign first SOM to be columns (x), second SOM to be rows (y)
    for j in range( ny ):
        for i in range( nx ):
            label1 = find_BMU( nlabels, som1, data[j,i,:] )
            label2 = find_BMU( nlabels, som2, data[j,i,:] )
            obs[label2][label1] += 1
            
            eprints( next(spinner) )
            eprints('\b')

    eprint( 'done' )

    '''
    for j in range( nlabels ):
        eprint( obs[j] )
    '''

    # create a class to class mapping (LUT) SOM1 labels to SOM2 labels
    # for later application in similarity measures
    if lutfile != None:
        eprints( myname + ': creating lut...' )

        lut = [0 for i in range( nlabels ) ]
        
        # brute force
        for i in range( nlabels ):
            
            # find maximum for this column
            maxc = -math.inf
            for j in range( nlabels ):
                if obs[j][i] > maxc:
                    maxc = obs[j][i]
                    ij = j
            lut[i] = ij

        lfile = open( lutfile, 'w' )
        for i in range( nlabels-1 ):
            lfile.write( str(lut[i]) + ',' )
        lfile.write( str(lut[i+1]) + '\n' )
        lfile.close()

        eprint('done')
            
    # construct vectors/matrices
    Ni = [0 for i in range(nlabels)]
    for i in range(nlabels):
        Ni[i] = 0
        for j in range(nlabels):
            Ni[i] += obs[j][i]
        
        if Ni[i] == 0:
            eprint( myname + ': error...Ni element at', i, ' is zero' )
            eprint( '   an unused label is indicated in file ' + som1file )
            eprint( '   try reducing number of classes in training...exiting.' )
            sys.exit(0)
        
    # get sum of vector
    sum_ni = 0
    for i in range(nlabels):
        sum_ni += Ni[i]

    Nj = [0 for i in range(nlabels)]
    for j in range(nlabels):
        Nj[j] = 0
        for i in range(nlabels):
            Nj[j] += obs[j][i]
        
        if Nj[j] == 0:
            eprint( myname + ': error...Nj element at', i, ' is zero' )
            eprint( '   an unused label is indicated in file ' + som2file )
            eprint( '   try reducing number of classes in training...exiting.' )
            sys.exit(0)

    # get sum of vector
    sum_nj = 0
    for j in range(nlabels):
        sum_nj += Nj[j]

    if sum_nj != sum_ni:
        eprint( myname + ': sums do not match...exiting' )
        sys.exit( 1 )

    ntotal = nx*ny    # total number of pixels

    if sum_nj != ntotal:
        eprint( myname + ': sample sums do not match...exiting' )
        sys.exit( 1 )

    # calculate expected values
    expected = [[0 for i in range(nlabels)] for j in range(nlabels)]
    for j in range( nlabels ):
        for i in range( nlabels ):
            expected[j][i] = (Nj[j] * Ni[i])/ntotal

    # calculate chi squared
    chisq = [[0 for i in range(nlabels)] for j in range(nlabels)]
    for j in range( nlabels ):
        for i in range( nlabels ):
            chisq[j][i] = ((obs[j][i]-expected[j][i])**2)/expected[j][i]

    # calculate cramer-v

    # numerator
    sum_chisq = 0.0
    for j in range( nlabels ):
        for i in range( nlabels ):
            sum_chisq += chisq[j][i]

    # denominator
    denominator = ntotal*(nlabels-1)

    Cv = math.sqrt( sum_chisq/denominator )
    eprint( myname + ': cramer-v done' )

    return Cv

#----------------------------------------------------------

def usage( self ):
        eprint( 'usage: cramer.py' )
        eprint( '       -h, --help' )
        eprint( '       -d datafile --data=datafile' )
        eprint( '       -f somfile, --first=somfile' )
        eprint( '       -s somfile, --second=somfile' )
        eprint( '       -l lutfile, --lut=lutfile' )
        eprint( '       -m , --mmap' )
        sys.exit(1)

def get_params( argv ):
    
    datafile = None
    som1file = None
    som2file = None
    lutfile = None
    mmap = False
        
    try:                                
        opts, args = getopt.getopt( argv, 'hd:f:s:l:m:',
                                    ['help','data=','first=',
                                     'second=','lut=', 'mmap'] )
            
    except getopt.GetoptError:           
        self.usage()                          
        sys.exit(2)  
                   
    for opt, arg in opts:                
        if opt in ( '-h', '--help' ):      
            self.usage()                     
            sys.exit(0)
        elif opt in ( '-d', '--data' ):
            datafile = arg
        elif opt in ( '-f', '--first' ):
            som1file = arg
        elif opt in ( '-s', '--second' ):
            som2file = arg
        elif opt in ( '-l', '--lut' ):
            lutfile = arg
        elif opt in ( '-m', '--mmap' ):
            mmap = True
        else:
            self.usage()                     
            sys.exit(1)

    if datafile == None:
        eprint( 'cramer: datafile is missing...exiting' )
        sys.exit(1)
        
    if som1file == None:
        eprint( 'cramer: first somfile is missing...exiting' )
        sys.exit(1)
        
    if som2file == None:
        eprint( 'cramer: second somfile is missing...exiting' )
        sys.exit(1)

    return datafile, som1file, som2file, lutfile, mmap

####################################################################
# command line user entry point 
####################################################################
if __name__ == '__main__':  

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ':  numpy version =', np.version.version )

    dataf,som1f,som2f,lutf,mmap = get_params( sys.argv[1:] )

    Cv = cramer( dataf, som1f, som2f, lutf, mmap )
    eprint( myname + ': cramer value =', Cv )
