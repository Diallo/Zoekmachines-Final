"""
Description
"""
import ast
import config
import json
import requests
import urllib
from datetime import datetime as dt

class TedTalk:
    def __init__(self, talk_id, get_related=False):
        with open(config.DEFAULT_DATA_PATH, 'r') as file:
            data = json.load(file)
        for t in data:
            if int(t['_id']) == talk_id:
                self.data = t
                break
        else:
            # Executed if no talk is found
            raise ValueError('Unknown Talk ID')
        
        # Generate embed url
        s1 = self.data['url'].split('www', 1)
        self.embed = f"{s1[0]}embed{s1[1]}"
        
        # Get name without speaker
        self.name = self.data['name'].split(": ")[1]
        
        # Get tag string
        self.tags = ", ".join(ast.literal_eval(self.data['tags']))
        
        # Get talk info
        try:
            self.info = requests.get(f"https://www.ted.com/services/v1/oembed.json?url="
                                     f"{self.data['url']}").json()
        except Exception:
            self.info = {'thumbnail_url': "https://www.nationalacademic.nl/sites/all/modules/aserv/aserv_media/images/banaan-gezond3.jpg"}
        
        # Convert fdate to human interpritable string
        fint = int(self.data['film_date'])
        self.fdate = dt.utcfromtimestamp(fint).strftime('%d %B %Y')
        
        # Convert pdate to human interpritable string
        pint = int(self.data['published_date'])
        self.pdate = dt.utcfromtimestamp(pint).strftime('%d %B %Y')
        
        # Get related talks if needed
        if get_related:
            self.related = []
            n = 3
            for r in ast.literal_eval(self.data['related_talks']):
                n -= 1
                if n < 1:
                    break
                try:
                    for t in data:
                        if t['name'] == f"{r['speaker']}: {r['title']}":
                            self.related.append(TedTalk(t['_id']))
                            break
                except IndexError:
                    continue
            print(self.related)
    
    def res_el(self):
        return(f"""
<div class="res">
    <div class="title"><a href="talk/{self.data['_id']}">{self.name}</a></div>
    <div class="info">
        by: <span class="speaker">{self.data['main_speaker']}</span>
        on:<span class="date">{self.fdate}</span>
        <span class="desc">{self.data['description']}</span>
    </div>
</div>
        """)