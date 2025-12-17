import numpy as np
from mcts import MCTS
from uttt import UTTT
from game_runner2 import GameRunner2
from gomoku import Gomoku
 
if __name__=="__main__":
    AI = MCTS(search_time_limit=30, search_steps_limit=np.inf, vanilla=True)
    # game_runner = GameRunner2(Gomoku,None,AI,0,1,None)
    game_runner = GameRunner2(UTTT,AI,None,0,1,None)
    outcome,game_info = game_runner.run()
