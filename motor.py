import math


###########################################################
###########################################################
#ABILITA I MOTORI
def abilita(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:en', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#ABILITA L'AZIMUTH
def abilita_az(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:a:en', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#ABILITA L'ELEVAZIONE
def abilita_el(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:e:en', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#DISABILITA I MOTORI
def disabilita(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:dis', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#RIMUOVE I FRENI
def brakes_remove(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:a:b off', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	sock.sendto(b'd:e:b off', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#INSERISCE I FRENI
def brakes_insert(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:a:b on', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	sock.sendto(b'd:e:b on', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#FRENO DI EMERGENZA
def stop(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:s', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#MOVIMENTO RELATIVO DI AZIMUTH
def mvr_az(sock, UDP_IP, UDP_PORT, giri):

	parte_int = str(int(math.modf(giri)[1]))
	parte_dec = str(int(math.modf(giri)[0]*4294967295))
	
	sock.sendto(b'd:a:mvr '+ str.encode(parte_int) + b',' + str.encode(parte_dec), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)

	return data


###########################################################
###########################################################
#MOVIMENTO RELATIVO DI ELEVAZIONE
def mvr_el(sock, UDP_IP, UDP_PORT, giri):

	parte_int = str(int(math.modf(giri)[1]))
	parte_dec = str(int(math.modf(giri)[0]*4294967295))
	
	sock.sendto(b'd:e:mvr '+ str.encode(parte_int) + b',' + str.encode(parte_dec), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
		
	return data


###########################################################
###########################################################
#MOVIMENTO ASSOLUTO DI AZIMUTH
def mva_az(sock, UDP_IP, UDP_PORT, giri):

	parte_int = str(int(math.modf(giri)[1]))
	parte_dec = str(int(math.modf(giri)[0]*4294967295))
	
	sock.sendto(b'd:a:mva '+ str.encode(parte_int) + b',' + str.encode(parte_dec), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
		
	return data


###########################################################
###########################################################
#MOVIMENTO ASSOLUTO DI ELEVAZIONE
def mva_el(sock, UDP_IP, UDP_PORT, giri):

	parte_int = str(int(math.modf(giri)[1]))
	parte_dec = str(int(math.modf(giri)[0]*4294967295))#2**32=4294967296
	
	sock.sendto(b'd:e:mva '+ str.encode(parte_int) + b',' + str.encode(parte_dec), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#IMPOSTA VELOCITÀ DI AZIMUTH
def set_velaz(sock, UDP_IP, UDP_PORT, vaz):

	sock.sendto(b'd:a:posv '+ str.encode(vaz), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#IMPOSTA VELOCITÀ DI ELEVAZIONE
def set_velel(sock, UDP_IP, UDP_PORT, vel):
	
	sock.sendto(b'd:e:posv '+ str.encode(vel), (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data


###########################################################
###########################################################
#RESET DEGLI ERRORI
def fault_reset(sock, UDP_IP, UDP_PORT):

	sock.sendto(b'd:a:fr', (UDP_IP, UDP_PORT))
	sock.sendto(b'd:e:fr', (UDP_IP, UDP_PORT))
	sock.settimeout(1)
	data, _ = sock.recvfrom(1024)
	print("Answer: %s" % data)
	
	return data
