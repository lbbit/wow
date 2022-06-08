# coding:utf-8
import unittest
import amap


class TestAmap(unittest.TestCase):
    def test_siteNameToPoint(self):
        addrStr = "江苏省苏州市江韵路9号华为苏州研究所"
        pointStr = "120.729470,31.261424"
        retStr = amap.siteNameToPoint(addrStr)
        self.assertEqual(retStr, pointStr)
        addrStr = "江苏省南通市如东县双甸镇石甸大桥"
        pointStr = "120.779098,32.349526"
        retStr = amap.siteNameToPoint(addrStr)
        self.assertEqual(retStr, pointStr)

    def test_getDrivePath(self):
        point1 = "120.729470,31.261424"
        point2 = "120.779098,32.349526"
        retStr = amap.getDrivePath(point1, point2)
        self.assertNotEqual(retStr, None)
        print(retStr)
        retInfo = amap.pathInfoParse(retStr)
        self.assertNotEqual(retInfo, None)
        print(retInfo)
        retweaInfo = amap.addWeaInfoToPathInfo(retInfo)
        print(retweaInfo)

    def test_getCityWeather(self):
        retInfo = amap.getCityWeather("320500")
        self.assertNotEqual(retInfo, None)
        print(retInfo)
        retInfo = amap.getCityWeather("320623")
        self.assertNotEqual(retInfo, None)
        print(retInfo)
        weaInfo = amap.weatherInfoParse(retInfo)
        self.assertNotEqual(weaInfo, None)
        print(weaInfo)


if __name__ == '__main__':
    unittest.main()
