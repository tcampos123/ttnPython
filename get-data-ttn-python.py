# Get data from TTN Console using Python

import paho.mqtt.client as mqtt
import json
import base64

#----------------------------------------------
#          Configure these values!

APPEUI = "..."      #Application EUI
APPID = "..."              #Application ID
PSW = "..."    #ACCESS KEYS

#-----------------------------------------------

def on_connect(client, userdata, flags, rc):
    client.subscribe('+/devices/+/up'.format(APPEUI))

def on_message(client, userdata, msg):
    j_msg = json.loads(msg.payload.decode('utf-8'))
    dev_eui = j_msg['hardware_serial']
    data_sensor = base64.b64decode(j_msg['payload_raw'])

    # print data
    sensor = str(data_sensor)                 #Transform to string
    l_data=len(sensor)                        #Length of String
    print('---')
    print('data:',sensor[2:l_data-1])         #Select String Array
    print('dev eui: ', dev_eui)
    print('---')
# set paho.mqtt callback
ttn_client = mqtt.Client()
ttn_client.on_connect = on_connect
ttn_client.on_message = on_message

ttn_client.username_pw_set(APPID, PSW)
ttn_client.connect("thethings.meshed.com.au", 1883, 60)

try:
    ttn_client.loop_forever()
except KeyboardInterrupt:
    print('disconnect')
    ttn_client.disconnect()
