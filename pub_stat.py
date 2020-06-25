import paho.mqtt.client as mqtt
import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import os
import re
import psutil
import mqconfig

MQ_HOST = mqconfig.mq_host
MQ_TITLE = mqconfig.mq_title

count = 0
def on_connect(client, userdata, flags, rc):
    print("Connect result: {}".format(mqtt.connack_string(rc)))
    client.connected_flag = True

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count    
    try:    
        count +=1
        payload_string = msg.payload.decode('utf-8')
        print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))
    except Exception as e:
        print ("Exception", e)

def pubTempData(client, freq=10, limit=100):
    try:    
        delta = 1/freq
    
        for i in range(limit*freq):
            ti = datetime.now()
            temp = os.popen("vcgencmd measure_temp").readline()
            da = re.findall(r'\d+\.\d+',temp.rstrip())[0]
            
            cpu_percent = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            available = round(memory.available/1024.0/1024.0,1)
            total = round(memory.total/1024.0/1024.0,1)

            row = "{:s}, {:s}, {:.1f}, {:.1f}, {:.1f}".format(ti.strftime("%Y-%m-%d %H:%M:%S.%f"), da, cpu_percent, total, total - available)
            client.publish(MQ_TITLE,payload=row, qos=1)
            if i%freq == 0:
                print (i, row)
            time.sleep(delta)
    except Exception as e:
        print ("Exception", e)

if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("test")
    client.username_pw_set(mqconfig.mq_user, password=mqconfig.mq_password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(MQ_HOST))
    client.connect(MQ_HOST, port=1883, keepalive=120)
    print ("connected {} ".format(MQ_HOST))
    client.loop_start()
    pubTempData(client)

    print ("sleep end")
    client.loop_stop()

