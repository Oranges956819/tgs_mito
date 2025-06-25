class parametri_osservativi():
	#Via Celoria 16, Milano
	milano_lat = 45.47640
	milano_lon = 9.23069
	milano_alt = 100 #in metri sul livello del mare
	
	#Testa Grigia, Milano
	mito_lat = 45.935381 #latitudine Plateau Rosà
	mito_lon = 7.707319 #longitudine Plateau Rosà
	mito_alt = 3480 #altitudine Plateau Rosà

	

































import time, pytz
from datetime import datetime
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz



def radec_to_el(raascension, declination):


	sun = SkyCoord(ra=raascension*u.degree, 
	dec=(declination+coord_dec_ofs[i]/np.cos(coord_dec_ini[i]))*u.degree, frame='icrs')
	
	observing_time = datetime.now(pytz.UTC)
	observing_location = EarthLocation(lat=observing_lat, lon=observing_lon, height=observing_alt*u.m)  

	a = AltAz(location=observing_location, obstime=observing_time)
	sun_altaz = sun.transform_to(a)
	sun_el = sun_altaz.alt * u.deg
	
	return sun_el.value


def radec_to_az(raascension, declination):

	sun = SkyCoord(ra=coord_ra_ini[i]*u.degree, 
	dec=(coord_dec_ini[i]+coord_dec_ofs[i]/np.cos(coord_dec_ini[i]))*u.degree, frame='icrs')
	
	observing_time = datetime.now(pytz.UTC)
	observing_location = EarthLocation(lat=observing_lat, lon=observing_lon, height=observing_alt*u.m)  

	a = AltAz(location=observing_location, obstime=observing_time)
	sun_altaz = sun.transform_to(a)
	sun_az = sun_altaz.az * u.deg
	
	return sun_az.value
