#!/usr/bin/env python2
###############################################################################
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################
 
__author__ = "Joel Boyd"
__copyright__ = "Copyright 2015"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"
 
###############################################################################

import logging
import os
import gzip

from genome import Genome

###############################################################################

class MatrixGenerator:
    
    COMPRESSED_SUFFIXES = set(['.gz', '.gzip'])
    REFERENCE_PATH = '/srv/db/uniprot/201607/KO.idmapping.dat.gz' ### ~ TODO: Wrap this up
    OLD_REFERENCE_PATH='/srv/db/uniprot/uniref_20151020/idmapping.KO.dat.gz'
    MATRIX_SUFFIX  = '_matrix.tsv'
    UR100 = 'UniRef100_'
    
    KO      = 'KO_IDS.txt'
    PFAM    = 'PFAM_IDS.txt'
    TIGRFAM = 'TIGRFAM_IDS.txt'

    def __init__(self, annotation_type):        
        data_directory = os.path.join(os.path.split(os.path.realpath(__file__))[0], '../data/ids/')
        if annotation_type == self.KO:
            self.annotation_list = [x.strip() for x in open(os.path.join(data_directory, self.KO))]
        elif annotation_type == self.PFAM:
            self.annotation_list = [x.strip() for x in open(os.path.join(data_directory, self.PFAM))]
        elif annotation_type == self.TIGRFAM:
            self.annotation_list = [x.strip() for x in open(os.path.join(data_directory, self.TIGRFAM))]

    def write_matrix(self, genomes_list, output_path):
        '''
        Writes a frequency matrix with of each annotation (rows) per sample (columns)

        Parameters
        ----------
        genomes_list        - list. List of Genome objects
        output_path         - string. Path to file to which the results are written.
        '''
        logging.info("    - Writing results to file: %s" % output_path)
        with open(output_path, 'w') as out_io:
            colnames = ['ID'] + [genome.name for genome in genomes_list]
            out_io.write('\t'.join(colnames) + '\n')
            for annotation in self.annotation_list:
                output_line = [annotation]
                for genome in genomes_list:
                    output_line.append( str(genome.count(annotation)) )
                out_io.write( '\t'.join(output_line) + '\n' )