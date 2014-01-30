import datetime
import logging
import sys
from lxml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import fiona

osm = etree.Element("osm",version='0.6', upload='true', generator='JOSM')
   	
source = fiona.open('shp/test_multipoligon.shp', 'r') #test_multipoligon #sf3_wgs84_reduce
	#print source.schema
print 'Length of source  %d' % (len(source))
id_node=0
for f in source:
	print 'Numero de forma en este geometry %d' % (len(f['geometry']['coordinates']))
	if len(f['geometry']['coordinates'])==1:
		print 'polygono'
		id_node=id_node+1*(-1)
  		#polygono(f,id_node)
  		way = etree.SubElement(osm, "way")
		way.set('id', str(id_node))
		way.set('action','modify')
		way.set('visible','true')
		tag=etree.SubElement(way, 'tag')
		tag.set('k','building')
		tag.set('v','yes')

		for x in xrange(0,len(f['geometry']['coordinates'][0])):
		  	#print x
			#print len(f['geometry']['coordinates'][0])
			id_node=id_node+1*(-1)
			#print id_node
			node = etree.SubElement(osm, "node")
			nd=etree.SubElement(way, "nd")
			node.set('id',str(id_node))
			nd.set("ref", str(id_node))
			node.set('action','modify')
			node.set('visible','true')
			node.set('lat',str(f['geometry']['coordinates'][0][x][1]))
			node.set('lon',str(f['geometry']['coordinates'][0][x][0]))
	else :
		print 'Multipoligon'
		relation = etree.SubElement(osm, "relation")
		id_node=id_node+1*(-1)
		relation.set('id',str(id_node))
		relation.set("ref", str(id_node))
		tag1=etree.SubElement(relation, 'tag')
		tag2=etree.SubElement(relation, 'tag')
		tag1.set('k','building')
		tag1.set('v','yes')
		tag2.set('k','type')
		tag2.set('v','multipolygon')
		#print 'y cordenadas %d' % (len(f['geometry']['coordinates'][0]))
		num_cordenadas=[]
		id_way=[]
		for x in xrange(0,len(f['geometry']['coordinates'])):					
  			way = etree.SubElement(osm, "way")			
			way.set('action','modify')
			way.set('visible','true')
			member = etree.SubElement(relation, "member")
			member.set('type', 'way')
			id_node=id_node+1*(-1)
			way.set('id', str(id_node))
			member.set('ref',str(id_node))
			num_cordenadas.append(len(f['geometry']['coordinates'][x]))
			id_way.append(id_node)
			for y in xrange(0,len(f['geometry']['coordinates'][x])):
				node = etree.SubElement(osm, "node")
				nd=etree.SubElement(way, "nd")
				id_node=id_node+1*(-1)  
				node.set('id',str(id_node))
				nd.set("ref", str(id_node))
				node.set('action','modify')
				node.set('visible','true')
				node.set('lat',str(f['geometry']['coordinates'][x][y][1]))
				node.set('lon',str(f['geometry']['coordinates'][x][y][0]))

			#print num_cordenadas
			#print id_way	
			#print num_cordenadas.index(max(num_cordenadas))
			#member.set('role','outer')
			#member.set('role','inner')

			#print len(f['geometry']['coordinates'][0][x])

xml = "<?xml version='1.0' encoding='UTF-8'?>\n"+etree.tostring(osm, encoding='utf8').replace('"',"'")
new_file = open('new_1545.osm', 'w')
new_file.write(xml)



		