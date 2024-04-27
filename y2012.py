import re
import pandas as pd
import numpy as np
import requests_html

session = requests_html.HTMLSession()
asession = requests_html.AsyncHTMLSession()

ladderURL = "https://www.afl.com.au/ladder?Competition=1&Season=52&Round=781"
fixtureURL = "https://www.afl.com.au/fixture?Competition=1&Season=52&Round=930"
playerMatchStatsURL = "https://www.afl.com.au/afl/matches/233#player-stats"

class GetLadder():
    """
    Gets info of ladder position for particular year and round
    """
    def __init__(self, ladderURL):
        self.ladderURL = ladderURL

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
            }
        
    def clear_ladder(self):
        """
        Clears all data so can be used again. 
        Called at the end of each function.
        """
        for key in self.dataLadder:
            self.dataLadder[key].clear()

    def ladder(self):
        # Fetch the webpage
        response = session.get(self.ladderURL)

        # Render JavaScript
        response.html.render()

        # Scrape the content
        content = response.html.find('.stats-table__table')

        for i in content:
            ladders = i.text

        # Get rid of all the n\ and put it into a dataframe
        ladder = re.sub("\n", "|", ladders).split('|')

        # Get rid of the specific words and split 'PosClub' into 'Pos' and 'Club'
        stopWords = ['Top 8', '-', 'Form', 'Latest', 'Up Next']
        ladder = [word for word in ladder if word not in stopWords]
        ladder[1:1] = 'Pos', 'Club'
        ladder.pop(0)

        # Puts the information into the dict
        for idx, el in enumerate(ladder):
            if idx > 0 and idx % 11 == 0:
                self.dataLadder['Position'].append(el)

            elif idx > 1 and idx % 11 == 1:
                self.dataLadder['Club'].append(el)

            elif idx > 2 and idx % 11 == 2:
                self.dataLadder['P'].append(el)
            
            elif idx > 3 and idx % 11 == 3:
                self.dataLadder['WR'].append(el)

            elif idx > 4 and idx % 11 == 4:
                self.dataLadder['Pts'].append(el)

            elif idx > 5 and idx % 11 == 5:
                self.dataLadder['%'].append(el)

            elif idx > 6 and idx % 11  == 6:
                self.dataLadder['W'].append(el)

            elif idx > 7 and idx % 11  == 7:
                self.dataLadder['L'].append(el)

            elif idx > 8 and idx % 11  == 8:
                self.dataLadder['D'].append(el)
            
            elif idx > 9 and idx % 11  == 9:
                self.dataLadder['PF'].append(el)

            elif idx > 10 and idx % 11  == 10:
                self.dataLadder['PA'].append(el)
   
        df = pd.DataFrame(data=self.dataLadder)
        self.clear_ladder()
        print(df)
        return df


class GetFixture():
    """
    Gets the fixture for particular year and round
    """
    def __init__(self, fixtureURL):
        self.fixtureURL = fixtureURL
        
        self.dataFixture = {
            'Date': [],
            'T1': [],
            'T2': [],
            'T1Score': [],
            'T2Score': [],
            'Venue': []
        }

    def fixture(self):
        """
        Shows information on which team played, respective scores and location
        """
        # Fetch the webpage
        response = session.get(self.fixtureURL)

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
        

class GetPlayeMatchStats():
    """
    Get player stat for particular game
    """
    def __init__(self, url) -> None:
        self.url = url
    
    def playerMatchStat(self):
        # Fetch the webpage
        response = session.get(self.url)

        # Render JavaScript
        response.html.render()

        # Scrape the content, only want "wrapper" class
        content = response.html.find('.stats-table__table')

        for i in content:
            pms = i.text

        pms = re.sub("\n", "|", pms).split('|')
        print(pms)

# fix = GetFixture(fixtureURL)
# lad = GetLadder(ladderURL)
pms = GetPlayeMatchStats(playerMatchStatsURL)

# fix.fixture()
# lad.ladder()
pms.playerMatchStat()
