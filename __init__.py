# -*- coding: utf-8 -*-
import logging
import requests
# import json

from modules import cbpi
from thread import start_new_thread

headers = {'content-type': '"application/json; charset=utf-8"'}
unit = "F"

@cbpi.initalizer(order=999)
def init(cbpi):  # Setup BrewFather telemetry (optional)
    global unit
    unit = cbpi.get_config_parameter("unit", "F")
    brew_father_url = cbpi.get_config_parameter("brew_father_url", None)
    if brew_father_url is None:
        cbpi.add_config_parameter("brew_father_url", "", "text", "Brewfather.app custom stream url; i.e. http://log.brewfather.net/stream?id=xxxxxxxxxxxxxx")


@cbpi.backgroundtask(key="brewfather_telemetry_task", interval=900) # Brewfather limits telemetry posts to once every 15 minutes per device
def brewfather_telemetry_task(api):
    brew_father_url = cbpi.get_config_parameter("brew_father_url", None)
    if brew_father_url is None:
        return False

    brew_name = cbpi.get_config_parameter("brew_name", None)

    for key, value in cbpi.cache.get("sensors").iteritems():
        if (value.type == "ONE_WIRE_SENSOR"):
            data = {}
            data['name'] = value.name
            data['temp'] = value.instance.last_value
            data['aux_temp'] = 0.0
            data['ext_temp'] = 0.0
            data['temp_unit'] = unit
            data['gravity'] = 0.000
            data['gravity_unit'] = "G" #SpGr
            data['pressure'] = 0
            data['pressure_unit'] = "PSI"
            data['ph'] = 0.0
            data['comment'] = "BrewfatherTelemetry"
            data['beer'] = brew_name
            # cbpi.app.logger.info("brewfather_telemetry: JSON %s" % json.dumps(data))
            r = requests.post(brew_father_url, json=data)
            cbpi.app.logger.info("brewfather_telemetry: Result %s" % r.text)

