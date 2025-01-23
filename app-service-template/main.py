# Copyright (C) 2024 IOTech Ltd
# SPDX-License-Identifier: Apache-2.0
"""
This acts sample code for creating and initializing a custom ApplicationService instance
`app_new_service`.
"""
import asyncio
import os


### OPENLEADR Libraries begin

##  Dependencies
"""
Most dependencies are taken care of through pip install
"""
from datetime import timedelta

##  Modules
from openleadr.client import OpenADRClient
from openleadr.server import OpenADRServer

### OPENLEADR Libraries end

from app_functions_sdk_py.functions import mqtt, filters
from app_functions_sdk_py.factory import new_app_service
from app_functions_sdk_py.utils.factory.mqtt import MQTTClientConfig

#OPENLEADR Variables Initiated
myOpenADRClient = OpenADRClient("CLIENT1", "127.0.0.1", False, "", "", "", "", True, "", True, "", False, True, 10, 300)
myOpenADRServer = OpenADRServer("SERVER1", "", "", "", "", True, 8080, "127.0.0.1", "", "", "", "/OpenADR2/Simple/2.0b", timedelta(seconds=10), "", "", True, True)

#OPENLEADR Instances end

class MyApp:
    def __init__(self):
        self.service_key = "app-new-service"

    def create_and_run_service(self) -> int:
        """
        Creates and runs a new application service
        """
        # create a new application service
        service, result = new_app_service(self.service_key)
        if result is False:
            return -1

        # set up the MQTT sender configuration
        mqtt_config = MQTTClientConfig(
            broker_address="test.mosquitto.org",
            client_id="test_client",
            topic="test_topic",
            secret_name="",
            auth_mode="none")

        # set the application service with filter_by_device_name and mqtt_send for default functions
        # pipeline
        service.set_default_functions_pipeline(
            # filter for events coming from Random-Integer-Device
            filters.new_filter_for(filter_values=["Random-Integer-Device"]).filter_by_device_name,
            # send the event to the external MQTT broker
            mqtt.new_mqtt_sender(mqtt_config=mqtt_config).mqtt_send
        )

        # run the service
        asyncio.run(service.run())
        return 0


if __name__ == "__main__":
    app = MyApp()
    code = app.create_and_run_service()
    os._exit(code)
