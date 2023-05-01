import pandas as pd
from playerData import PlayerData

# self.dictLabels = ['player_name', 'player_team', 'player_pos', 'player_price', 'player_avail', 'games_played', 'avg_fantasy_pts', 
#                            'total_fantasy_pts', 'last_wk_fantasy_pts', '3_wk_avg', '5_wk_avg', 'high_score', 'low_score', 'owned_by', 
#                         #    '$/point', 'rd_9_rank', 'season_rank']

# a wrapper class to store DF of general data, and associated arrays used to create it
class GeneralData:
    def __init__(self) -> None:
        # a data frame that contains the fantasy player IDs of each player, along with other general stats (kept in a row)
        self.playerDataLabels = PlayerData().dictLabels
        
        self.playerIDs = []
        self.playerNames = []
        self.playerTeams = []
        self.playerPositions = []
        self.playerAvails = []
        self.playerGames = []
        self.averageFantasyPoints = []
        self.totalFantasyPoints = []
        self.lastWeekFantasyPoints = []
        self.threeWeekAverages = []
        self.fiveWeekAverages = []
        self.highScores = []
        self.lowScores = []
        self.ownedBy = []
        self.dollarsPerPoint = []
        self.roundRank = []
        self.seasonRank = []
        
        self.generalDataLists = [self.playerIDs, self.playerNames, self.playerTeams, self.playerPositions, self.playerAvails, self.playerGames, self.averageFantasyPoints, 
                                 self.totalFantasyPoints, self.lastWeekFantasyPoints, self.threeWeekAverages, self.fiveWeekAverages, self.highScores, 
                                 self.lowScores, self.ownedBy, self.dollarsPerPoint, self.roundRank, self.seasonRank]
        
    # appends data of row entry to all the lists
    def appendListEntry(self, id, dictionary):
        self.playerIDs.append(id)
        
        # now iterating through dictionary and appending values to corresponding arrays
        for i in range(1, len(self.playerDataLabels)):
            self.generalDataLists[i].append(dictionary[self.playerDataLabels[i]])
        
    # once all the data values have been appended, create the general DF
    def createDF(self):
        generalDF = pd.DataFrame()

        generalDF['playerIDs'] = self.playerIDs
        
        for i in range (1, len(self.generalDataLists)):
            
            generalDF[self.playerDataLabels[i - 1]] = self.generalDataLists[i]
            
        return generalDF
        