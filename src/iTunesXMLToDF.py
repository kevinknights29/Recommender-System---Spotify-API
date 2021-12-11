import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


def getDfFromXml(xml_file):
    
    #open the xml file and store its content in a variable
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, xml_file)
    with open(filename, 'r') as f:
        xml_data = f.read()

    #get the specific dictionary with the list of songs or tracks
    bs_xml = bs(xml_data, 'lxml')
    library = bs_xml.find('dict')
    tracklist = library.find('dict')

    #dict keys
    keys = ['Name', 'Artist', 'Album', 'Genre', 'Total Time', 'Play Count', 'Skip Count']
    
    #create a DataFrame to store the tracks' attributes
    data = pd.DataFrame()
    
    #create a dictionary for each track with the right format
    for track in tracklist.children:
        if track.name == 'dict':
            track_dict = {}
            track_children = list(track.children)
            for i, child in enumerate(track_children):
                if child.text in keys:
                    key = child.text.lower().replace(' ', '_')
                    track_dict[key] = track_children[i+1].text
                else:
                    continue
            data = data.append(track_dict, ignore_index=True)
        else:
            continue
    
    #impute NA and fill them with 0    
    data[['play_count', 'skip_count']] = data[['play_count', 'skip_count']].fillna(0)
    #convert numeric columns stored as object to np.int64
    data[['total_time', 'play_count', 'skip_count']] = data[['total_time', 'play_count', 'skip_count']].astype(np.int64)
    

    return data