import numpy as np
from mcts import State
from numba import jit
from numba import int8

__version__ = "1.0.1"
__author__ = "Przemysław Klęsk"
__email__ = "pklesk@zut.edu.pl" 

class UTTT(State):
    """
    Class for states of UTTT game.
    
    Attributes:
        M (int): 
            number of rows in the board, defaults to ``15``.            
        N (int): 
            number of columns in the board, defaults to ``15``.
        SYMBOLS (List):
            list of strings representing stone symbols (black, white) or ``"."`` for empty cell. 
    """        
    
    N = 9
    SYMBOLS = [' O ', ' * ', ' X '] # ["\u25CB", "+", "\u25CF"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        if self.parent:
            self.board = np.copy(self.parent.board)
            self.sup_board_wins = np.copy(self.parent.sup_board_wins)
        else:
            self.board = np.zeros((UTTT.N, UTTT.N), dtype=np.int8)
            self.sup_board_wins = np.zeros(10, dtype=np.int8)
            self.sup_board_wins[0:10] = -2
            print(self.sup_board_wins)
    
    @staticmethod
    def class_repr():
        """        
        Returns a string representation of class ``UTTT`` (meant to instantiate states of UTTT game), informing about the size of board.
        
        Returns:
            str: string representation of class ``UTTT`` (meant to instantiate states of UTTT game), informing about the size of board. 
        """        
        return f"{UTTT.__name__}_{UTTT.N}x{UTTT.N}"    
            
    def __str__(self):
        """        
        Returns a string representation of this ``UTTT`` state - the contents of its game board.
        
        Returns:
            str: string representation of this ``UTTT`` state - the contents of its game board.
        """                
        s = "  "
        for j in range(UTTT.N):
            s += f" {chr(j + ord('A'))} "
        s += "\n"
        for i in range(UTTT.N, 0, -1):
            s += str(i).rjust(2)
            for j in range(UTTT.N):
                s += UTTT.SYMBOLS[self.board[i - 1, j] + 1]
            s += str(i).ljust(2)
            s += "\n"
        s += "  "
        for j in range(UTTT.N):
            s += f" {chr(j + ord('A'))} "
        return s         
    
    def take_action_job(self, action_index):
        """
        Places a stone onto the crossing of the board indicated by the action_index (row: ``action_index // UTTT.N``, column: ``action_index % UTTT.N``)
        and returns ``True`` if the action is legal (crossing was not occupied).
        Otherwise, does no changes and returns ``False``.
 
        Args:
            action_index (int):
                index of crossing where to place a stone.
       
        Returns:
            action_legal (bool):
                boolean flag indicating if the specified action was legal and performed.
        """        
        i = action_index // UTTT.N
        j = action_index % UTTT.N
        if i < 0 or i >= UTTT.N or j < 0 or j >= UTTT.N:
            return False
       
        i0=i%3
        j0=j%3
        nb=i0*3+j0

        bi=i//3
        bj=j//3
        i0= bi*3
        j0=bj*3
        b=bi*3+bj
        if self.sup_board_wins[-1] != -2:
            if self.sup_board_wins[-1] != b:
                return False
        
        if self.sup_board_wins[b] != -2:
            return False
       
        if self.sup_board_wins[nb]!= -2:
            self.sup_board_wins[9] = -2
        else:
            self.sup_board_wins[9] = nb

           
        if self.board[i, j] != 0:
            return False
       
        
        self.board[i, j] = self.turn
       

        #Poziomo
        if (self.board[i0][j0]==self.board[i0][j0+1]) and (self.board[i0][j0+1]==self.board[i0][j0+2]) and self.board[i0][j0]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0]
        if (self.board[i0+1][j0]==self.board[i0+1][j0+1]) and (self.board[i0+1][j0+1]==self.board[i0+1][j0+2]) and self.board[i0+1][j0]!= 0:
            self.sup_board_wins[b] = self.board[i0+1][j0]
        if (self.board[i0+2][j0]==self.board[i0+2][j0+1]) and (self.board[i0+2][j0+1]==self.board[i0+2][j0+2]) and self.board[i0+2][j0]!= 0:
            self.sup_board_wins[b] = self.board[i0+2][j0]
        #Pionowo
        if (self.board[i0][j0]==self.board[i0+1][j0]) and (self.board[i0+1][j0]==self.board[i0+2][j0]) and self.board[i0][j0]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0]
        if (self.board[i0][j0+1]==self.board[i0+1][j0+1]) and (self.board[i0+1][j0+1]==self.board[i0+2][j0+1]) and self.board[i0][j0+1]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0+1]
        if (self.board[i0][j0+2]==self.board[i0+1][j0+2]) and (self.board[i0+1][j0+2]==self.board[i0+2][j0+2]) and self.board[i0][j0+2]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0+2]
        #Skosy
        if (self.board[i0][j0]==self.board[i0+1][j0+1]) and (self.board[i0+1][j0+1]==self.board[i0+2][j0+2]) and self.board[i0][j0]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0]
        if (self.board[i0][j0+2]==self.board[i0+1][j0+1]) and (self.board[i0+1][j0+1]==self.board[i0+2][j0]) and self.board[i0][j0+2]!= 0:
            self.sup_board_wins[b] = self.board[i0][j0+2]

        sum_of_non_zero=0
        for l in range(3):
            for k in range(3):
                if self.board[i0+l][j0+k]!=0:
                    sum_of_non_zero+=1
        if sum_of_non_zero==9:
            self.sup_board_wins[b]=0
       
        if self.sup_board_wins[b] != -2 and nb == b:
            self.sup_board_wins[-1] = -2
       
        self.turn *= -1
        return True


    def compute_outcome_job(self):
        """        
        Computes and returns the game outcome for this state in compliance with rules of UTTT game: 
        {-1, 1} denoting a win for the minimizing or maximizing player, respectively, if he connected exactly 5 his stones (6 or more do not count for a win); 
        0 denoting a tie, when the board is filled and no line of 5 exists; 
        ``None`` when the game is ongoing.
        
        Returns:
            outcome ({-1, 0, 1} or ``None``)
                game outcome for this state.
        """        
        i = self.last_action_index // UTTT.N
        j = self.last_action_index % UTTT.N

        numba = False
        if numba: # a bit faster outcome via numba
            numba_outcome = UTTT.compute_outcome_job_numba_jit(UTTT.N, UTTT.N, self.turn, i, j, self.board)
            if numba_outcome != 0:
                return numba_outcome 
        else:
            last_token = -self.turn        

            for k in range(3):
                if (self.sup_board_wins[k] == self.sup_board_wins[k + 3] and self.sup_board_wins[k + 3] == self.sup_board_wins[k + 6]) and self.sup_board_wins[k] != -2 and self.sup_board_wins[k] != 0:
                    return self.sup_board_wins[k]

            for k in range(3):
                if (self.sup_board_wins[k*3] == self.sup_board_wins[k*3 + 1] and self.sup_board_wins[k*3 + 1] == self.sup_board_wins[k*3 + 2]) and self.sup_board_wins[k*3] != -2 and self.sup_board_wins[k*3] != 0:
                    return self.sup_board_wins[k*3]
                
            if (self.sup_board_wins[0] == self.sup_board_wins[4] and self.sup_board_wins[4] == self.sup_board_wins[8]) and self.sup_board_wins[0] != -2 and self.sup_board_wins[0] != 0:
                return self.sup_board_wins[0]
            
            if (self.sup_board_wins[2] == self.sup_board_wins[4] and self.sup_board_wins[4] == self.sup_board_wins[6]) and self.sup_board_wins[2] != -2 and self.sup_board_wins[2] != 0:
                return self.sup_board_wins[2]
                                                     
        if np.all(self.sup_board_wins[0:9] != -2):
            return 0
        return None        

    @staticmethod
    @jit(int8(int8, int8, int8, int8, int8, int8[:, :]), nopython=True, cache=True)  
    def compute_outcome_job_numba_jit(M, N, turn, last_i, last_j, board):
        """Called by ``compute_outcome_job`` for faster outcomes."""
        last_token = -turn        
        i, j = last_i, last_j
        # N-S
        total = 0
        for k in range(1, 6):
            if i - k < 0 or board[i - k, j] != last_token:
                break
            total += 1
        for k in range(1, 6):
            if i + k >= M or board[i + k, j] != last_token:
                break            
            total += 1
        if total == 4:
            return last_token        
        # E-W
        total = 0
        for k in range(1, 6):
            if j + k >= N or board[i, j + k] != last_token:
                break
            total += 1
        for k in range(1, 6):
            if j - k < 0 or board[i, j - k] != last_token:
                break            
            total += 1
        if total == 4:
            return last_token
        # NE-SW
        total = 0
        for k in range(1, 6):
            if i - k < 0 or j + k >= N or board[i - k, j + k] != last_token:
                break
            total += 1
        for k in range(1, 6):
            if i + k >= M or j - k < 0 or board[i + k, j - k] != last_token:
                break
            total += 1            
        if total == 4:
            return last_token
        # NW-SE
        total = 0
        for k in range(1, 6):
            if i - k < 0 or j - k < 0 or board[i - k, j - k] != last_token:
                break
            total += 1
        for k in range(1, 6):
            if i + k >= M or j + k >= N or board[i + k, j + k] != last_token:
                break
            total += 1            
        if total == 4:
            return last_token        
        return 0        
                            
    def take_random_action_playout(self):
        """        
        Picks a uniformly random action from actions available in this state and returns the result of calling ``take_action`` with the action index as argument.
        
        Returns:
            child (State): 
                result of ``take_action`` call for the random action.          
        """        
        if self.sup_board_wins[-1] == -2:
            indexes=[]
            for i in range(9):
                if self.sup_board_wins[i] == -2:
                    index_0 = (i//3 * 3 * 9 + ((i % 3) * 3))
                    for j in range(3):
                        indexes.append(index_0+j)
                    for j in range(3):
                        indexes.append(index_0+j+9)
                    for j in range(3):
                        indexes.append(index_0+j+18)
        else:
            for i in range(9):
                if self.sup_board_wins[-1] == i:
                    index_0 = (i//3 * 3 * 9 + ((i % 3) * 3))
                    break
            indexes=[]
            for i in range(3):
                indexes.append(index_0+i)
            for i in range(3):
                indexes.append(index_0+i+9)
            for i in range(3):
                indexes.append(index_0+i+18)
 
        indexes = np.array(indexes)[self.board.ravel()[indexes] == 0]

        if len(indexes) == 0:
            return None

        action_index = np.random.choice(indexes)

        action_index = np.random.choice(indexes)
        child = self.take_action(action_index)
        return child    
    
    def get_board(self):
        """                
        Returns the board of this state (a two-dimensional array of bytes).
        
        Returns:
            board (ndarray[np.int8, ndim=2]):
                board of this state (a two-dimensional array of bytes).
        """        
        return self.board
    
    def get_extra_info(self):
        return self.sup_board_wins
   
    @staticmethod
    def action_name_to_index(action_name):
        """        
        Returns an action's index (numbering from 0) based on its name. E.g., name ``"B4"`` for 15 x 15 UTTT maps to index ``18``.
        
        Args:
            action_name (str):
                name of an action.
        Returns:
            action_index (int):
                index corresponding to the given name.   
        """        
        letter = action_name.upper()[0]
        j = ord(letter) - ord('A')
        i = int(action_name[1:]) - 1
        return i * UTTT.N + j

    @staticmethod
    def action_index_to_name(action_index):
        """        
        Returns an action's name based on its index (numbering from 0). E.g., index ``18`` for 15 x 15 UTTT maps to name ``"B4"``.
        
        Args:
            action_index (int):
                index of an action.
        Returns:
            action_name (str):
                name corresponding to the given index.          
        """        
        i = action_index // UTTT.N
        j = action_index % UTTT.N
        return f"{chr(ord('A') + j)}{i + 1}"
   
    @staticmethod
    def get_board_shape():
        """
        Returns a tuple with shape of boards for UTTT game.
        
        Returns:
            shape (tuple(int, int)):
                shape of boards related to states of this class.
        """        
        return (UTTT.N, UTTT.N)

    @staticmethod
    def get_extra_info_memory():
        """        
        Returns amount of memory (in bytes) needed to memorize additional information associated with UTTT states - currently 0 (no such information).
        
        Returns:
            extra_info_memory (int):
                number of bytes required to memorize additional information associated with UTTT states.
        """        
        return 10

    @staticmethod
    def get_max_actions():
        """
        Returns the maximum number of actions (the largest branching factor) equal to the product: ``UTTT.N * UTTT.N``.
        
        Returns:
            max_actions (int):
                maximum number of actions (the largest branching factor) equal to the product: ``UTTT.N * UTTT.N``.
        """                        
        return UTTT.N * UTTT.N