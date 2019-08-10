import datetime
import time
import urllib3
# disable InsecureRequestWarning if your are working without certificate verification
# see https://urllib3.readthedocs.org/en/latest/security.html # be sure to use a recent enough urllib3 version if this fails
try: 
	urllib3.disable_warnings()
except:
	print('urllib3.disable_warnings() failed - get a recentenough urllib3 version to avoid potential InsecureRequestWarning warnings! Can and will continue though.')

# use with or without proxy
http = urllib3.PoolManager()
url = 'https://iotmmsb7af91ae6.us1.hana.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/'
#url = 'https://iotmmsi843568trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/http/data/'
#deviceID = 'b7e75e6a-0364-494b-a6c4-7a25af775ea9'
deviceID = '34d074e3-ad45-42b7-bc9f-d3ee28765424'
url = url +deviceID
headers = urllib3.util.make_headers()
#headers['Authorization'] = 'Bearer ' + '64a33a2048da5ed80a854b6789084da' 
headers['Authorization'] = 'Bearer ' + 'ecde36ac5bf57a96943c3bc34c338a6b' 
headers['Content-Type'] = 'application/json;charset=utf-8'

#I just started with random numbers, you can choose what ever you like

Rojo = 1
Verde = 1
Azul = 0

#just put in 3 rows into the DB 

for x in range(0, 10):

	current_time = int (time.time() *100) 
	timestamp =str (current_time) 

	stringRojo =  str (Rojo)
	stringVerde= str (Verde) 
	stringAzul = str (Azul) 

	print (str (current_time))
	# send message body and the corresponding payload layout that you defined in the IoT Services Cockpit
	# replace messagetypeid with id from IOT cockpit
	body='{"messageType":"6dd42e38b500568838e3","mode":"sync","messages":[{"timestamp":'
	body=body+timestamp
	
	body = body +',"Rojo":'+ stringRojo
	body = body +',"Verde":'+ stringVerde
	body = body +',"Azul":'+stringAzul+'}]}'

	print ("")
	print (body)
	r = http.urlopen('POST', url, body=body, headers=headers)
	print ("") 
	print(r.status) 
	print(r.data)









