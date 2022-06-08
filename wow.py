# weather on the way
import amap
import logging


class Wow:
    'weather on the way'
    originName = ''
    destNmae = ''
    originPoint = None
    destPoint = None

    def __init__(self, originName, destNmae):
        self.originName = originName
        self.destNmae = destNmae

    def nameToPoint(self):
        self.originPoint = amap.siteNameToPoint(self.originName)
        self.destPoint = amap.siteNameToPoint(self.destNmae)

    def getWow(self):
        self.nameToPoint()
        if self.originPoint == None or self.destPoint == None:
            logging.warning("add name to point failed, oName:%s, dName:%s, oPoint:%s, dPoint:%s," % (
                self.originName, self.destNmae, self.originPoint, self.destPoint))
            return None
        pathResp = amap.getDrivePath(self.originPoint, self.destPoint)
        if pathResp == None:
            logging.warning("getDrivePath failed, oName:%s, dName:%s" % (self.originName, self.destNmae))
            return None
        pathInfo = amap.pathInfoParse(pathResp)
        if pathInfo == None:
            logging.warning("getDrivePath failed, oName:%s, dName:%s" % (self.originName, self.destNmae))
            return None
        return amap.addWeaInfoToPathInfo(pathInfo)
