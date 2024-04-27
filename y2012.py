import re
import pandas as pd
import numpy as np
import requests_html

session = requests_html.HTMLSession()
asession = requests_html.AsyncHTMLSession()

class Round1():
    """
        Returns a dataframe for different rounds in 2012 ladder.
    """
    def __init__(self):
        self.dataLadder = {
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
            }
        
        self.dataFixture = {
            'Date': [],
            'T1': [],
            'T2': [],
            'T1Score': [],
            'T2Score': [],
            'Venue': []
        }

    def clear_data(self):
        """
        Clears all data so can be used again. 
        Called at the end of each function.
        """
        for key in self.dataLadder:
            self.dataLadder[key].clear()


    def ladder(self):
        url = 'https://www.afl.com.au/ladder?Competition=1&Season=2&Round=5'
        # Fetch the webpage
        response = session.get(url)

        # Render JavaScript
        response.html.render()

        # Scrape the content
        content = response.html.find('.stats-table__table')

        for i in content:
            ladders = i.text

        # Get rid of all the n\ and put it into a dataframe
        ladder = re.sub("\n", "|", ladders).split('|')

        # Get rid of the word 'Top 8', to make arr make sense
        ladder.remove('Top 8')
        print(ladder)

        # count = 0
        # # Puts the information into the dict
        # for i in range(13, len(ladder)):
        #     if count == 0:
        #         self.dataLadder['Position'].append(ladder[i])

        #     elif count == 1:
        #         self.dataLadder['Club'].append(ladder[i])

        #     elif count == 2:
        #         self.dataLadder['P'].append(ladder[i])
            
        #     elif count == 3:
        #         self.dataLadder['WR'].append(ladder[i])

        #     elif count == 4:
        #         self.dataLadder['Pts'].append(ladder[i])

        #     elif count == 5:
        #         self.dataLadder['%'].append(ladder[i])

        #     elif count == 6:
        #         self.dataLadder['W'].append(ladder[i])

        #     elif count == 7:
        #         self.dataLadder['L'].append(ladder[i])

        #     elif count == 8:
        #         self.dataLadder['D'].append(ladder[i])
            
        #     elif count == 9:
        #         self.dataLadder['PF'].append(ladder[i])

        #     elif count == 10:
        #         self.dataLadder['PA'].append(ladder[i])

        #     elif count == 11:
        #         self.dataLadder['Form'].append(ladder[i])


        #     if count == 14:
        #         count = -1

        #     count += 1
        
        # df = pd.DataFrame(data=self.dataLadder)
        # self.clear_data()
        # print(df)
        # return df


    def fixture(self):
        """
        Shows information on which team played, respective scores and location
        """
        url = 'https://www.afl.com.au/fixture?Competition=1&Season=2&Round=6'
        # Fetch the webpage
        response = session.get(url)

        # Render JavaScript
        response.html.render()

        # Scrape the content, only want "wrapper" class
        content = response.html.find('div.wrapper:not([class*=" "])')

        for i in content:
            fixture = i.text

        # Get rid of all the n\ and put it into a dataframe
        fixture = re.sub("\n", "|", fixture).split('|')

        # Get rid of Full Time, Highlights, Replays
        stopWords = ['FULL TIME', 'Highlights', 'Replays', 'Match Report']
        fixture = [word for word in fixture if word not in stopWords]

        # Add missing dates if they are missing
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i in range(0, len(fixture), 8):
            prevDay = fixture[i - 8]

            # if the first word of i is not in days, insert prevDay
            if fixture[i].split()[0] not in days:
                fixture.insert(i, prevDay)
        
        # Convert to df
        for idx, word in enumerate(fixture):
            if idx % 8 == 0:
                self.dataFixture['Date'].append(word)

            elif idx % 8 == 2:
                self.dataFixture['T1'].append(word)

            elif idx % 8 == 3:
                self.dataFixture['T1Score'].append(word)

            elif idx % 8 == 4:
                self.dataFixture['T2Score'].append(word)

            elif idx % 8 == 5:
                self.dataFixture['T2'].append(word)

            elif idx % 8 == 7:
                self.dataFixture['Venue'].append(word)

        df = pd.DataFrame(data=self.dataFixture)
        print(df)
        return df
        

        

        

r1 = Round1()
r1.ladder()

