import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/')
def webScrape():
        keyWords = open("keywords.txt").read().splitlines() 
        
        df = pd.DataFrame(columns = ['Keyword','Title','URL'])
        
        #AR15.com
        data = requests.get('https://urldefense.com/v3/__https://www.ar15.com/forums/Equipment-Exchange/AR15-Parts-New-Lower-Receiver/125/__;!!Bbg-OcCDlOs!T6SPqMDtsVY4Vk39ZzosABP95RtKZ_FkgWA9Fczc7IfsrSGT315NdhcvHQtW1JwZRjyAkA$ ')
        soup = BeautifulSoup(data.text, 'html.parser')
        links = soup.find_all('a')
        ar15Site = 'https://www.ar15.com'
        
        for x in keyWords:
                for l in links:
                        href = l.get('href')
                        title = l.get('title')
                        if x in href and title != None:
                                df.loc[df.shape[0]+1, 'URL'] = ar15Site+href
                                df.loc[df.shape[0], 'Title'] = str(title)
                                df.loc[df.shape[0], 'Keyword'] = str(x)
        
        pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
        
        html_string = '''
                <html>
                <head><title>HTML Pandas Dataframe with CSS</title></head><link rel="stylesheet" type="text/css" href="/static/df_style.css?q=
                '''+str(random.randint(0,100))+'''"/><body> {table}</body></html>.'''
        
        with open('templates/table.html', 'w') as f:
                f.write(html_string.format(table=df.to_html(classes='mystyle', justify = 'center', render_links = True)))
        
        return render_template('table.html')

app.run('0.0.0.0',8080)