def data_means(data_out, data_plt, np):
    from time import mktime, strptime
    
    DT = data_out.DT
    
    dur, gates = data_out.BB.shape
    s = ((24*12), gates)
    data_plt.ZZ = np.ones(s)*np.nan
    data_plt.BB = np.ones(s)*np.nan
    flagBB = np.ones(s)
    
    s1= ((24*12),6)
    data_plt.DT = np.ones(s1)*np.nan
    
    s2= (24*12)
    data_plt.DoY = np.ones(s2)*np.nan
    
    #s3= (24*12,3)
    #data_plt.cbh = np.ones(s3)*np.nan
    
    
    count = -1
    for hr in range(0, 24, 1):
        for mn in range(0, 60, 5):
            count = count + 1
            
            data_plt.DT[count,0] = int(DT[0,0])
            data_plt.DT[count,1] = int(DT[0,1])
            data_plt.DT[count,2] = int(DT[0,2])
            data_plt.DT[count,3] = int(hr)
            data_plt.DT[count,4] = int(mn)
            data_plt.DT[count,5] = 0
            
            msg = str(int(DT[0,2])) + '/' + str(int(DT[0,1])) + '/' + str(int(DT[0,0])) + ' '
            msg = msg + str(hr) + ':' + str(mn)
            tt = strptime(msg, '%d/%m/%Y %H:%M')  
            data_plt.DoY[count] = float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24
            
            bb = data_out.BB[((DT[:,3] == hr) & ((DT[:,4] >= mn) & (DT[:,4] < mn + 5))),:]
            #cbh = data_out.cbh[((DT[:,3] == hr) & ((DT[:,4] >= mn) & (DT[:,4] < mn + 5))),:]
            zz = data_out.ZZ[((DT[:,3] == hr) & ((DT[:,4] >= mn) & (DT[:,4] < mn + 5))),:]
            
            #dur, gates = bb.shape
            if dur > 0:
                data_plt.ZZ[count,:] = zz[0,:]
                data_plt.BB[count,:] = bb[0,:]
                #data_plt.cbh[count,:] = cbh [0,:]
    
    #QC data
    dur, gates = data_plt.BB.shape
    
    ii_min = np.where(data_plt.BB <= 1e-7)
    flagBB[ii_min] = 2
    ii_max = np.where(data_plt.BB > 0.06)
    flagBB[ii_max] = 2
    
    #filter - gate
    for i in range(gates-1):
        for ii in range(2,dur-3):
            if ((flagBB[ii-2,i]) and (flagBB[ii,i] == 1) and (flagBB[ii+2,i] != 1)):
                flagBB[ii,i] = 2
    
    #filter - time            
    for i in range(dur-1):
        for ii in range(2,gates-3):
            if ((flagBB[i,ii-2]) and (flagBB[i,ii] == 1) and (flagBB[i,ii+2] != 1)):
                flagBB[i,ii] = 2            
                
    #filter - gate
    for i in range(gates-1):            
        for ii in range(1,dur-2):
            if ((flagBB[ii-1,i]) and (flagBB[ii,i] == 1) and (flagBB[ii+1,i] != 1)):
                flagBB[ii,i] = 2
   
    #filter - time
    for i in range(dur-1):
        for ii in range(1,gates-2):
            if ((flagBB[i,ii-1]) and (flagBB[i,ii] == 1) and (flagBB[i,ii+1] != 1)):
                flagBB[i,ii] = 2
    
    np.putmask(data_plt.BB, flagBB != 1, np.nan)
    np.putmask(data_plt.CBH, data_plt.CBH < 10, np.nan)
    data_plt.BB = np.ma.masked_invalid(data_plt.BB)
    data_plt.cbh = np.ma.masked_invalid(data_plt.CBH)
    
    return data_plt
    
def data_plot(data_plt, np):
    from matplotlib import pyplot as plt
  
    #pull out data to be plotted for easy plotting
    x = (data_plt.DoY - data_plt.DoY[0]) * 24
    y = data_plt.ZZ[1,:]
    z = np.log10(data_plt.BB.transpose())
    #create figure object
    fig = plt.figure()
    #plot backscatter profile
    plt.pcolor(x, y, z, cmap='Greens', vmin = np.log10(1e-7), vmax = np.log10(0.07))
    ax = plt.gca()
    #plot cloud bases
    #line, = plt.plot(x,data_plt.cbh[:,0],'ko', label='Cloud Base 1')
    #line, = plt.plot(x,data_plt.cbh[:,1],'ks', label='Cloud Base 2')
    #line, = plt.plot(x,data_plt.cbh[:,2],'k*', label='Cloud Base 3')
    #line, = plt.plot(x,data_plt.cbh[:,3],'k^', label='Cloud Base 4')
    #get data strings
    yyyy = str(int(data_plt.DT[0,0]))
    mmmm = str(int(data_plt.DT[0,1]))
    if (len(mmmm) < 2):
        mmmm = '0' + mmmm
    dddd = str(int(data_plt.DT[0,2]))
    if (len(dddd) < 2):
        dddd = '0' + dddd
    #put on grid and labels
    ax.set_xlabel('Hour (UTC)')
    ax.set_ylabel('Height (m)')
    #ax.set_title('WAO Ceilometer: ' + dddd + '/' + mmmm + '/' + yyyy)
    ax.grid(True)
    
    cb = plt.colorbar()  
    cb.set_label(r'${log}_{10}{(Attenuated Aerosol Backscatter Coefficient)}(m^{-1} sr^{-1})$')    
    plt.legend()
  
    plt.show()
  
    return
        
def quick_look_plt(data_QC, np):       
    from collections import namedtuple 
    data_plt = namedtuple("data_plt", "")
  
    data_plt = data_means(data_QC, data_plt, np)
    data_plot(data_plt, np) 
    
    return