# Fighting game prediction bot
This project is a prototype for an ai fighting game opponent that has to predict the game state and best action some arbitrary number of frames into the future, in order to better represent a human player with human reaction speeds.

# Running the game
To run the game simply clone the repository, extract it and run:
```
$ python text_fighter.py
```
From here enter the name of player one and player two, this is also how you select the ai opponents.
To have an ai opponent play the game enter the name of the bot's python file. For example, if you wanted to see the kick bot fight the mcts bot respond to the prompt like this:
```
Who is player 1?
mcts_bot
Who is player 2?
kick_bot
```
To play the game maually just enter any other name into the prompt like so:
```
Who is player 1?
bob
Who is player 2?
alice
```
If you would like to graph a large amount of trial runs between bots you will need the matplotlib python module installed.
Then go into the Graph.py and edit the line that calls text fighter using the script_input method to use any two bots you would like to compare.
```
h = text_fighter.script_input('mcts_bot', 'kick_bot')
```

# The problem that needs solving
Fighting game single player modes have consistently been important to a fighting game's sales, and underwhelming in their execution. There are many reasons this may be the case, but to me the main reason is that the game is fundementally different against a human as compared to a computer. The developers would need to design for two different experiences and they will ultimately end up comprimizing one of the two. If, however, we could make the computer play in a more human like manner, then the player experience would be quite similar solo as it is with other players. 

# Previous approaches
In my search to see how others had developed their ai I came across a decent amount of information about street fighter 2. It looks like the game was reverse engineered to see exactly how everything, but most notably to us the ai, works. In sf2 the ai is made up of batch scripts that run given certain criteria. The main issue with this is that every attack pattern must be hard coded into the game and every response to an opponent must as well. It's clear that methods similar to this are still the norm as evidenced by forum posts like this: https://gamefaqs.gamespot.com/boards/927089-soulcalibur-iii/45995379

The only way to solve this is to allow the opponent to be more flexible, especially in it's defense, but this leads to it's own set of problems, like instantly blocking a move that no human could have reacted to. Tekken 5 ai is a good example of this, here is a guide for how people worked around beating the ai, not being able to rely on the usual 50/50 mixups but instead on glitches in the programming of the ai. https://gamefaqs.gamespot.com/ps2/920588-tekken-5/faqs/36871 (see section 7)

# My approach
I look to combine the flexibility of monte carlo tree search used in programs like alphago with a rolling buffer system to simulate human reaction speeds. I have modified the monte carlo tree search quite a bit from it's origional usage by adding the concept of risk based analysis. This modification can be seen in the diagram below but to describe it succinctly I would say that it calculates the likelyhood of taking damage and dealing damage separately, and allows for a paramater to be passed to it telling it to be more or less risk tolerant.

# Risk reward model
![diagram](https://raw.githubusercontent.com/metalgaiden/FG_Prediction_Bot/master/FG_Bot_Diagram.png)

In order to accomplish this Behaviour I used mcts in combination with a unique risk reward model in order to have the ai make the correct choice in any given situation given imperfect predicted data. The data on each player’s predicted responses is stored in a json file which is generated any time a new player fights the AI.  

The AI will fill a buffer with moves to do two or more turns ahead. In order to figure out what to do that far into the future the AI will traverse a tree of possible actions picking only the node with the most likelihood of happening. 

This is shown by lines 1 and 2 on the diagram. Once here the Program will look at the possible children nodes and classify them into three groups: neutral (3 on the diagram) positive (a node that damages the opponent 4 on the diagram) and negative (a node where the bot receives damage 5 on the diagram). 

For the neutral nodes a rollout is performed on that node to a specified maximum depth the amount of wins recorded are stored as the node’s win rate and the amount of losses are stored as that node’s risk factor, each divided by the total number of rollouts performed. For positive nodes their reward factor is already 1 but their risk is calculated by performing a rollout on the parent node instead (line 6). The negative nodes are ignored unless there are no other actions remaining. 

The risk and reward factors are then passed into a function to evaluate the best option, for our program we used the formula: (prob + reward) + c * (1-risk) where c is a constant used to change the risk propensity of the bot as needed. In the diagram below because the probability is somewhat low (45%) so the program will look more at risk than it does at reward. As a result the program would likely pick option 3.

# Limitations
The current version uses a command line interface and a turn based approximation of a fighting game interation. The next obvious step would be to place the ai into a real time game with an n frames rolling buffer that contatly made predictions and calculations. The biggest issue with this transition would be the inefficiency of making calculations in a continuous space. In a discrete game like chess you can calculate or even go you can calculate games as a finite number of simulations, but in a continuous space it becomes much harder. Even with all the discrete turn based fighter I have made, the data file for each ai fighter, stored in an xml file, is far too huge to be practical. It could work but would require a lot of training and would be very slow to figure out new strategies because the it would fail to see similar screen positions like positions that are one pixel off as the same. 
