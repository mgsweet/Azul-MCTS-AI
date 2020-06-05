# MCTS based AZUL AI Agent

An AI agent that using Monte Carlo Tree Search to master the tile-laying game of Azul.

## Our Best Agent

We ranked **6th** in the last tournament and **2nd** in the final playoffs. Our win rate in the first eight is the worst. However, our game score is high. In the final playoff, **we beat the player who ranked first in the final tournament.** 



## Usage

To run our best agent and the naive player:

```
python runner.py -r Diamond_Three.myPlayer -b  naive_player
```

We also provide some other agent, you can find them in `players/Diamond_Three/`.



## More Details

Check our assignment report for more details: [report](doc/report.pdf)



## Future Work

- Use some heuristic functions like the one here https://cmath-school.com/blog/azul-ai to do pruning or make a more accurate future reward function.
- We leave many `TODO` in our code, where we think can be improved in the future.



---

## Assignment Specification

This repository contains a framework to support developing autonomous agents for the boardgame AZUL, published by Plan B Games. The game frame is forked from [Michelle Blom](https://github.com/michelleblom)'s repository, and GUI is developed by [Guang Hu](https://github.com/guanghuhappysf128) and  [Ruihan Zhang](https://github.com/zhangrh93). The code is in Python 3.

Students should be able to use this frame and develop their own agent under the directory players. This framework is able to run AZUL with two agents in a 1v1 game, and GUI will allow user to navigate through recorded game states. In addition, a replay can be saved and played for debug purpose.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html
- https://github.com/michelleblom/AZUL

### Setting up the environment

Python 3 is required, and library tkinter should be installed along with python 3.

The code uses three library that required to be installed: ```numpy```,```func_timeout```,```tqdm```, which can be done with the following command:
```bash
pip install numpy tqdm func_timeout
```
If have both python 2 and python 3 installed, you might need to use following command:
```bash
pip3 install numpy tqdm func_timeout
```

### How to run it?

The code example can be run with command:
```bash
python runner.py
```
, which will run the game with two default players (naive_player). 

A standard example to run the code would be:
```bash
python runner.py -r naive_player -b random_player -s 
```

Other command line option can be viewed with argument: ```-h``` or ```--help```

When a game ends, the GUI will pause to allow user selecting each states on listbox (right side of the window), and it will change accordingly. And replay file will be generated once the GUI window is closed.

***For Debug purpose:***
***Please use the Example.ipynb to start***

**Extra function**
- timeout limit
- timeout warning and fail
- replay system
- GUI displayer (allow switch)
- delay time setting

**class and parameters**

*AdvancedRunner*

Runner with timelimit, timeout warnings, displayer, replay system. It returns a replay file.

*ReplayRunner*

Use replay file to unfold a replay

*GUIGameDisplayer*

GUI game displayer, you coud click items in the list box and use arrow keys to select move.
