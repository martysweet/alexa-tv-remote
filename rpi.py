from __future__ import print_function
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import sys
import logging
import time
import getopt

AWS_IOT_SUBSCRIBE_TOPIC = 'alexa-tv-remote'
AWS_IOT_CLIENT_ID = 'alexa-tv-remote-device'

# This should be set to your accounts endpoint, such as UNIQUE.iot.REGION.amazonaws.com
AWS_IOT_ENDPOINT = 'data.iot.eu-west-1.amazonaws.com'
AWS_IOT_ROOT_CA = 'root-CA.crt'
AWS_IOT_PRIVATE_KEY = 'private.pem.key'
AWS_IOT_CERTIFICATE = 'client.crt'

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(AWS_IOT_CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(AWS_IOT_ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(AWS_IOT_ROOT_CA, AWS_IOT_PRIVATE_KEY, AWS_IOT_CERTIFICATE)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(AWS_IOT_SUBSCRIBE_TOPIC, 1, customCallback)
time.sleep(2)