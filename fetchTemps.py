import requests # GET POST
import fetchFans # Call function to set duty cycles
# from secrets import SECRETS # variables stored in env file

def prometheusResponse(name,url,ip):
    try:
        response = requests.get(url + '/api/v1/query',
        params={
            'query': 'round(node_thermal_zone_temp{type="cpu-thermal"})'
        })
        degree = response.json()['data']['result'][0]['value'][1]
        print(name + " Temp: "+ degree + "°")
        # getColorawait_Watch(int(watch_results))
        return degree
    except Exception:
        # DNS MDS not registered attempting internet protocal address
        print("Host Name Failed attempting IP @:" + ip)
        try:
            response = requests.get(ip + '/api/v1/query',
            params={
                'query': 'round(node_thermal_zone_temp{type="cpu-thermal"})'
            })
            degree = response.json()['data']['result'][0]['value'][1]
            print(name + " Temp: "+ degree + "°")
            return degree
        except Exception:
            print("Prometheus "+ name + " error")
            degree = "0"
            return degree
            pass # Keep code going on try catch error

def get_Color(temp, fan):
    if temp > 59:
        # set fan(x) to HIGH
        if fan != "null":
            fetchFans.set_Fan_Speed(fan, 100, "HIGH")
            # temp red
        return ["#FF0000", "HIGH"]
    elif temp > 40 and temp <= 58:
        # set fan(x) to MED
        if fan != "null":
            fetchFans.set_Fan_Speed(fan, 75, "MED")
            # temp yellow
        return ["#FFFF00","MED"]
    else:
        # set fan(x) to LOW
        if fan != "null":
            fetchFans.set_Fan_Speed(fan, 35, "LOW")
            # temp green
        return ["#00FF00","LOW"]
