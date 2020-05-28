import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/')
def webScrape():
        
        keywords = open('keywords.txt').read().splitlines()

        df = pd.DataFrame(columns=['Keyword', 'URL', 'Title', 'Info'])
        
        # New Lower AR15
        data = requests.get('https://www.ar15.com/forums/Equipment-Exchange/AR15-Parts-New-Lower-Receiver/125/')
        soup = BeautifulSoup(data.text, 'html.parser')
        links = soup.find_all('div', {'class':'large-6 medium-9 small-12 columns'})
        prefix = "https://www.ar15.com"

        for x in keywords:     
                x = x.upper()
                for l in links:
                        href = l.find_all('a')[1].get('href')
                        info = l.find_all('a')[1].get('title')
                        title = l.find_all('a')[1].getText()
                        if x in href.upper():
                                df = df.append(pd.DataFrame([[x, prefix+href, title, info]],columns=['Keyword', 'URL', 'Title', 'Info']))

        # M4 site parts 
        data = requests.get('https://www.m4carbine.net/forumdisplay.php?111-AR-Parts-amp-Furniture-(EE)')
        soup = BeautifulSoup(data.text, 'html.parser')
        links = soup.find_all('div', {'class':'threadinfo'})
        prefix = "https://www.m4carbine.net"
        
        for x in keywords:
                x = x.upper()   
                for l in links:
                        title = l.find('a',{'class':'title'}).getText()
                        info = l.get('title')
                        href = l.find('a',{'class':'title'}).get('href')
                        if x in href.upper():
                                df = df.append(pd.DataFrame([[x, prefix+href, title, info]],columns=['Keyword', 'URL', 'Title', 'Info']))

        # Export data to Excel
        pd.set_option('colheader_justify', 'center')
        
        html_string = '''
                <html>
                <head><title>HTML Pandas Dataframe with CSS</title></head><link rel="stylesheet" type="text/css" href="/static/df_style.css?q=
                '''+str(random.randint(0,100))+'''"/><body> {table}</body></html>.'''
        
        df = df.reset_index(drop = True)
        with open('templates/table.html', 'w') as f:
                f.write(html_string.format(table=df.to_html(classes='mystyle', justify = 'center', render_links = True)))
        
        return render_template('table.html')

app.run('0.0.0.0',8080)