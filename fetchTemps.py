import requests # GET POST
import fetchFans # Call function to set duty cycles
from secrets import SECRETS # variables stored in env file

def fetch_Watch():
    try:
        response = requests.get(SECRETS.URL_WATCHTOWER + '/api/v1/query',
        params={
            'query': 'round(node_thermal_zone_temp{type="cpu-thermal"})'
        })
        watch_results = response.json()['data']['result'][0]['value'][1]
        print("WatchTower Temp: "+ watch_results + "°")
        # getColorawait_Watch(int(watch_results))
        return watch_results
    except Exception:
        print("Prometheus WatchTower error")
        watch_results = "0"
        return watch_results
        pass # Keep code going on try catch error

def fetch_Peons():
    try:
        response = requests.get(SECRETS.URL_PEONS + '/api/v1/query',
        params={
            'query': 'round(node_thermal_zone_temp{type="cpu-thermal"})'
        })
        peons_results = response.json()['data']['result'][0]['value'][1]
        print("Peons Temp: "+ peons_results + "°")
        # getColorawait_Peons(int(peons_results))
        return peons_results
    except Exception:
        print("Prometheus Peons error")
        peons_results = "0"
        return peons_results
        pass # Keep code going on try catch error

def fetch_Unifi():
    try:
        response = requests.get(SECRETS.URL_UNIFI + '/api/v1/query',
        params={
            'query': 'round(node_thermal_zone_temp{type="cpu-thermal"})'
        })
        unifi_results = response.json()['data']['result'][0]['value'][1]
        print("UniFi Temp: "+ unifi_results + "°")
        # getColorawait_Unifi(int(unifi_results))
        return unifi_results
    except Exception:
        print("Prometheus UniFi error")
        unifi_results = "0"
        return unifi_results
        pass # Keep code going on try catch error

def get_Color(temp, fan):
    if temp > 59:
        # set fan(x) to HIGH
        fetchFans.set_Fan_Speed(fan, 100, "HIGH")
        # temp red
        return "#00FF00"
    elif temp > 40 and temp <= 58:
        # set fan(x) to MED
        fetchFans.set_Fan_Speed(fan, 75, "MED")
        fetchFans.set_Fan_Speed(0, 75, "MED")
        # temp yellow
        return "#FFFF00"
    else:
        # set fan(x) to LOW
        fetchFans.set_Fan_Speed(fan, 35, "LOW")
        fetchFans.set_Fan_Speed(0, 35, "LOW")
        # temp green
        return "#00FF00"

def getColorawait_Watch(watch_results):
    watch_color = get_Color(watch_results)

def getColorawait_Peons(peons_results):
    peons_color = get_Color(peons_results)

def getColorawait_Unifi(unifi_results):
    unifi_color = get_Color(unifi_results)
