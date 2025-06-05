import time, pytz
from datetime import datetime
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
from parametri_solari import parametri_osservativi as param

import numpy as np
import re


def schedule_to_matrix(filename):

	matrix = np.loadtxt(filename, dtype=str, delimiter='|', skiprows=1, unpack='true')
	
	def parametri_scansione():
		global n_scan
		n_scan = len(matrix[0,:])
		global t_scan
		t_scan = float(re.split('[a-f]', matrix[13,0])[0])
		global raa_0
		raa_0 = float(re.split('[a-f]', matrix[4,0])[0])
		global dec_0
		dec_0 = float(re.split('[a-f]', matrix[5,0])[0])
		global delta_raa
		delta_raa = float(re.split('[a-f]', matrix[6,0])[0])
		global delta_dec
		delta_dec = float(re.split('[a-f]', matrix[7,0])[0])
		
		global offset_raa
		offset_raa = np.zeros(n_scan,float)
		global offset_dec
		offset_dec = np.zeros(n_scan,float)
		
		for i in range(n_scan):
			offset_raa[i] = float(re.split('[a-f]', matrix[15,i])[0])
			offset_dec[i] = float(re.split('[a-f]', matrix[16,i])[0])
	
	parametri_scansione()

	
	#for i in range(n_scan):
	
		#offset_raa[i] = float(re.split('[a-f]', matrix[15,i])[0])
		#offset_dec[i] = float(re.split('[a-f]', matrix[16,i])[0])
		
		
		#print('La scansione numero ' + str(i+1) + ' ha limiti:\n (ra_ini, dec_ini) = ('
		#+ str(raa_0 + offset_raa[i]) + ', ' + str(dec_0 + offset_dec[i]) + ')', end='\t')
		#print('\t (ra_fin, dec_fin) = ('
		#+ str(raa_0 + offset_raa[i] + delta_raa) + ', ' + str(dec_0 + offset_dec[i] + delta_dec) + ')', end='\n')


def radec_to_elaz(raascension, declination, t_scan, LOCATION):


	sun = SkyCoord(ra=raascension*u.degree, dec=declination*u.degree, frame='icrs')
	
	observing_time = t_scan
	
	if(LOCATION == 'TG'):
		observing_location = EarthLocation(lat=param.mito_lat, lon=param.mito_lon, height=param.mito_alt*u.m)

	a = AltAz(location=observing_location, obstime=observing_time)
	sun_altaz = sun.transform_to(a)
	sun_el = sun_altaz.alt * u.deg
	sun_az = sun_altaz.az * u.deg
	
	return sun_el.value, sun_az.value
