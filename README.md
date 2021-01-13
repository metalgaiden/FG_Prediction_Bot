# FG_Prediction_Bot
A prototype for a predictive fighting game bot. 
It uses an mcts like algorithm to pick moves based on the opponent's most likely action.

The current version uses a command line interface to simulate a basic fighting game, though future versions may use a real time version.

A description of the mcts function from my writeup for class, see the diagram included for more information:

"In order to accomplish this Behaviour we use mcts in combination with a unique risk reward model in order to have the ai make the correct choice in any given situation given imperfect predicted data. The data on each player’s predicted responses is stored in a json file which is generated any time a new player fights the AI.  

The AI will fill a buffer with moves to do two or more turns ahead. In order to figure out what to do that far into the future the AI will traverse a tree of possible actions picking only the node with the most likelihood of happening. 

This is shown by lines 1 and 2 on the diagram. Once here the Program will look at the possible children nodes and classify them into three groups: neutral (3 on the diagram) positive (a node that damages the opponent 4 on the diagram) and negative (a node where the bot receives damage 5 on the diagram). 

For the neutral nodes a rollout is performed on that node to a specified maximum depth the amount of wins recorded are stored as the node’s win rate and the amount of losses are stored as that node’s risk factor, each divided by the total number of rollouts performed. For positive nodes their reward factor is already 1 but their risk is calculated by performing a rollout on the parent node instead (line 6). The negative nodes are ignored unless there are no other actions remaining. 

The risk and reward factors are then passed into a function to evaluate the best option, for our program we used the formula: (prob + reward) + c * (1-risk) where c is a constant used to change the risk propensity of the bot as needed. In the diagram below because the probability is somewhat low (45%) so the program will look more at risk than it does at reward. As a result the program would likely pick option 3."

![diagram](https://raw.githubusercontent.com/metalgaiden/FG_Prediction_Bot/master/FG_Bot_Diagram.png)
