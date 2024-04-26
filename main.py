from bs4 import BeautifulSoup
import re
import pprint
import pandas as pd
import numpy as np
import requests_html


session = requests_html.HTMLSession()
asession = requests_html.AsyncHTMLSession()

class Year2012():
    def webscrape(self, url):
        """
        Does preliminary webscrapping
        """
        # Fetch the webpage
        response = session.get(url)

        # Render JavaScript
        response.html.render()

        # Scrape the content
        content = response.html.find('.stats-table__table')

        for i in content:
            ladder = i.text

        # Get rid of all the n\ and put it into a dataframe
        ladder = re.sub("\n", "|", ladder).split('|')

        # Get rid of the word 'Top 8', to make arr make sense
        ladder.remove('Top 8')

        return ladder


    def round1(self):
        """
        Returns a dataframe for round 1 2012 ladder.
        """
        url = 'https://www.afl.com.au/ladder?Competition=1&Season=2&Round=5'
        ladder = self.webscrape(url)

        data ={
            'Position': [],
            'Club': [],
            'P': [],
            'WR': [],
            'Pts': [],
            '%': [],
            'W': [],
            'L': [],
            'D': [],
            'PF': [],
            'PA': [],
            'Form': [],
            'Latest': [],
            'Up Next': [],
            }

        count = 0
        # Puts the information into the dict
        for i in range(13, len(ladder)):
            if count == 0:
                data['Position'].append(ladder[i])

            elif count == 1:
                data['Club'].append(ladder[i])

            elif count == 2:
                data['P'].append(ladder[i])
            
            elif count == 3:
                data['WR'].append(ladder[i])

            elif count == 4:
                data['Pts'].append(ladder[i])

            elif count == 5:
                data['%'].append(ladder[i])

            elif count == 6:
                data['W'].append(ladder[i])

            elif count == 7:
                data['L'].append(ladder[i])

            elif count == 8:
                data['D'].append(ladder[i])
            
            elif count == 9:
                data['PF'].append(ladder[i])

            elif count == 10:
                data['PA'].append(ladder[i])

            elif count == 11:
                data['Form'].append(ladder[i])

            elif count == 12:
                data['Latest'].append(ladder[i])

            elif count == 13:
                data['Up Next'].append(ladder[i])
                
            if count == 14:
                count = -1

            count += 1
            
        df = pd.DataFrame(data=data)
        print(df)
        return df
    
    def round2():
        pass

year_2012 = Year2012()
year_2012.round1()

