# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-
# FOUND SERVICE SETTINGS THAT WORK
# https://unix.stackexchange.com/questions/472950/systemd-status-203-exec-error-when-creating-new-service
# https://raspberrypi.stackexchange.com/questions/96673/i-want-to-run-a-python-3-script-on-startup-and-in-an-endless-loop-on-my-raspberr

import concurrent.futures
from api_monitor import monitor
from api_server import apiHttp

apiService = apiHttp
monitorService = monitor

def start_Service(name, service):
    try:
        print("Starting service: ", name)
        service.start()
    except Exception as e:
        print("Error starting service: ", e)

with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(start_Service("monitor", monitorService))
    f2 = executor.submit(start_Service("api", apiService))