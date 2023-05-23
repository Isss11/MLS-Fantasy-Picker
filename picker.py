NUM_PLAYERS = 15

# performs algorithm to choose players, based on their predicted scores created in the pointsPredictor
class Picker:
    def __init__(self, goalkeepers, defenders, midfielders, forwards) -> None:
        self.budget = 100000000
        self.positionAllocations = (2, 5, 5, 3) # picks 4-4-2 formation with 1 sub each
        
        # storing data frames of each position
        self.goalkeepers = goalkeepers
        self.defenders = defenders
        self.midfielders = midfielders
        self.forwards = forwards
        
        self.sortLists()
        
    # sorts list by predicted score (won't make an effect until I calculate predicted score differently then initial setup)
    def sortLists(self):
        self.goalkeepers = self.goalkeepers.sort_values(by='predicted_score', ascending=False)
        self.defenders = self.defenders.sort_values(by='predicted_score', ascending=False)
        self.midfielders = self.midfielders.sort_values(by='predicted_score', ascending=False)
        self.forwards = self.forwards.sort_values(by='predicted_score', ascending=False)
        
    # deploys greedy algorithm to get one of the best (not necessarily the absolute best) predicted subset of players
    def pickTeam(self):
        budgetSpent = 0
        
        gkInd = defInd = midInd = forInd = 0
        self.goalkeepersChosen = [] # really should just be one, just using an array for consistency
        self.defendersChosen = []
        self.midfieldersChosen = []
        self.forwardsChosen = []
        
        # greedy algorithm to pick players
        # initial allocations -- starts off with highest predicted socres
        for i in range(self.positionAllocations[0]):
            self.goalkeepersChosen.append(i)
            
        for i in range(self.positionAllocations[1]):
            self.defendersChosen.append(i)
            
        for i in range(self.positionAllocations[2]):
            self.midfieldersChosen.append(i)
            
        for i in range(self.positionAllocations[3]):
            self.forwardsChosen.append(i)  
            
        totalCost = self.getTeamCosts()
        
        # if best team is over the budget, perform the following greedy algorithm until it is below the budget
        # FIXME will need to account for times when there are over 3 playerson one team
        while (totalCost > self.budget):
            # will find highest cost player and move them
            highestCostPosition = 0 # setting to goalkeeper by default
            highestCostPlayer = 0
            costofHighestPlayer = (self.goalkeepers.iloc[self.goalkeepersChosen[0]])['player_price']
            
            for i in range (len(self.goalkeepersChosen)):
                if (self.goalkeepers.iloc[self.goalkeepersChosen[i]])['player_price'] > costofHighestPlayer:
                    costofHighestPlayer = (self.goalkeepers.iloc[self.goalkeepersChosen[i]])['player_price']
                    highestCostPlayer = i
                    
            for i in range (len(self.defendersChosen)):
                if (self.defenders.iloc[self.defendersChosen[i]])['player_price'] > costofHighestPlayer:
                    costofHighestPlayer = (self.defenders.iloc[self.defendersChosen[i]])['player_price']
                    highestCostPosition = 1
                    highestCostPlayer = i
                    
            for i in range (len(self.midfieldersChosen)):
                if (self.midfielders.iloc[self.midfieldersChosen[i]])['player_price'] > costofHighestPlayer:
                    costofHighestPlayer = (self.midfielders.iloc[self.midfieldersChosen[i]])['player_price']
                    highestCostPosition = 2
                    highestCostPlayer = i
                    
            for i in range (len(self.forwardsChosen)):
                if (self.forwards.iloc[self.forwardsChosen[i]])['player_price'] > costofHighestPlayer:
                    costofHighestPlayer = (self.forwards.iloc[self.forwardsChosen[i]])['player_price']
                    highestCostPosition = 3
                    highestCostPlayer = i
                    
            # after picking highest player in highest position, we should move the player to the one after the latest index in that position
            if highestCostPosition == 0:
                listToChange = self.goalkeepersChosen
            elif highestCostPosition == 1:
                listToChange = self.defendersChosen
            elif highestCostPosition == 2:
                listToChange = self.midfieldersChosen
            elif highestCostPosition == 3:
                listToChange = self.forwardsChosen
            
            # finding highest index so that we can increment after that (to avoid picking the same player)
            highestIndexInPosition = listToChange[0]
            
            for i in listToChange:
                if i > highestIndexInPosition:
                    highestIndexInPosition = i
                    
            # now incrementing highest cost player to the next index (after corresponding higestIndexInPosition in respective position)
            listToChange[highestCostPlayer] = highestIndexInPosition + 1
                                
            # checking cost again to see if this complies with the rules
            totalCost = self.getTeamCosts()
            
            # now need to check to make sure there are not over 3 players from one team (have to check for multiple cases as well)
            teamCounts, teamPlayers = self.getTeamPlayers()
            self.adjustForMaxTeamCount(1, teamCounts, teamPlayers)
            
            print("Current cost is ", totalCost)
            
        print("Total cost is ", totalCost)
            
    # adjusts teams when they have over the maximum amount of players from a single team
    # takes a maximum amount of players, and two dictionaries holding the counts and the team players, respectively
    def adjustForMaxTeamCount(self, maxPlayers, teamCounts, teamPlayers):
        teamsToAdjust = dict()
        
        # for all teams that have more players then maxPlayers, put them into this dictionary so that we can deal with them
        for i in teamCounts:
            if teamCounts[i] > maxPlayers:
                teamsToAdjust.update({i : teamPlayers[i]}) 
                
        # we will pick the teams with lowest indices (lowest prediced scores, and update those so that the maximum player
        # condition is satisfied)
        for i in teamsToAdjust:
            pass    
            
    # checks team cost so that we can see if it is over 100 million
    def getTeamCosts(self):
        goalkeepersCost = 0
        defendersCost = 0
        midfieldersCost = 0
        forwardsCost = 0
        
        for i in self.goalkeepersChosen:
            goalkeepersCost += (self.goalkeepers.iloc[i])['player_price']
            
        for i in self.defendersChosen:
            defendersCost += (self.defenders.iloc[i])['player_price']
            
        for i in self.midfieldersChosen:
            midfieldersCost += (self.midfielders.iloc[i])['player_price']
            
        for i in self.forwardsChosen:
            forwardsCost += (self.forwards.iloc[i])['player_price']
            
        totalCost = goalkeepersCost + defendersCost + midfieldersCost + forwardsCost
        
        return totalCost
    
    # creates and returns two dictionaries with the players counts on each team and the player indices, according to the sorted predictions
    # arrays
    def getTeamPlayers(self):
        teamCountsDictionary = dict()
        teamPlayersDictionary = dict()
        
        for i in self.goalkeepersChosen:
            try:
                currentTeamCount = teamCountsDictionary[(self.goalkeepers.iloc[i])['player_team']]
            # if team is not in dictionary, team count is zero
            except KeyError:
                currentTeamCount = 0
                # mapping a list to the players dictionary, will append corresponding player indices to it
                teamPlayersDictionary.update({(self.goalkeepers.iloc[i])['player_team'] : []})
                
            teamCountsDictionary.update({(self.goalkeepers.iloc[i])['player_team'] : currentTeamCount + 1})
            teamPlayersDictionary[(self.goalkeepers.iloc[i])['player_team']].append(i)

        
        for i in self.defendersChosen:
            try:
                currentTeamCount = teamCountsDictionary[(self.defenders.iloc[i])['player_team']]
            except KeyError:
                currentTeamCount = 0
                teamPlayersDictionary.update({(self.defenders.iloc[i])['player_team'] : []})

                
            teamCountsDictionary.update({(self.defenders.iloc[i])['player_team'] : currentTeamCount + 1})
            teamPlayersDictionary[(self.defenders.iloc[i])['player_team']].append(i)

         
        for i in self.midfieldersChosen:
            try:
                currentTeamCount = teamCountsDictionary[(self.midfielders.iloc[i])['player_team']]
            except KeyError:
                currentTeamCount = 0
                teamPlayersDictionary.update({(self.midfielders.iloc[i])['player_team'] : []})
                
            teamCountsDictionary.update({(self.midfielders.iloc[i])['player_team'] : currentTeamCount + 1})
            teamPlayersDictionary[(self.midfielders.iloc[i])['player_team']].append(i)

              
        for i in self.forwardsChosen:
            try:
                currentTeamCount = teamCountsDictionary[(self.forwards.iloc[i])['player_team']]
            except KeyError:
                currentTeamCount = 0
                teamPlayersDictionary.update({(self.forwards.iloc[i])['player_team'] : []})

            teamCountsDictionary.update({(self.forwards.iloc[i])['player_team'] : currentTeamCount + 1})    
            teamPlayersDictionary[(self.forwards.iloc[i])['player_team']].append(i)
        
        return teamCountsDictionary, teamPlayersDictionary
    
    # gets 4 values (really just for the 4 multiplier values and returns 0, 1, 2, or 3 depending on what is the largest)
    def getMaxVal(self, val1, val2, val3, val4):
        maxInd = 0
        maxVal = val1
        
        if val2 > maxVal:
            maxVal = val2
            maxInd = 1
            
        if val3 > maxVal: 
            maxVal = val3
            maxInd = 2
            
        if val4 > maxVal:
            maxVal = val4
            maxInd = 3
            
        return maxInd