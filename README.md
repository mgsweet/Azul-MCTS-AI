# MCTS based AZUL AI Agent
🎲 An AI agent that using Monte Carlo Tree Search to master the tile-laying game of Azul.

## Description
This repository contains a framework to support developing autonomous agents for the boardgame AZUL, published by Plan B Games. The game frame is forked from [Michelle Blom](https://github.com/michelleblom)'s repository, and GUI is developed by [Guang Hu](https://github.com/guanghuhappysf128) and  [Ruihan Zhang](https://github.com/zhangrh93). The AI agents are developed by [Aaron Yau](https://github.com/mgsweet), [Alan Ung](https://github.com/alanung) and [Aoqi Zuo](https://github.com/aoqiz). The code is in Python 3. This framework is able to run AZUL with two agents in a 1v1 game, and GUI will allow user to navigate through recorded game states. In addition, a replay can be saved and played for debug purpose.

Some information about the game:
- https://en.wikipedia.org/wiki/Azul_(board_game)
- https://boardgamegeek.com/boardgame/230802/azul
- https://www.planbgames.com/en/news/azul-c16.html
- https://github.com/michelleblom/AZUL


## Our Best Agent

We ranked **6th** in the last tournament and **2nd** in the final playoff. Our **total score in the tournament is the best**. However, our win rate is the worst in the first eight. In the final playoff, **we beat *404Error* (who ranked first in the final tournament).** 

### final_competition-05-Jun-2020-04-40-18

| Position | Team               | Win | Tie | Lost | TotalGame | TotalScore | FAILED | FinalScore |
|----------|--------------------|-----|-----|------|-----------|------------|--------|------------|
| 1        | 404Error           | 240 | 1   | 27   | 268       | 14755      | 0      | 26775      |
| 2        | AlphaAzul          | 230 | 4   | 34   | 268       | 14011      | 0      | 25591      |
| 3        | Amazing_Azul       | 192 | 3   | 73   | 268       | 14703      | 0      | 24363      |
| 4        | StaffTeamEasy      | 201 | 3   | 64   | 268       | 14163      | 0      | 24273      |
| 5        | thisisgroup1       | 180 | 4   | 84   | 268       | 14692      | 0      | 23772      |
| 6        | **Diamond_Three**  | 156 | 8   | 104  | 268       | **15466**  | 0      | 23426      |
| 7        | UnionOfThreeCities | 212 | 6   | 50   | 268       | 12662      | 0      | 23382      |
| 8        | AutoChess_Queen    | 203 | 7   | 58   | 268       | 13055      | 0      | 23345      |

## Demo Link
We also provide a demo for the project. which can be find here:

https://www.youtube.com/watch?v=4tPvgutIbvI

## Getting Started

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

### How to run our agent

To run our best agent and the naive player:

```
python runner.py -r Diamond_Three.myPlayer -b  naive_player

```
We also provide some other agents, you can find them in `players/Diamond_Three/`.

### How to run the original game provided by the teaching team?

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

## More Details

Check our assignment report for more details: [report](doc/report.pdf)


## Future Work
We very much welcome your pull request if you improve our agent. The following ideas are some aspect we think can improve the result our agent.

- Use some heuristic functions like the one here https://cmath-school.com/blog/azul-ai to do pruning or make a more accurate future reward function.
- We leave many `TODO` in our code, where we think can be improved in the future.
- Actually, you can also reuse the subtree generated by the previous round and continue update the subtree to gain a better result. We didn't implement that because we are not fully understood the algorithm when implementing it.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors of the AI Agents in this repo

* [**Aaron Yau**](https://github.com/mgsweet)  
* [**Alan Ung**](https://github.com/alanung)
* [**Aoqi Zuo**](https://github.com/aoqiz) 
