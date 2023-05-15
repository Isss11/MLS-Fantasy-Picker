NUM_PLAYERS = 15

# performs algorithm to choose players, based on their predicted scores created in the pointsPredictor
class Picker:
    def __init__(self, goalkeepers, defenders, midfielders, forwards) -> None:
        self.budget = 100
        self.positionAllocations = (2, 5, 5, 3) # picks 4-4-2 formation with 1 sub each
        # position budgets will be used as the budget allocated in the Knapsack problem selection
        self.positionBudgets = (self.budget * self.positionAllocations[0]/ NUM_PLAYERS,self.budget * self.positionAllocations[1] / NUM_PLAYERS,
                                self.budget * self.positionAllocations[2]/ NUM_PLAYERS, self.budget * self.positionAllocations[3]/ NUM_PLAYERS)
        
        print(self.positionBudgets)
        
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
        goalkeepersChosen = [] # really should just be one, just using an array for consistency
        defendersChosen = []
        midfieldersChosen = []
        forwardsChosen = []
        
        # greedy algorithm to pick players
        # initial allocations -- starts off with highest predicted socres
        for i in range(self.positionAllocations[0]):
            goalkeepersChosen.append(i)
            
        for i in range(self.positionAllocations[1]):
            defendersChosen.append(i)
            
        for i in range(self.positionAllocations[2]):
            midfieldersChosen.append(i)
            
        for i in range(self.positionAllocations[3]):
            forwardsChosen.append(i)  
            
        print(str(self.checkTeamCost(goalkeepersChosen, defendersChosen, midfieldersChosen, forwardsChosen)))
            
        return goalkeepersChosen, defendersChosen, midfieldersChosen, forwardsChosen
            
    # checks team cost so that we can see if it is over 100 million
    def checkTeamCost(self, goalkeepersChosen, defendersChosen, midfieldersChosen, forwardsChosen):
        goalkeepersCost = 0
        defendersCost = 0
        midfieldersCost = 0
        forwardsCost = 0
        
        print(self.goalkeepers)
        
        for i in goalkeepersChosen:
            print((self.goalkeepers.iloc[i])['player_name'])
            goalkeepersCost += (self.goalkeepers.iloc[i])['player_price']
            
        for i in defendersChosen:
            defendersCost += (self.defenders.iloc[i])['player_price']
            
        for i in midfieldersChosen:
            midfieldersCost += (self.midfielders.iloc[i])['player_price']
            
        for i in forwardsChosen:
            forwardsCost += (self.forwards.iloc[i])['player_price']
            
        print(goalkeepersCost, defendersCost, midfieldersCost, forwardsCost)
            
        totalCost = goalkeepersCost + defendersCost + midfieldersCost + forwardsCost
        
        return totalCost
