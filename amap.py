# https://lbs.amap.com/api/webservice/guide/api
import requests
import logging
import json
from time import sleep

apikey = 'f20d630651f6fab38a0cc7610cc4f134'
logging.basicConfig(level=logging.INFO)


def myGetRequst(url, data):
    resp = requests.get(url=url, params=data)
    retry = 0
    while resp.text == None and retry < 5:
        retry = retry + 1
        logging.warning("myGetRequst failed sleep 3s, url:%s, data:%s" % (url, data))
        sleep(3)
        resp = requests.get(url=url, params=data)
    return resp


# 将地点名称转换为经纬度点，转换失败返回None
def siteNameToPoint(addrName):
    logging.info("call siteNameToPoint, trans addrname:%s" % addrName)
    if str(addrName) == '':
        logging.warning('siteNameToPoint failed, addrName: %s' % addrName)
        return None
    url = 'http://restapi.amap.com/v3/geocode/geo'
    data = {
        "key": apikey,
        "address": addrName
    }
    resp = myGetRequst(url, data)
    respJson = json.loads(resp.text)
    if respJson["status"] != "1":
        # 返回失败
        print(resp.text)
        logging.warning("siteNameToPoint failed, addrName:%s, status:%s, info:%s" % (
            addrName, respJson["status"], respJson["info"]))
        return None
    else:
        point = respJson["geocodes"][0]["location"]
        return point


'''
将路径规划返回的json数据处理成需要的数据
{
count:x
route:[
{
"distance":xx
"costTime":xx
"costMoney":xx
"crosscitys":[{adcode:xx, name:xx},{}]
"crossdistricts":[{name:xx, adcode:xx},{}]
},
...
]
}
'''


def pathInfoParse(pathJson):
    if pathJson == None or pathJson["status"] != "1":
        logging.warning('pathInfoParse failed, pathJson: %s' % pathJson)
        return None
    pathRet = {}
    count = int(pathJson["count"])
    pathRet["count"] = count
    pathRet["route"] = []
    for i in range(count):
        tmp = {}
        tmp["distance"] = int(pathJson["route"]["paths"][i]["distance"])
        tmp["costTime"] = int(pathJson["route"]["paths"][i]["cost"]["duration"])
        tmp["costMoney"] = int(pathJson["route"]["paths"][i]["cost"]["tolls"])
        tmp["citys"] = []
        tmp["crossdistricts"] = []
        tmp["crosscitys"] = []
        for step in pathJson["route"]["paths"][i]["steps"]:
            cityInfo = {}
            for city in step["cities"]:
                cityInfo["adcode"] = city["adcode"]
                cityInfo["name"] = city["city"]
                if cityInfo not in tmp["crosscitys"]:
                    tmp["crosscitys"].append(cityInfo)
                districtInfo = {}
                for district in city["districts"]:
                    districtInfo["name"] = district["name"]
                    districtInfo["adcode"] = district["adcode"]
                    if districtInfo not in tmp["crossdistricts"]:
                        tmp["crossdistricts"].append(districtInfo)
        pathRet["route"].append(tmp)
    return pathRet


# 输入起始点经纬度，返回驾车路线信息
def getDrivePath(orgin, dest):
    logging.info("call getDrivePath, form %s to %s" % (orgin, dest))
    url = 'http://restapi.amap.com/v5/direction/driving'
    data = {
        "key": apikey,
        "origin": orgin,
        "destination": dest,
        "show_fields": "cost,tmcs,cities"
    }
    resp = myGetRequst(url, data)
    respJson = json.loads(resp.text)
    if respJson["status"] != "1":
        # 返回失败
        print(resp.text)
        logging.warning("getDrivePath failed, orgin:%s, dest:%s, status:%s, info:%s" % (
            orgin, dest, respJson["status"], respJson["info"]))
        return None
    else:
        return respJson


'''
{
city:xx
province:xx
daycount:xx
casts:[{date:xx, dayweather:xx, nightweather:xx, daytemp:xx, nighttemp:xx}, {}]
}
'''


def weatherInfoParse(wInfo):
    if wInfo == None or wInfo["status"] != "1":
        logging.warning('weatherInfoParse failed, wInfo: %s' % wInfo)
        return None
    retWeaInfo = {}
    retWeaInfo["city"] = wInfo["forecasts"][0]["city"]
    retWeaInfo["province"] = wInfo["forecasts"][0]["province"]
    retWeaInfo["daycount"] = len(wInfo["forecasts"][0]["casts"])
    retWeaInfo["casts"] = []
    for cast in wInfo["forecasts"][0]["casts"]:
        tmpCast = {}
        tmpCast["date"] = cast["date"]
        tmpCast["dayweather"] = cast["dayweather"]
        tmpCast["nightweather"] = cast["nightweather"]
        tmpCast["nighttemp"] = cast["nighttemp"]
        tmpCast["daytemp"] = cast["daytemp"]
        retWeaInfo["casts"].append(tmpCast)
    return retWeaInfo


# 输入城市adcode编码，返回城市天气信息
def getCityWeather(adcode):
    logging.info("call getCityWeather, get weather of adcode:%s" % adcode)
    url = 'http://restapi.amap.com/v3/weather/weatherInfo'
    data = {
        "key": apikey,
        "city": adcode,
        "extensions": "all",
    }
    resp = myGetRequst(url, data)
    respJson = json.loads(resp.text)
    if respJson["status"] != "1":
        # 返回失败
        print(resp.text)
        logging.warning("getCityWeather failed, adcode:%s" % (adcode))
        return None
    else:
        return respJson


'''
{
count:x
route:[
{
"distance":xx
"costTime":xx
"costMoney":xx
"crosscitys":[{adcode:xx, name:xx, weather:{xxx}},{}]
"crossdistricts":[{name:xx, adcode:xx, weather:{xxx}},{}]
},
...
]
}
'''


# 查询途径城市的天气并插入到pathInfo中
def addWeaInfoToPathInfo(pathInfo):
    if pathInfo == None or pathInfo["count"] == 0:
        logging.warning("addWeaInfoToPathInfo failed, pathInfo:%s" % (pathInfo))
        return None
    for route in pathInfo["route"]:
        for city in route["crosscitys"]:
            weaResp = getCityWeather(city["adcode"])
            city["weather"] = weatherInfoParse(weaResp)
        for district in route["crossdistricts"]:
            weaResp = getCityWeather(district["adcode"])
            district["weather"] = weatherInfoParse(weaResp)
    return pathInfo
