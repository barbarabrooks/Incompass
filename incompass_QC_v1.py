def QC_BB(data_raw, np):
    data_raw.BB_flag = np.ones(data_raw.BB.shape)
   
    ii_min = np.where(data_raw.BB <= 1e-7)
    data_raw.BB_flag[ii_min] = 2
    ii_max = np.where(data_raw.BB > 0.06)
    data_raw.BB_flag[ii_max] = 2
   
    return data_raw
   
def QC_BB_noise(data_raw):
    dur, gates = data_raw.BB_flag.shape
    #for each gate
    for i in range(gates-1):
        for ii in range(2,dur-3):
            if ((data_raw.BB_flag[ii-2,i]) and (data_raw.BB_flag[ii,i] == 1) and (data_raw.BB_flag[ii+2,i] != 1)):
                data_raw.BB_flag[ii,i] = 2
        for ii in range(2,dur-2):
            if ((data_raw.BB_flag[ii-1,i]) and (data_raw.BB_flag[ii,i] == 1) and (data_raw.BB_flag[ii+1,i] != 1)):
                data_raw.BB_flag[ii,i] = 2
   
    #for each time
    for i in range(dur-1):
        for ii in range(2,gates-3):
            if ((data_raw.BB_flag[i,ii-2]) and (data_raw.BB_flag[i,ii] == 1) and (data_raw.BB_flag[i,ii+2] != 1)):
                data_raw.BB_flag[i,ii] = 2
        for ii in range(2,gates-2):
            if ((data_raw.BB_flag[i,ii-1]) and (data_raw.BB_flag[i,ii] == 1) and (data_raw.BB_flag[i,ii+1] != 1)):
                data_raw.BB_flag[i,ii] = 2
                
    return data_raw
   
def QC_CBH(data_raw, np):
    # AMF flags: 
    #1 - good data, 2 - no sig backscatter, 3 - full obfurscation no cloud base
    #4 - some obfurscation - transparent, 5 - time stamp
   
    # vaisala flags:
    #0 - no sig backscatter, 1 - one cb, 2 - two cbs, 3 - 3 cbs, 4 - 4 cbs
    #5 - full obfurscation no cloud base, 6 - some obfurscation - transparent
    #/ - Raw data input to algorithm missing or suspect
    
    #get rid of '/////'
    for n in range(len(data_raw.ET)):
        if data_raw.cbh1[n].find('/') > -1:
            data_raw.cbh1[n] = -1.00e+20
        else:
            data_raw.cbh1[n] = float(data_raw.cbh1[n]) * 0.3048 #convert to meters      
    
    for n in range(len(data_raw.ET)):
        if data_raw.cbh2[n].find('/') > -1:
            data_raw.cbh2[n] = -1.00e+20
        else:
            data_raw.cbh2[n] = float(data_raw.cbh2[n]) * 0.3048 #convert to meters  
        
    for n in range(len(data_raw.ET)):
        if data_raw.cbh3[n].find('/') > -1:
            data_raw.cbh3[n] = -1.00e+20
        else:
            data_raw.cbh3[n] = float(data_raw.cbh3[n]) * 0.3048 #convert to meters    
            
    for n in range(len(data_raw.ET)):
        if data_raw.cbh4[n].find('/') > -1:
            data_raw.cbh4[n] = -1.00e+20
        else:
            data_raw.cbh4[n] = float(data_raw.cbh4[n]) * 0.3048 #convert to meters       
    
    data_raw.cbh_flag = np.ones(data_raw.cbh1.shape)
    
    ii_0 = np.where(data_raw.detection_status == 0)
    data_raw.cbh_flag[ii_0] = 2
    data_raw.cbh1[ii_0] = -1.00e+20
    data_raw.cbh2[ii_0] = -1.00e+20
    data_raw.cbh3[ii_0] = -1.00e+20
    data_raw.cbh4[ii_0] = -1.00e+20
    
    ii_0 = np.where(data_raw.detection_status == 1)
    data_raw.cbh2[ii_0] = -1.00e+20
    data_raw.cbh3[ii_0] = -1.00e+20
    data_raw.cbh4[ii_0] = -1.00e+20
    
    ii_0 = np.where(data_raw.detection_status == 2)
    data_raw.cbh3[ii_0] = -1.00e+20
    data_raw.cbh4[ii_0] = -1.00e+20
    
    ii_0 = np.where(data_raw.detection_status == 3)
    data_raw.cbh4[ii_0] = -1.00e+20

    ii_0 = np.where(data_raw.detection_status == 5)
    data_raw.cbh_flag[ii_0] = 3
    data_raw.cbh1[ii_0] = -1.00e+20
    data_raw.cbh2[ii_0] = -1.00e+20
    data_raw.cbh3[ii_0] = -1.00e+20
    data_raw.cbh4[ii_0] = -1.00e+20
    
    ii_0 = np.where(data_raw.detection_status == 6)
    data_raw.cbh_flag[ii_0] = 4
    data_raw.cbh1[ii_0] = -1.00e+20
    data_raw.cbh2[ii_0] = -1.00e+20
    data_raw.cbh3[ii_0] = -1.00e+20
    data_raw.cbh4[ii_0] = -1.00e+20
     
    return data_raw
   
def tidy_data(data_raw, data_QC, np):
    s = (len(data_raw.ET),4)
    data_QC.cbh = np.ones(s)
    
    data_QC.DT = data_raw.DT
    data_QC.ET = data_raw.ET
    data_QC.DoY = data_raw.DoY
    data_QC.laser_pulse_energy = data_raw.laser_pulse_energy
    data_QC.laser_temperature = data_raw.laser_temperature
    data_QC.tilt_angle = data_raw.tilt_angle
    data_QC.window_contamination = ((data_raw.window_transmission)/100)*2500 #mv eqivalent to vaisala window contamination
    data_QC.back_light = data_raw.back_light
    data_QC.BB = data_raw.BB
    data_QC.ZZ = data_raw.ZZ
    data_QC.BB_flag = data_raw.BB_flag
    for n in range(len(data_raw.ET)):
        data_QC.cbh[n,0] = data_raw.cbh1[n]
        data_QC.cbh[n,1] = data_raw.cbh2[n]
        data_QC.cbh[n,2] = data_raw.cbh3[n]
        data_QC.cbh[n,3] = data_raw.cbh4[n]
    
    data_QC.cbh_flag = data_raw.cbh_flag
    
    return data_QC
    
def QC_data(data_raw, np, data_QC):
    data_raw = QC_BB(data_raw, np)
    data_raw = QC_BB_noise(data_raw)
    data_raw = QC_CBH(data_raw, np)
    data_QC = tidy_data(data_raw, data_QC, np)
    
    return data_QC