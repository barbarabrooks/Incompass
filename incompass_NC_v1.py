def create_NC_bck_file(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'uor-ceilometer-1' #instrument name
   f2 = 'kanpur' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'aerosol-backscatter' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc
   
def create_NC_cbh_file(dout, DT):
   from netCDF4 import Dataset
   
   f1 = 'uor-ceilometer-1' #instrument name
   f2 = 'kanpur' #platform name
   mm = str(int(DT[0,1]))
   if len(mm)<2:
      mm = "0" + mm
   dd = str(int(DT[0,2]))
   if len(dd)<2:
      dd = "0" + dd   
   f3 = str(int(DT[0,0])) + mm + dd #date yyyymmdd
   f4 = 'cloud-base' #data product
   f5 = "v1" #version number
   f6 = ".nc"
   fn = dout + f1 + chr(95) + f2 + chr(95) + f3 + chr(95) + f4 + chr(95) + f5 + f6

   fn_nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   
   return fn_nc   
   
def NC_Global_Attributes(fn_nc, meta, ET):
   from datetime import datetime
   import numpy as np
   
   name = meta.loc[:, 'Name':'Name':1].values
   exp = meta.loc[:, 'Example':'Example':1].values
   pos = exp[34]
   pos = pos[0]
   ix1 = pos.find('N')
   ix2 = pos.find(',')
   ix3 = pos.find('E')
   
   lat = np.float32(pos[0:ix1])
   lon = np.float32(pos[ix2+1:ix3])
   
   pos = exp[35]
   pos = pos[0]
   ix1 = pos.find('m')
   base_height = np.float32(pos[0:ix1])
   
   for i in range(40):
      msg1 = np.array(name[i])
      msg2 = np.array(exp[i])
      fn_nc.setncattr(msg1[0], msg2[0])
   
   fn_nc.last_revised_date = datetime.utcnow().isoformat()  
   fn_nc.time_coverage_start = datetime.utcfromtimestamp(ET[0]).isoformat()
   fn_nc.time_coverage_end = datetime.utcfromtimestamp(ET[len(ET)-1]).isoformat()
   
   return lat, lon, base_height
   
def NC_Dimensions_bck(fn_nc, ET, ZZ):
   time = fn_nc.createDimension('time', len(ET) )
   altitude = fn_nc.createDimension('altitude', len(ZZ) )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1) 

def NC_Dimensions_cbh(fn_nc, ET, li):
   time = fn_nc.createDimension('time', len(ET) )
   layer_index = fn_nc.createDimension('layer_index', li )
   latitude = fn_nc.createDimension('latitude', 1)
   longitude = fn_nc.createDimension('longitude', 1)    
   
def NC_VaraiblesAndData(fn_nc, data, np, lat, lon):
   #time
   times = fn_nc.createVariable('time', np.float64, ('time',))
   #variable attributes
   times.type = 'float64'
   times.units = 'seconds since 1970-01-01 00:00:00'
   times.standard_name = 'time'
   times.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
   times.axis = 'T'
   times.valid_min = np.float64(min(data.ET))
   times.valid_max = np.float64(max(data.ET))
   times.calendar = 'standard'
   #write data
   times[:] = np.float64(data.ET)
   
   #lat
   latitudes = fn_nc.createVariable('latitude', np.float32, ('latitude',))
   #variable attributes
   latitudes.type = 'float32'
   latitudes.units = 'degrees_north'
   latitudes.standard_name = 'latitude'
   latitudes.long_name = 'Latitude'
   #write data
   latitudes[:] = np.float32(lat)
   
   #lon
   longitudes = fn_nc.createVariable('longitude', np.float32, ('longitude',))
   #variable attributes
   longitudes.type = 'float32'
   longitudes.units = 'degrees_east'
   longitudes.standard_name = 'longitude'
   longitudes.long_name = 'Longitude'
   #write data
   longitudes[:] = np.float32(lon)
   
   #doy
   doys = fn_nc.createVariable('day_of_year', np.float32, ('time',))
   #variable attributes
   doys.type = 'float32'
   doys.units = '1'
   doys.long_name = 'Day of Year'
   doys.valid_min = np.float32(min(data.DoY))
   doys.valid_max = np.float32(max(data.DoY))
   #write data
   doys[:] = np.float32(data.DoY)
   
   #year
   years = fn_nc.createVariable('year', np.int32, ('time',))
   #variable attributes
   years.type = 'int32'
   years.units = '1'
   years.long_name = 'Year'
   years.valid_min = np.int32(min(data.DT[:,0]))
   years.valid_max = np.int32(max(data.DT[:,0])) 
   #write data
   years[:] = np.int32(data.DT[:,0])
   
   #month
   months = fn_nc.createVariable('month', np.int32, ('time',))
   #variable attributes
   months.type = 'int32'
   months.units = '1'
   months.long_name = 'Month'
   months.valid_min = np.int32(min(data.DT[:,1]))
   months.valid_max = np.int32(max(data.DT[:,1])) 
   #write data
   months[:] = np.int32(data.DT[:,1])  
   
   #day
   days = fn_nc.createVariable('day', np.int32, ('time',))
   #variable attributes
   days.type = 'int32'
   days.units = '1'
   days.long_name = 'Day'
   days.valid_min = np.int32(min(data.DT[:,2]))
   days.valid_max = np.int32(max(data.DT[:,2]))
   #write data
   days[:] = np.int32(data.DT[:,2])
   
   #hour
   hours = fn_nc.createVariable('hour', np.int32, ('time',))
   #variable attributes
   hours.type = 'int32'
   hours.units = '1'
   hours.long_name = 'Hour'
   hours.valid_min = np.int32(min(data.DT[:,3]))
   hours.valid_max = np.int32(max(data.DT[:,3])) 
   #write data
   hours[:] = np.int32(data.DT[:,3])
   
   #minute
   minutes = fn_nc.createVariable('minute', np.int32, ('time',))
   #variable attributes
   minutes.type = 'int32'
   minutes.units = '1'
   minutes.long_name = 'Minute'
   minutes.valid_min = np.int32(min(data.DT[:,4]))
   minutes.valid_max = np.int32(max(data.DT[:,4]))  
   #write data
   minutes[:] = np.int32(data.DT[:,4])
   
   #second
   seconds = fn_nc.createVariable('second', np.float32, ('time',))
   #variable attributes
   seconds.type = 'float32'
   seconds.units = '1'
   seconds.long_name = 'Second'
   seconds.valid_min = np.float32(min(data.DT[:,5]))
   seconds.valid_max = np.float32(max(data.DT[:,5])) 
   #write data
   seconds[:] = np.float32(data.DT[:,5])
   
   #Laser Pulse Energy
   LPE = fn_nc.createVariable('laser_pulse_energy', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   LPE.type = 'float32'
   LPE.units = '%'
   LPE.long_name = 'Laser Pulse Energy (% of maximum)'
   LPE.valid_min = np.float32(min(data.laser_pulse_energy))
   LPE.valid_max = np.float32(max(data.laser_pulse_energy))
   LPE.cell_methods = 'time: mean'
   LPE.coordinates = 'latitude longitude'
   #write data
   LPE[:] = np.float32(data.laser_pulse_energy)
   
   #Laser Temperature
   LT = fn_nc.createVariable('laser_temperature', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   LT.type = 'float32'
   LT.units = 'K'
   LT.long_name = 'Laser Temperature'
   LT.valid_min = np.float32(min(data.laser_temperature)) + np.float32(273.15)
   LT.valid_max = np.float32(max(data.laser_temperature)) + np.float32(273.15)
   LT.cell_methods = 'time: mean'
   LT.coordinates = 'latitude longitude'
   #write data
   LT[:] = np.float32(data.laser_temperature) + np.float32(273.15)
   
   #Tilt Angle
   LTA = fn_nc.createVariable('sensor_zenith_angle', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   LTA.type = 'float32'
   LTA.units = 'degree'
   LTA.long_name = 'Sensor Zenith Angle (from vertical)'
   LTA.valid_min = np.float32(min(data.tilt_angle))
   LTA.valid_max = np.float32(max(data.tilt_angle))
   LTA.cell_methods = 'time: mean'
   LTA.coordinates = 'latitude longitude'
   #write data
   LTA[:] = np.float32(data.tilt_angle)
   
   #Window Contaminatiom
   WC = fn_nc.createVariable('window_contamination', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   WC.type = 'float32'
   WC.units = 'mV'
   WC.long_name = 'Window Contamination (mV as measured by ADC: 0 - 2500)'
   WC.valid_min = np.float32(min(data.window_contamination))
   WC.valid_max = np.float32(max(data.window_contamination))
   WC.cell_methods = 'time: mean'
   WC.coordinates = 'latitude longitude'
   #write data
   WC[:] = np.float32(data.window_contamination)
   
   #Background Light
   BL = fn_nc.createVariable('background_light', np.float32, ('time',),fill_value=-1.00e+20)
   #variable attributes
   BL.type = 'float32'
   BL.units = 'mV'
   BL.long_name = 'Background Light (mV as measured by ADC: 0 - 2500)'
   BL.valid_min = np.float32(min(data.back_light))
   BL.valid_max = np.float32(max(data.back_light))
   BL.cell_methods = 'time: mean'
   BL.coordinates = 'latitude longitude'
   #write data
   BL[:] = np.float32(data.back_light)
 
def NC_VaraiblesAndData_bck(fn_nc, data, np, base_height): 
   #Altitude 
   ALT = fn_nc.createVariable('altitude', np.float32, ('altitude',),fill_value=-1.00e+20)
   #variable attributes
   ALT.type = 'float32'
   ALT.units = 'm'
   ALT.standard_name = 'altitude'
   ALT.long_name = 'Geometric height above geoid (WGS84).'
   ALT.axis = 'Z'
   XX = data.ZZ[1,:]
   for n in range(len(data.ZZ[1,:])):
       XX[n] = data.ZZ[1,n] + base_height
       
   np.putmask(XX, (XX <= 0), np.nan)
   
   ALT.valid_min = np.float32(min(XX))
   ALT.valid_max = np.float32(max(XX))
   ALT.coordinates = 'latitude longitude'
   #write data
   ALT[:] = np.float32(XX) # only need to be an array
   
   #Aerosol backscatter
   BCK = fn_nc.createVariable('attenuated_aerosol_backscatter_coefficient', np.float32, ('time','altitude',),fill_value=-1.00e+20)
   #variable attributes
   BCK.type = 'float32'
   BCK.units = 'm-1 sr-1'
   BCK.long_name = 'Attenuated Aerosol Backscatter Coefficient'
   BB = data.BB
   np.putmask(BB, data.BB_flag != 1, np.nan)
   BCK.valid_min = np.float32(np.nanmin(np.nanmin(BB))) #apply mask then search
   BCK.valid_max = np.float32(np.nanmax(np.nanmax(BB))) #apply mask then search
   BCK.cell_methods = 'time: mean'
   BCK.coordinates = 'latitude longitude'
   #write data
   BCK[:,:] = np.float32(data.BB)
   
   #Qc flag
   qc_flags = fn_nc.createVariable('qc_flag', np.int8, ('time','altitude',))
   #variable attribute
   qc_flags.type = 'byte'
   qc_flags.units = '1'
   qc_flags.long_name = 'Data Quality Flag'
   qc_flags.flag_values = '0b,1b,2b,3b,4b'
   qc_flags.flag_meanings = 'not_used' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'good_data' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'bad_data_attenuated_aerosol_backscatter_coefficient_outside_instrument_operational_range' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'bad_data_gate_index_exceeds_number_of_measurement_gates_in_use' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags[:] = np.int8(data.BB_flag)
   
def NC_VaraiblesAndData_cbh(fn_nc, data, np, base_height): 
   #Cloud base_height
   CBH = fn_nc.createVariable('cloud_base_altitude', np.float32, ('time','layer_index',),fill_value=-1.00e+20)
   #variable attributes
   CBH.type = 'float32'
   CBH.units = 'm'
   CBH.standard_name = 'cloud_base_altitude'
   CBH.long_name = 'Cloud Base Altitude (Geometric height above geoid WGS84)'
   s = (len(data.ET),4)
   for n in range(len(data.ET)):
       for m in range(4):
          if data.cbh[n,m] < 0:
             data.cbh[n,m] = -1.00e+20
          if data.cbh[n,m] > 0:   
             data.cbh[n,m] = data.cbh[n,m] + base_height
       
   XX = data.cbh
   np.putmask(XX, (XX <= 0), np.nan)
   CBH.valid_min = np.float32(np.nanmin(np.nanmin(XX))) #apply mask then search
   CBH.valid_max = np.float32(np.nanmax(np.nanmax(XX))) #apply mask then search
   CBH.cell_methods = 'time: mean'
   CBH.coordinates = 'latitude longitude'
   #write data
   CBH[:,:] = np.float32(data.cbh)
   
   #Qc flag
   qc_flags = fn_nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   qc_flags.type = 'byte'
   qc_flags.units = '1'
   qc_flags.long_name = 'Data Quality Flag'
   qc_flags.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   qc_flags.flag_meanings = 'not_used' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'good_data' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_no_signifcant_backscatter' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_full_obscuration_determined_but_no_cloud_base_detected' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_some_obscuration_detected_but_determined_to_be_transparent' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'bad_data_raw_data_missing' + '\n'
   qc_flags.flag_meanings = qc_flags.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   qc_flags[:] = np.int8(data.cbh_flag)   
   
def NC_ceil(pd, np, dout, meta_bck, meta_cbh, data):
   #aerosol backscatter profiles
   fn_nc = create_NC_bck_file(dout, data.DT) #aerosol backscatter profiles
   lat, lon, base_height = NC_Global_Attributes(fn_nc, meta_bck, data.ET)
   NC_Dimensions_bck(fn_nc, data.ET, data.ZZ[0,:])
   NC_VaraiblesAndData(fn_nc, data, np, lat, lon)
   NC_VaraiblesAndData_bck(fn_nc, data, np, base_height)
   fn_nc.close()
   
   #cloud base height
   fn_nc = create_NC_cbh_file(dout, data.DT) #cloud base height
   lat, lon, base_height = NC_Global_Attributes(fn_nc, meta_cbh, data.ET)
   NC_Dimensions_cbh(fn_nc, data.ET, 4)
   NC_VaraiblesAndData(fn_nc, data, np, lat, lon)
   NC_VaraiblesAndData_cbh(fn_nc, data, np, base_height)
   fn_nc.close()