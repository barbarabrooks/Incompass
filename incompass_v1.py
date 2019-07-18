#Python 3 code to parse wao cceilometer data 
# args expected
#1. input directory 
#2. output diretory 
#3. path to meta file

import sys
import os
import numpy as np
import pandas as pd
np.warnings.simplefilter(action='ignore', category=FutureWarning)
from collections import namedtuple
import incompass_parser_v1 as onp
import incompass_QC_v1 as qc
#import incompass_plot_v1 as cplt
import incompass_NC_v1 as nc

data_raw = namedtuple("data_raw", "")
data_QC = namedtuple("data_QC", "")

din = str(sys.argv[1]) #input directory
dout = str(sys.argv[2]) #output directory
fn_meta_bck = str(sys.argv[3]) # backscatter meta file
fn_meta_cbh = str(sys.argv[4]) # cloud-base meta file

infiles = sorted(os.listdir(din)) #list of file in input directory
   
#parse the data  
data_raw = onp.ceil_parse(din, infiles, np, data_raw)  

#QC data
data_QC = qc.QC_data(data_raw, np, data_QC)

#plot and save image
#cplt.quick_look_plt_v2(data_QC, np, dout)

#Meta data
meta_bck = pd.read_excel(fn_meta_bck)
meta_cbh = pd.read_excel(fn_meta_cbh)

#save nc file
nc.NC_ceil(pd, np, dout, meta_bck, meta_cbh, data_QC) 