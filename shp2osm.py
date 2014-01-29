import shapefile
from sys import argv
import json
from lxml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
# read the shapefile
sf = shapefile.Reader("shp/for_edit.shp")
osm = etree.Element("osm",version='0.6', upload='true', generator='JOSM')



  #<node id='-101451' action='modify' visible='true' lat='37.7636307393908' lon='-122.48046881653359' />
nodes = [[]]
shapes = sf.shapes()

#print sf.fields
#fields = sf.fields[1:]
#field_names = [field[0] for field in fields]
#geojson = { "type": "FeatureCollection", "features": [] }

id_node=-1
print len(sf.shapeRecords())
for x in xrange(0,len(sf.shapeRecords())):  
  way = etree.SubElement(osm, "way")
  way.set('id', str(id_node))
  way.set('action','modify')
  way.set('visible','true')
  for y in xrange(0,len(shapes[x].points)):
    node = etree.SubElement(osm, "node")
    nd=etree.SubElement(way, "nd")       
    id_node=id_node+1*(-1)
    node.set('id',str(id_node))
    node.set('action','modify')
    node.set('visible','true')
    node.set('lat',str(shapes[x].points[y][1]))
    node.set('lon',str(shapes[x].points[y][0]))
    nd.set("ref", str(id_node))
  tag=etree.SubElement(way, 'tag')
  tag.set('k','building')
  tag.set('v','yes')

xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(osm, encoding='utf8').replace('"',"'")
new_file = open('new.osm', 'w')
new_file.write(xml)

