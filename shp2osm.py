import shapefile
import argparse
import xml.etree.ElementTree as et

class SHP2OSM:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.osm_data = None

    def shp2osm(self):
        self.read_shp()
        self.to_osm_data()
        self.write_osm()

    def read_shp(self):
        self.sf = shapefile.Reader(self.input)
        self.shapes = self.sf.shapes()

    def to_osm_data(self):
        osm = et.Element("osm",version='0.6', upload='true', generator='JOSM')
        id_node = -1
        size = len(self.sf.shapeRecords())
        for x in range(size):  
            way = et.SubElement(osm, "way")
            way.set('id', str(id_node))
            way.set('action', 'modify')
            way.set('visible', 'true')
            for y in range(len(self.shapes[x].points)):
                node = et.SubElement(osm, "node")
                id_node = id_node + 1*(-1)
                node.set('id', str(id_node))
                node.set('action', 'modify')
                node.set('visible', 'true')
                node.set('lat', str(self.shapes[x].points[y][1]))
                node.set('lon', str(self.shapes[x].points[y][0]))
                
                nd = et.SubElement(way, "nd")       
                nd.set("ref", str(id_node))
                
                tag = et.SubElement(way, 'tag')
                tag.set('k','building')
                tag.set('v','yes')

        self.osm_data = et.tostring(osm)

    def write_osm(self):
        with open(self.output, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
        with open(self.output, 'a+b') as f:
            f.write(self.osm_data)

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--input', dest='input', default='G:/dataset/sample数据/hc_51world_1020/laneline.shp')
    parse.add_argument('--output', dest='output', default='./laneline.osm')# 'G:/dataset/sample数据/laneline.osm'
    arg = parse.parse_args()
    trans = SHP2OSM(arg.input, arg.output)
    trans.shp2osm()



