# coding:utf-8
import wow
import logging


def wowInfoToCsv(wowInfo, orgName, dstName, csvfileName):
    csvStr = ""
    csvStr += "出发地：,%s\n目的地：,%s\n从出发地到目的地一共有%s条路径方案。\n" % (orgName, dstName, wowInfo["count"])
    cnt = 1
    for route in wowInfo["route"]:
        csvStr += "路径方案%s：,总里程 %s米,总耗时 %s分钟,高速费%s元\n途径城市天气状况：\n" % (
            cnt, route["distance"], route["costTime"], route["costMoney"])
        csvStr += "省份,城市,"
        for cast in route["crosscitys"][0]["weather"]["casts"]:
            csvStr += "%s白天,%s晚上," % (cast["date"], cast["date"])
        csvStr += "\n"
        for crosscity in route["crosscitys"]:
            weatherInfo = crosscity["weather"]
            csvStr += "%s,%s" % (weatherInfo["province"], weatherInfo["city"])
            for cast in weatherInfo["casts"]:
                csvStr += ",%s(%s度),%s(%s度)" % (
                    cast["dayweather"], cast["daytemp"], cast["nightweather"], cast["nighttemp"])
            csvStr += "\n"
        cnt = cnt + 1
        csvStr += "\n\n"
    with open(csvfileName, "w") as f:
        f.write(csvStr)


logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    orgName = "江苏省南通市如东县双甸镇石甸大桥"
    dstName = "湖南省张家界市慈利县龙潭河镇"
    weatherOnWay = wow.Wow(originName=orgName, destNmae=dstName)
    wowInfo = weatherOnWay.getWow()
    if wowInfo == None:
        logging.warning("getWow failed, orgName:%s , dstName:%s " % (orgName, dstName))
    else:
        print("出发地：%s\r\n目的地：%s\r\n从出发地到目的地一共有%s条路径方案。" % (orgName, dstName, wowInfo["count"]))
        cnt = 1
        for route in wowInfo["route"]:
            print("路径方案%s：\t 总里程 %s米\t总耗时 %s分钟\t高速费%s元\r\n途径城市天气状况：" % (
                cnt, route["distance"], route["costTime"], route["costMoney"]))
            print("省份\t城市", end='')
            for cast in route["crosscitys"][0]["weather"]["casts"]:
                print("\t%s白天\t%s晚上" % (cast["date"], cast["date"]), end='')
            print("\r\n", end='')
            for crosscity in route["crosscitys"]:
                weatherInfo = crosscity["weather"]
                print("%s\t%s" % (weatherInfo["province"], weatherInfo["city"]), end='')
                for cast in weatherInfo["casts"]:
                    print("\t%s(%s度)\t%s(%s度)" % (
                        cast["dayweather"], cast["daytemp"], cast["nightweather"], cast["nighttemp"]), end='')
                print("\r\n", end='')
            cnt = cnt + 1
            print("\r\n\r\n", end='')
        wowInfoToCsv(wowInfo, orgName, dstName, "wow.csv")
