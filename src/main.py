import pandas as pd
from iTunesXMLToDF import getDfFromXml

itunes_xml = r'../ref/itunes_library.xml'

tracks_data = getDfFromXml(itunes_xml)

print(tracks_data)


