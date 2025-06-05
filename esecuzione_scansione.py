import numpy as np
import time, pytz, sys, os, socket
import motor as drive
import convertitore_schedule as sched
from datetime import datetime, timedelta

LOCATION = 'TG'

UDP_IP = "192.168.1.5" ; UDP_PORT = 1700
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



#Creo cartella e file di log
t_now = datetime.now(pytz.UTC)
if not os.path.isdir('LOGdir/' + str(t_now.strftime('%Y-%m-%d')) + '/'): os.makedirs('LOGdir/' + str(t_now.strftime('%Y-%m-%d')) + '/')
filelog = open('LOGdir/' + str(t_now.strftime('%Y-%m-%d')) + '/log_' + str(t_now.strftime('%Y-%m-%dT%Hh%Mm%Ss')) + '.txt', 'w')
filelog.write('N | DATETIME | POS-RAA | POS-DEC | POS-AZ | POS-EL | GIRI-AZ | GIRI-EL | VEL-AZ | VEL-EL\n')



#Elaboro il file lis ottenendo gli input che mi interessano
filename = sys.argv[1]
sched.schedule_to_matrix(filename)



#Calcolo punto di inizio scansione per una prima fase di avvicinamento del telescopio
print('\n1. Movimento sul primo punto della mappa')
declination = sched.dec_0 + sched.offset_dec[0] - sched.delta_dec / 2
raascension = sched.raa_0 + (sched.offset_raa[0] - sched.delta_raa / 2 ) / np.cos(np.radians(declination))
el_deg, az_deg = sched.radec_to_elaz(raascension, declination, t_now, LOCATION) #converto raa-dec in el-az
giri_el_0 = 2668 - (90 - el_deg) * 100 #converto angoli in giri per il motore
#giri_az_0 = (180 - (az_deg - 70)) * 100 + 3955
giri_az_0 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955
print('\t1.1. Rimozione freni e abilitazione dei motori')
drive.brakes_remove(sock, UDP_IP, UDP_PORT) ; drive.abilita(sock, UDP_IP, UDP_PORT)
print('\t1.2. Impostazione delle velocità')
v_el = str(20000000) ; v_az = str(25000000)
drive.set_velel(sock, UDP_IP, UDP_PORT, v_el) ; drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)
print('\t1.3. Comando movimenti')
drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_0) ; drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_0)
print('\t1.4. Sleep di 5s per terminare il movimento\n')
time.sleep(30)




print('Inizio scansioni ...\n\n') ; t_slew = 1
for i in range(sched.n_scan):
	
	print('Scansione ' + str(i+1) + '/' + str(sched.n_scan),'\t',
	datetime.now(pytz.UTC).strftime("%Hh%Mm%Ss"))
	
	
	
	#CONVERSIONE DA COORDINATE RAA-DEC A COORDINATE EL-AZ
	obs_time = datetime.now(pytz.UTC) + timedelta(seconds=t_slew)
	if(i%2==0):
		declination = sched.dec_0 + sched.offset_dec[i] - sched.delta_dec / 2
		raascension = sched.raa_0 + (sched.offset_raa[i] - sched.delta_raa / 2 ) / np.cos(np.radians(declination))
		el_deg, az_deg = sched.radec_to_elaz(raascension, declination, obs_time, LOCATION)
	
	else:
		declination = sched.dec_0 + sched.offset_dec[i] + sched.delta_dec / 2
		raascension = sched.raa_0 + (sched.offset_raa[i] + sched.delta_raa / 2 ) / np.cos(np.radians(declination))
		el_deg, az_deg = sched.radec_to_elaz(raascension, declination, obs_time, LOCATION)
	
	
	
	#IMPOSTAZIONE VELOCITÀ E COMANDO MOVIMENTI
	v_el = str(20000000) ; v_az = str(20000000)
	drive.set_velel(sock, UDP_IP, UDP_PORT, v_el) ; drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)
	giri_el_0 = 2668 - (90 - el_deg) * 100 #; giri_az_0 = (180 - (az_deg - 70)) * 100 + 3955 #conversione angoli giri
	giri_az_0 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955
	drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_0) ; drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_0)
	
	
	
	#SCRITTURA SU FILE
	filelog.write(str(i+1) + ' | ' + str(obs_time.strftime("%Hh%Mm%Ss")) + ' | '
	+ str(raascension) + ' | ' + str(declination) + ' | ' + str(az_deg) + ' | '
	+ str(el_deg) + ' | ' + str(giri_az_0) + ' | ' + str(giri_el_0) + ' | '
	+ str(v_az) + ' | ' + str(v_el) + '\n')
	
	
	
	#TEMPO DI RIPOSO DURANTE LO SLEW
	print('Attendere movimento di slew ...')
	time.sleep(t_slew)
	#time.sleep(5) #ulteriori secondi di sleep
	time.sleep(1)
	
	
	
	
	
	
	#CONVERSIONE DA COORDINATE RAA-DEC A COORDINATE EL-AZ
	obs_time = datetime.now(pytz.UTC) + timedelta(seconds=sched.t_scan)
	if(i%2==0):
		declination = sched.dec_0 + sched.offset_dec[i] + sched.delta_dec / 2
		raascension = sched.raa_0 + (sched.offset_raa[i] + sched.delta_raa / 2 ) / np.cos(np.radians(declination))
		el_deg, az_deg = sched.radec_to_elaz(raascension, declination, obs_time, LOCATION)
	
	else:
		declination = sched.dec_0 + sched.offset_dec[i] - sched.delta_dec / 2
		raascension = sched.raa_0 + (sched.offset_raa[i] - sched.delta_raa / 2 ) / np.cos(np.radians(declination))
		el_deg, az_deg = sched.radec_to_elaz(raascension, declination, obs_time, LOCATION)
	
	
	
	#CONVERSIONE DA ANGOLI A GIRI
	giri_el_1 = 2668 - (90 - el_deg) * 100# ; giri_az_1 = (180 - (az_deg - 70)) * 100 + 3955
	giri_az_1 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955
	delta_giri_el = np.abs(giri_el_1 - giri_el_0) ; delta_giri_az = np.abs(giri_az_1 - giri_az_0)

	#CALCOLO VELOCITÀ DI SCANSIONE
	v_el = str(int(delta_giri_el * 8.544 * 10000 * 2 * np.pi / sched.t_scan))
	v_az = str(int(delta_giri_az * 8.544 * 10000 * 2 * np.pi / sched.t_scan))
	
	#IMPOSTA VELOCITÀ E COMANDA MOVIMENTI
	drive.set_velel(sock, UDP_IP, UDP_PORT, v_el) ; drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)
	drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_1) ; drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_1)
	
	
	
	#SCRITTURA SU FILE
	filelog.write(str(i+1) + ' | ' + str(obs_time.strftime("%Hh%Mm%Ss")) + ' | '
	+ str(raascension) + ' | ' + str(declination) + ' | ' + str(az_deg) + ' | '
	+ str(el_deg) + ' | ' + str(giri_az_1) + ' | ' + str(giri_el_1) + ' | '
	+ str(v_az) + ' | ' + str(v_el) + '\n')
	
	
	
	#TEMPO DI RIPOSO DURANTE LA SCANSIONE
	print('Attendere movimento di scan ...', end='\n\n')
	time.sleep(sched.t_scan)
	#time.sleep(20) #ulteriori secondi di sleep
	time.sleep(2)



sock.close()
filelog.close()
