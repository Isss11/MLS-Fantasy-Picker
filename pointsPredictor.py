import pandas as pd
from dataImporter import DataImporter
from picker import Picker

# takes all the players that were parsed by the dataImporter class and creates a simple set of predictions for all positions
class PointsPredictor:
    def __init__(self) -> None:
        self.forwardsPredictions = pd.DataFrame()
        self.midfieldersPredictions = pd.DataFrame()
        self.defendersPredictions = pd.DataFrame()
        self.goalkeepersPredictions = pd.DataFrame()
        
    # takes the players and separates them by position (returns forwards, midfielders, defenders, and goalkeepers dictionary arrays)
    def separateByPosition(self, players):
        forwards = []
        midfielders = []
        defenders = []
        goalkeepers = []
        
        for i in players:
            if i.generalFantasyAttrDict['player_pos'] == "Forward":
                forwards.append(i)
            elif i.generalFantasyAttrDict['player_pos'] == "Midfielder":
                midfielders.append(i)
            elif i.generalFantasyAttrDict['player_pos'] == "Defender":
                defenders.append(i)
            else:
                goalkeepers.append(i)
                
        return forwards, midfielders, defenders, goalkeepers
                
    
    # creates predictions and stores them all as dataframes
    # FIXME -- right now the algorithm is very basic, it merely uses the average fantasy points as the predictor for each
    def predict(self, players):
        # separating players dictionary by position
        forwards, midfielders, defenders, goalkeepers = self.separateByPosition(players)
        
        self.forwardsPredictions = self.createPredictionTable(forwards)
        self.midfieldersPredictions = self.createPredictionTable(midfielders)
        self.defendersPredictions = self.createPredictionTable(defenders)
        self.goalkeepersPredictions = self.createPredictionTable(goalkeepers)
        
    # takes a subset of the original players array (e.g. just the midfielders, and creates the DF)
    def createPredictionTable(self, playerSubset):
        playerNames = []
        predictedScores = []
        playerPrices = []
        dollarsPerPoint = []
        playersSubsetDF = pd.DataFrame()
        
        # now iterates through and appends data to the arrays to create the data frame later
        for i in range(len(playerSubset)):
            playerNames.append(playerSubset[i].generalFantasyAttrDict['player_name'])
            predictedScores.append(playerSubset[i].generalFantasyAttrDict['avg_fantasy_pts'])
            playerPrices.append(playerSubset[i].generalFantasyAttrDict['player_price'])
            dollarsPerPoint.append(playerSubset[i].generalFantasyAttrDict['$/point'])
        
        playersSubsetDF["player_name"] = playerNames
        playersSubsetDF["player_price"] = playerPrices
        playersSubsetDF["$/point"] = dollarsPerPoint
        playersSubsetDF["predicted_score"] = predictedScores
        
        return playersSubsetDF
        
if __name__ == "__main__":
    mlsData = DataImporter()
    
    mlsData.loadData("2023-05-14")
    
    predictor = PointsPredictor()
    predictor.predict(mlsData.playerDataSets)
    
    # now creating the picker
    picker = Picker(predictor.goalkeepersPredictions, predictor.defendersPredictions,
                    predictor.midfieldersPredictions, predictor.forwardsPredictions)
    
    print(predictor.goalkeepersPredictions)
    print(predictor.defendersPredictions)
    print(predictor.midfieldersPredictions)
    print(predictor.forwardsPredictions)
    
    picker.pickTeam()
    
    print("Goalkeepers:", picker.goalkeepersChosen)
    print("Defenders:", picker.defendersChosen)
    print("Midfielders:", picker.midfieldersChosen)
    print("Forwards", picker.forwardsChosen)
    
    # printing out actual players
    print("\nCHOSEN PLAYERS\n**************")
    print("Goalkeepers")
    for i in range(2):
        print(predictor.goalkeepersPredictions.iloc[picker.goalkeepersChosen[i]])
        
    print("Defenders")
    for i in range(5):
        print(predictor.defendersPredictions.iloc[picker.defendersChosen[i]])
        
    print("Midfielders")
    for i in range(5):
        print(predictor.midfieldersPredictions.iloc[picker.midfieldersChosen[i]])
        
    print("Forwards")
    for i in range(3):
        print(predictor.forwardsPredictions.iloc[picker.forwardsChosen[i]])