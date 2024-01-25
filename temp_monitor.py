import subprocess
import re
import time
from typing import List
from mqtt import MQTT
import sys 

REFRESH_INTERVAL_S = 30

broker = 'broker.emqx.io'
port = 1883
topic = "ece382/aeybel-jason-ultra96/temp"
client_id = "ultra96"

def getTemps() -> List[float]:
    sensors_output = subprocess.run(
        ['sensors','iio_hwmon-isa-0000'],
        stdout=subprocess.PIPE
    )
    temperature_output = subprocess.run(
        ['grep','temp'],
        input=sensors_output.stdout,
        stdout=subprocess.PIPE
    )
    stripped_bytestring = temperature_output.stdout.rstrip()
    temp_list = stripped_bytestring.decode("utf-8").split()[1::2]
    temps = list(map(lambda t: float(re.search(r"[-+]?\d*\.\d+|\d+", t).group()),temp_list))
    return temps

def publish_temp(client) -> None:
     while True:
        time.sleep(REFRESH_INTERVAL_S)
        temps = getTemps()
        
        for idx,temp in enumerate(temps):
            temp_topic = topic+"/"+str(idx)
            result = client.publish(temp_topic, temp)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                pass
                # print(f"Message sent")
            else:
                print(f"Failed to send message to topic {temp_topic}")

def main():
    broker = sys.argv[1]
    port = int(sys.argv[2])
    topic = sys.argv[3]
    client_id = sys.argv[4]
    mqtt = MQTT(broker,port,client_id)
    client = mqtt.connect_mqtt()
    client.loop_start()
    publish_temp(client)
    client.loop_stop()

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        main()
