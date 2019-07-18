def get_file(fn, lines):
    ll=[]
    f = open(fn, 'r') 
    ll = f.readlines()
    f.close()
    for i in ll:
        lines.append(i)
    
    return lines
   
def parse_block(lines):
    start_of_block = []
    for i in range(len(lines)):
        a = lines[i]
        if a.count('CS') == 1:
            start_of_block.append(i)
    return start_of_block

def parse_time(lines, start_of_block, np, data):
    import time
    from datetime import datetime
    import calendar
    DT = []
    DoY = []
    ET = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]]
        b = a[0:a.index('C')-1]   
        t = []
        t.append(int(b[0:4]))
        t.append(int(b[5:7]))
        t.append(int(b[8:10]))
        t.append(int(b[11:13]))
        t.append(int(b[14:16]))
        t.append(float(b[17:len(b)]))
       
        c = time.strptime(b[0:len(b)],'%Y-%m-%dT%H:%M:%S.%f')
      
        DT.append(t)
        DoY.append(float(c.tm_yday)+(float(t[3])+float(t[4]/(60))+float(t[5]/(60*60)))/24)
        ET.append(calendar.timegm(c))
       
    data.DT = np.array(DT)
    data.DoY = np.array(DoY)
    data.ET = np.array(ET)
    
    return data
  
def parse_line1(lines, start_of_block, np, data):
    aa = []
    bb = []
    cc = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]]
        b = a[a.index('C'):len(a)-1] 
        aa.append(b[2:3])         #unit_id
        bb.append(b[3:6])       #OS system, 001 ... 999
        cc.append(b[6:len(b)])  #message number should be 2
        
    data.unit_id = np.array(aa)
    data.os = np.array(bb)
    data.message = np.array(cc)
    return data
   
def parse_line2(lines, start_of_block, np, data):
    aa = []
    bb = []
    cc = []
    dd = []
    ee = []
    ff = []
    gg = []
    hh = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]+1]
        b = a[a.index(' ')+1:len(a)-1]
        aa.append(b[0])          #detection status
        bb.append(b[1])          #warnings
        cc.append(b[3:6])        #window transmission (%)
        dd.append(b[7:12])       #cloudbase height 1
        ee.append(b[13:18])      #cloudbase height 2
        ff.append(b[19:24])      #cloudbase height 3
        gg.append(b[25:30])      #cloudbase height 4
        hh.append(b[31:len(b)])  #flag 
    
    data.detection_status = np.array(aa)
    data.warnings = np.array(bb)
    data.window_transmission = np.array(cc)
    data.window_transmission = data.window_transmission.astype(np.int)
    data.cbh1 = np.array(dd)
    data.cbh2 = np.array(ee)
    data.cbh3 = np.array(ff)
    data.cbh4 = np.array(gg)
    data.cflag = np.array(hh)
    
    return data 

def parse_line3(lines, start_of_block, np, data):
    aa = []
    bb = []
    cc = []
    dd = []
    ee = []
    ff = []
    gg = []
    hh = []
    ii = []
    jj = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]+2]
        b = a[a.index(' ')+1:len(a)-1]
        aa.append(b[0:5])       #scale
        bb.append(b[6:8])       #backscatter resolution (m)
        cc.append(b[9:13])      #Profile length
        dd.append(b[14:17])     #laser pulse energy (%)
        ee.append(b[18:21])     #laser temperature
        ff.append(b[22:24])     #tilt angle
        gg.append(b[25:29])     #background light
        hh.append(b[30:34])     #pulse quantity x 1000 (0000 - 9999)
        ii.append(b[35:37])     #sample rate MHz (00 - 99)
        jj.append(b[38:len(b)]) #sum 
        
    data.scale = np.array(aa)
    data.v_resolution = np.array(bb)
    data.v_resolution = data.v_resolution.astype(np.int)
    data.p_length = np.array(cc)
    data.p_length = data.p_length.astype(np.int)
    data.laser_pulse_energy = np.array(dd)
    data.laser_temperature = np.array(ee)
    data.tilt_angle = np.array(ff)
    data.back_light = np.array(gg)
    data.pulse_quality = np.array(hh)
    data.sample_rate = np.array(ii)
    data.sum = np.array(jj)
    
    return data 

def parse_line4(lines, start_of_block, np, data):
    alt = []
    line4 = []
    for i in range(len(start_of_block)-1):
        a = lines[start_of_block[i]+3]
        v_resolution = data.v_resolution[i]
        z = np.ones(2048)
        bb = np.ones(2048)
        for ii in range(2048):
            z[ii] = (ii * v_resolution) + (v_resolution/2)
            st = 27 + (ii * 5)
            ed = 27 + (ii * 5) + 5
            temp = int(a[st:ed],16)#(10 000.sr.km)-1
            bb[ii] = float(temp/1e8)#sr-1 m-1
                
        line4.append(bb)
        alt.append(z)
        
    data.ZZ = np.array(alt)
    data.BB = np.array(line4)    
    
    return data
    
def ceil_parse(din, infiles, np, data): 
    lines = []
    #read all file in directory
    for ii in range(0,len(infiles)):
        lines = get_file((din + infiles[ii]), lines)
        
    #parse out the data
    start_of_block = parse_block(lines)
    
    data = parse_time(lines, start_of_block, np, data)  # time
    data = parse_line1(lines, start_of_block, np, data) # housekeeping 1
    data = parse_line2(lines, start_of_block, np, data) # cloudbase height
    data = parse_line3(lines, start_of_block, np, data) # housekeeping 2
    data = parse_line4(lines, start_of_block, np, data) # backscatter profile
    
    return data