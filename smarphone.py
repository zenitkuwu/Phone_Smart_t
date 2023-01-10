from kivy.app import App
from kivy.uix.button import Button
from paho.mqtt import client as mqtt_client


broker = "mqtt.by"
port = 1883
topic = "user/zenitcu/request"
topic_pub = "user/zenitcu/command/37/"
topic_sub = "user/zenitcu/notification/37/#"
client_id = "user_zenitcu_room"
username = "zenitcu"
password = "zb7imv80"
deviceID = "CPU"
is_on = False

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,status):
    # msg = f"messages: {msg_count}"
    msg = "{\"action\":\"command/insert\",\"deviceId\":\""+deviceID+"\",\"command\":{\"command\":\"LED_control\",\"parameters\":{\"led\":\""+status+"\"}}}"
    # msg = '{"action":"command/insert","command":{"id":432436060,"command":"LED_control","timestamp":"2021-03-24T00:19:44.418","lastUpdated":"2021-03-24T00:19:44.418","userId":37,"deviceId":"s3s9TFhT9WbDsA0CxlWeAKuZykjcmO6PoxK6","networkId":37,"deviceTypeId":5,"parameters":{"led":"on"},"lifetime":null,"status":null,"result":null},"subscriptionId":1616544981034531}'
    result = client.publish(topic_pub, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

class MainApp(App):

    def __init__(self,client,**kw):
        super(MainApp,self).__init__(**kw)
        self.client = client

    def build(self):
        return Button(
                text="Led",
                size_hint=(.5, .5),
                pos_hint={'center_x': .5, 'center_y': .5},
                on_press=self.press_btn)

    def press_btn(self,instance):
        global is_on
        if is_on:
            publish(client, "0")
            instance.text = "Led ON"
            is_on = False
        else:
            publish(client, "1")
            instance.text = "Led OFF"
            is_on = True




if __name__ == '__main__':
    client = connect_mqtt()

    client.loop_start()
    MainApp(client).run()
    client.loop_stop()