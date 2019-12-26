# -*- coding: utf-8 -*-
import logging
import requests

from modules import cbpi
from thread import start_new_thread

headers = {'content-type': '"application/x-www-form-urlencoded; charset=utf-8"'}

@cbpi.initalizer(order=999)
def init(cbpi):  # Setup BrewFather telemetry (optional)
    brew_father_url = cbpi.get_config_parameter("brew_father_url", None)
    if brew_father_url is None:
        cbpi.add_config_parameter("brew_father_url", "", "text", "Brewfather.app custom stream url; i.e. http://log.brewfather.net/stream?id=xxxxxxxxxxxxxx")


@cbpi.backgroundtask(key="brewfather_telemetry_task", interval=900) # Brewfather limits telemetry posts to once every 15 minutes per device
def brewfather_telemetry_task(api):
    brew_father_url = cbpi.get_config_parameter("brew_father_url", None)
    if brew_father_url is None:
        return False

    brew_name = cbpi.get_config_parameter("brew_name", None)

    now = datetime.datetime.now()
    for key, value in cbpi.cache.get("sensors").iteritems():
        cbpi.app.logger.info(value)
        if (value.instance.type == "ONE_WIRE_SENSOR"):
            data = {}
            data['name'] = value.instance.name
            data['temp'] = value.instance.value
            data['aux_temp'] = 0
            data['ext_temp'] = 0
            data['temp_unit'] = value.instance.unit
            data['gravity'] = 0.000
            data['gravity_unit'] = "G" #SpGr
            data['pressure'] = 0
            data['pressure_unit'] = "PSI"
            data['ph'] = 0
            data['comment'] = ""
            data['beer'] = brew_name
            r = requests.post(url, headers=headers, data=data)
            cbpi.app.logger.info("Result %s" % r.text)



