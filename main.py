from bs4 import BeautifulSoup
import re
import pprint
import pandas as pd
import numpy as np
import requests_html


session = requests_html.HTMLSession()
asession = requests_html.AsyncHTMLSession()

class Year2012():
    """
        Returns a dataframe for different rounds in 2012 ladder.
    """
    def __init__(self):
        self.data = {
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

    def webscrape(self, url):
        """
        Does preliminary webscrapping.
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


    def clear_data(self):
        """
        Clears all data so can be used again. 
        Called at the end of each function.
        """
        for key in self.data:
            self.data[key].clear()


    def round1(self):
        url = 'https://www.afl.com.au/ladder?Competition=1&Season=2&Round=5'
        ladder = self.webscrape(url)

        count = 0
        # Puts the information into the dict
        for i in range(13, len(ladder)):
            if count == 0:
                self.data['Position'].append(ladder[i])

            elif count == 1:
                self.data['Club'].append(ladder[i])

            elif count == 2:
                self.data['P'].append(ladder[i])
            
            elif count == 3:
                self.data['WR'].append(ladder[i])

            elif count == 4:
                self.data['Pts'].append(ladder[i])

            elif count == 5:
                self.data['%'].append(ladder[i])

            elif count == 6:
                self.data['W'].append(ladder[i])

            elif count == 7:
                self.data['L'].append(ladder[i])

            elif count == 8:
                self.data['D'].append(ladder[i])
            
            elif count == 9:
                self.data['PF'].append(ladder[i])

            elif count == 10:
                self.data['PA'].append(ladder[i])

            elif count == 11:
                self.data['Form'].append(ladder[i])


            if count == 14:
                count = -1

            count += 1
        
        df = pd.DataFrame(data=self.data)
        self.clear_data()
        print(df)
        return df
    

    def round2(self):
        url = "https://www.afl.com.au/ladder?Competition=1&Season=2&Round=6"
        ladder = self.webscrape(url)

        # print(ladder)
        for idx, el in enumerate(ladder):
            if idx % 13 == 0 :
                self.data['Position'].append(el)

        print(self.data)
        

year_2012 = Year2012()
year_2012.round1()
# year_2012.round2()

