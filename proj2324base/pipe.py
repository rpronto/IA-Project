# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 106700 Afonso Cordeiro Ferreira Rosa
# 105672 Rafael Alexandre Proença Pronto

import sys
import copy
import numpy as np
from sys import *
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

FC, FB, FE, FD, BC, BB, BE, BD, VC, VB, VE, VD, LH, LV = (
    'FC', 'FB', 'FE', 'FD', 'BC', 'BB', 'BE', 'BD', 'VC', 'VB', 'VE', 'VD', 'LH', 'LV'
)

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def set_grid(self, grid):
        self.board.set_grid(grid)
    
    def get_board(self):
        return self.board
    
    def increase_state_id(self):
        self.state_id += 1

    def decrease_state_id(self):
        PipeManiaState.state_id -= 1

       
    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, input):
        self.grid = np.array(input)
        self.size = len(self.grid)
        self.pos = 1

    def increase_pos(self):
        self.pos += 1

    def get_grid(self):
        return self.grid
    
    def set_grid(self, grid):
        self.grid = grid
    
    def set_value(self, row: int, col: int, value):
        self.grid[row][col] = value

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (
            self.grid[row - 1][col] if row > 0 else 'None',
            self.grid[row + 1][col] if row < self.size - 1 else 'None'
        )
        
    def adjacent_horizontal_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (
            self.grid[row][col - 1] if col > 0 else 'None',
            self.grid[row][col + 1] if col < self.size - 1 else 'None'
        )

    def adjacent_right_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente à direita"""
        return self.grid[row][col + 1] if col + 1 < self.size else 'None'
        
        
    def adjacent_left_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente à direita"""
        return self.grid[row][col - 1] if col - 1 > -1 else 'None'
        
    def adjacent_upper_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente abaixo"""
        return self.grid[row - 1][col] if row - 1 > -1 else 'None'
        
    
    def adjacent_lower_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente abaixo"""
        return self.grid[row + 1][col] if row + 1 < self.size else 'None'
        

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        input_lines = []
        while True:
            line = stdin.readline().split()
            if line == []:
                break
            input_lines.append(line)
        return Board(input_lines)

    def print_grid(self):
        for row in self.grid:
            print('\t'.join(row))
        return ""

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, initial_state: Board):
        """O construtor especifica o estado inicial."""
        self.initial = initial_state

    def get_pos(self, id, n):    
        min, max = 0, n - 1
        
        lim = n*4 - 4

        if(id > lim):
            new_id = id - lim
            n -= 2
            row = ((new_id - 1)//n) + 1
            col = ((new_id - 1)%n) + 1
      
        else:
            if id <= n:
                row = min
                col = id - 1
            elif n < id <= n*2 - 1:
                col = max
                row = id - n 
            elif n*2 - 1 < id <= n*3 - 2:
                row = max
                col = n*3 - 2 - id
            elif n*3 - 2 < id <= n*4 - 4:
                col = min
                row = 4*n - 3 - id
        return (row, col)
    
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento.
        0 -> ROTATE_CLOCKWISE
        1 -> ROTATE_COUNTERCLOCKWISE
        90 -> 90 graus de rotação, no sentido horário ou anti-horário
        180 -> 180 graus de rotação, no sentido horário (180 graus a posição 
        será igual independentemente do sentido da rotação então consideramos 
        sempre o sentido horário)
        Peça de ligação roda sempre para a direita 90 graus (o resultado é independente do sentido)
        """
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
        actions = []
        n = state.board.size
        
        id = state.board.pos
        state.board.increase_pos()
        if id > n*n:
            return actions
        pos = self.get_pos(id, n)
        row = pos[0]
        col = pos[1]
        piece = state.board.get_value(row, col)
        min_pos = 0
        max_pos = n - 1

        right_exit = [FD, BC, BB, BD, VB, VD, LH]
        left_exit = [FE, BC, BB, BE, VC, VE, LH]
        upper_exit = [FC, BC, BE, BD, VC, VD, LV]
        lower_exit = [VE, VB, LV, BB, BE, BD, FB]
        
        if (col == min_pos) and (row != min_pos):                  
            lower_piece = state.board.adjacent_lower_value(row, col)                 
            left_piece = state.board.adjacent_left_value(row, col)
            if lower_piece in upper_exit:                                    
                if (left_piece in right_exit): 
                    if piece in [VE, BE, BB]:
                        actions.append((row, col, 0))                              
                    if piece in [VD, BD, BC]:
                        actions.append((row, col, 2)) 
                    if piece in [VC, BC, BE]: 
                        actions.append((row, col, -1)) 
                    if piece in [VB, BB, BD] :
                        actions.append((row, col, 1))  
                    
                else:
                    if piece in [FB, BD, VB, LV]:
                        actions.append((row, col, 0))                                                          
                    if piece in [FC, BE, VC]:
                        actions.append((row, col, 2))  
                    if piece in [FE, BB, VE]: 
                        actions.append((row, col, -1))   
                    if piece in [FD, BC, VD, LH] :
                        actions.append((row, col, 1))   
                    
            else:                                                               
                if (left_piece in right_exit):
                    if piece in [FE, BC, VC, LH]:
                        actions.append((row, col, 0))                                  
                    if piece in [FD, BB, VB]:
                        actions.append((row, col, 2))  
                    if piece in [FC, BD, VD]: 
                        actions.append((row, col, -1))   
                    if piece in [FB, BE, VE, LV] :
                        actions.append((row, col, 1))   
                    
                else:
                    if piece in [VD, FD, FC]:
                        actions.append((row, col, 0))                                                          
                    if piece in [VE, FE, FB]:
                        actions.append((row, col, 2))  
                    if piece in [VB, FB, FD]: 
                        actions.append((row, col, -1))   
                    if piece in [VC, FC, FE] :
                        actions.append((row, col, 1))     
                    
                    
        elif (col == max_pos) and (row != max_pos):                  
            upper_piece = state.board.adjacent_upper_value(row, col)                 
            right_piece = state.board.adjacent_right_value(row, col)
            if upper_piece in lower_exit:                                    
                if (right_piece in left_exit):
                    if piece in [VD, BD, BC]:
                        actions.append((row, col, 0))                               
                    if piece in [VE, BE, BB]:
                        actions.append((row, col, 2))  
                    if piece in [VB, BB, BD]: 
                        actions.append((row, col, -1))   
                    if piece in [VC, BC, BE] :
                        actions.append((row, col, 1))     
                    
                else:
                    if piece in [FC, BE, VC, LV]:
                        actions.append((row, col, 0))                                                           
                    if piece in [FB, BD, VB]:
                        actions.append((row, col, 2))  
                    if piece in [FD, BC, VD]: 
                        actions.append((row, col, -1))   
                    if piece in [FE, BB, VE, LH] :
                        actions.append((row, col, 1))    
                    
            else:                                                               
                if (right_piece in left_exit):
                    if piece in [FD, BB, VB, LH]:
                        actions.append((row, col, 0))                                  
                    if piece in [FE, BC, VC]:
                        actions.append((row, col, 2))  
                    if piece in [FB, BE, VE]: 
                        actions.append((row, col, -1))   
                    if piece in [FC, BD, VD, LV] :
                        actions.append((row, col, 1))     
                    
                else:
                    if piece in [VE, FE, FB]:
                        actions.append((row, col, 0))                                                           
                    if piece in [VD, FD, FC]:
                        actions.append((row, col, 2))  
                    if piece in [VC, FC, FE]: 
                        actions.append((row, col, -1))   
                    if piece in [VB, FB, FD] :
                        actions.append((row, col, 1))     
                    
            if row == min_pos:
                actions = self.check_adjacent(piece, state, row, col, actions, 0)       
        elif (row == max_pos) and (col != min_pos):                             
            lower_piece = state.board.adjacent_lower_value(row, col)                 
            right_piece = state.board.adjacent_right_value(row, col)
            if lower_piece in upper_exit:                                    
                if (right_piece in left_exit):                                  
                    if piece in [VB, BB, BD]:
                        actions.append((row, col, 0))                               
                    if piece in [VC, BC, BE]:
                        actions.append((row, col, 2))  
                    if piece in [VE, BE, BB]: 
                        actions.append((row, col, -1))   
                    if piece in [VD, BD, BC]:
                        actions.append((row, col, 1))     
                    
                else:                                                           
                    if piece in [FB, BE, VE, LV]:
                        actions.append((row, col, 0))                                                           
                    if piece in [FC, BD, VD]:
                        actions.append((row, col, 2))  
                    if piece in [FE, BC, VC]: 
                        actions.append((row, col, -1))  
                    if piece in [FD, BB, VB, LH]:
                        actions.append((row, col, 1))     
                    
            else:                                                               
                if (right_piece in left_exit):
                    if piece in [FD, VD, BC, LH]:
                        actions.append((row, col, 0))                                 
                    if piece in [FE, VE, BB]:
                        actions.append((row, col, 2))  
                    if piece in [FB, VB, BD]: 
                        actions.append((row, col, -1))  
                    if piece in [FC, VC, BE, LV] :
                        actions.append((row, col, 1))   
                    
                else:
                    if piece in [FC, VC, FE]:
                        actions.append((row, col, 0))                                                            
                    if piece in [FB, VB, FD]:
                        actions.append((row, col, 2))  
                    if piece in [FD, VD, FC]: 
                        actions.append((row, col, -1))   
                    if piece in [FE, VE, FB] :
                        actions.append((row, col, 1))  
                        
            if col == max_pos: 
                actions = self.check_adjacent(piece, state, row, col, actions, 1)
            
        else:                                                                   
            upper_piece = state.board.adjacent_upper_value(row, col)                 
            left_piece = state.board.adjacent_left_value(row, col)
            if upper_piece in lower_exit:                                    
                if (left_piece in right_exit):
                    if piece in [VC, BC, BE]:
                        actions.append((row, col, 0))                               
                    if piece in [VB, BB, BD]:
                        actions.append((row, col, 2))  
                    if piece in [VD, BD, BC]: 
                        actions.append((row, col, -1))   
                    if piece in [VE, BE, BB] :
                        actions.append((row, col, 1))     
                    
                else:
                    if piece in [FC, BD, VD, LV]:
                        actions.append((row, col, 0))                                                           
                    if piece in [FB, BE, VE]:
                        actions.append((row, col, 2)) 
                    if piece in [FD, BB, VB]: 
                        actions.append((row, col, -1))   
                    if piece in [FE, BC, VC, LH] :
                        actions.append((row, col, 1))     
                    
            else:                                                               
                if (left_piece in right_exit):
                    if piece in [FE, BB, VE, LH]:
                        actions.append((row, col, 0))                                  
                    if piece in [FD, BC, VD]:
                        actions.append((row, col, 2))  
                    if piece in [FC, BE, VC]: 
                        actions.append((row, col, -1))   
                    if piece in [FB, BD, VB, LV] :
                        actions.append((row, col, 1))     
                    
                else:
                    if piece in [FB, FD, VB]:
                        actions.append((row, col, 0))                                                           
                    if piece in [FC, FE, VC]:
                        actions.append((row, col, 2))  
                    if piece in [FE, VE, FB]: 
                        actions.append((row, col, -1))   
                    if piece in [FD, FC, VD] :
                        actions.append((row, col, 1)) 
                    
            if row == max_pos:
                actions = self.check_adjacent(piece, state, row, col, actions, 2)
        if piece in [FC, FD, FE, FB]:
            final_actions = self.check_fechos(piece, state, row, col, actions)
            return final_actions
        return actions

    
    def check_fechos(self, piece, state: PipeManiaState, row: int, col: int, actions):
        values_v = state.board.adjacent_vertical_values(row, col)
        values_h = state.board.adjacent_horizontal_values(row, col)
        fecho = [FC, FD, FB, FE]
        ligacao = [LH, LV]
        possible_result = []
        final_actions = []
        if (values_v[0] not in fecho) and (values_v[0] != 'None'):
            if values_v[0] in ligacao:
                upper_2 = state.board.adjacent_upper_value(row - 1, col)
                if (upper_2 not in fecho) and (upper_2 != 'None'):
                    possible_result.append(FC)
            else:         
                possible_result.append(FC)
        if (values_v[1] not in fecho) and (values_v[1] != 'None'):
            if values_v[1] in ligacao:
                lower_2 = state.board.adjacent_lower_value(row + 1, col)
                if (lower_2 not in fecho) and (lower_2 != 'None'):
                    possible_result.append(FB)
            else:         
                possible_result.append(FB)
        if  (values_h[0] not in fecho) and (values_h[0] != 'None'):
            if values_h[0] in ligacao:
                left_2 = state.board.adjacent_left_value(row, col - 1)
                if (left_2 not in fecho) and (left_2 != 'None'):
                    possible_result.append(FE) 
            else:         
                possible_result.append(FE)
        if  (values_h[1] not in fecho) and (values_h[1] != 'None'):
            if values_h[1] in ligacao:
                right_2 = state.board.adjacent_right_value(row, col + 1)
                if (right_2 not in fecho) and (right_2 != 'None'):
                    possible_result.append(FD)
            else:         
                possible_result.append(FD)
                
        for action in actions:
            pos_piece = fecho.index(piece)
            pos_final = (pos_piece + action[2]) % len(fecho)
            if fecho[pos_final] in possible_result:
                final_actions.append(action)
        return final_actions
        
                
    def check_adjacent(self, piece, state: PipeManiaState, row: int, col: int, actions, flag):
        if flag == 0:
            adjacent_piece = state.board.adjacent_left_value(row, col)
        elif flag == 1:
            adjacent_piece = state.board.adjacent_upper_value(row, col)
        else: 
            adjacent_piece = state.board.adjacent_right_value(row, col)
        
        final_actions = []
        right_exit = [FD, BC, BB, BD, VB, VD, LH]
        left_exit = [FE, BC, BB, BE, VC, VE, LH]
        upper_exit = [FC, BC, BE, BD, VC, VD, LV]
        lower_exit = [VE, VB, LV, BB, BE, BD, FB]
        fecho = [FC, FD, FB, FE]
        bifurcacao = [BC, BD, BB, BE]
        volta = [VC, VD, VB, VE]
        ligacao = [LH, LV]

        adjacent_exits = [right_exit, lower_exit, left_exit]
        piece_exits = [left_exit, upper_exit, right_exit]

        if piece in fecho:
            tipo = fecho
        elif piece in bifurcacao:
            tipo = bifurcacao
        elif piece in volta:
            tipo = volta
        elif piece in ligacao:
            tipo = ligacao
        for action in actions:
            pos_piece = tipo.index(piece)
            pos_final = (pos_piece + action[2]) % len(tipo)
            if ((adjacent_piece in adjacent_exits[flag]) and (tipo[pos_final] in piece_exits[flag])) or ((adjacent_piece not in adjacent_exits[flag]) and (tipo[pos_final] not in piece_exits[flag])):
                final_actions.append(action)
        return final_actions 

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
        new_board = copy.deepcopy(state.board)
        row = action[0]
        col = action[1]
        piece = state.board.get_value(row, col)
        if action[2] != 0:
            fecho = [FC, FD, FB, FE]
            bifurcacao = [BC, BD, BB, BE]
            volta = [VC, VD, VB, VE]
            ligacao = [LH, LV]
            if piece in fecho:
                tipo = fecho
            elif piece in bifurcacao:
                tipo = bifurcacao
            elif piece in volta:
                tipo = volta
            elif piece in ligacao:
                tipo = ligacao
            
            pos = tipo.index(piece)
            pos_final = (pos + action[2]) % len(tipo)
            piece = tipo[pos_final]
        new_board.set_value(row, col, piece)
        new_state = PipeManiaState(new_board)  
        return new_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        right_exit = [FD, BC, BB, BD, VB, VD, LH, 'None']
        left_exit = [FE, BC, BB, BE, VC, VE, LH, 'None']
        upper_exit = [FC, BC, BE, BD, VC, VD, LV, 'None']
        lower_exit = [VE, VB, LV, BB, BE, BD, FB, 'None']
    
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
        n = state.board.size
        if state.board.pos < n*n:
            return False
        
        def is_valid_piece(row, col):
            return (0 <= row < state.board.size) and (0 <= col < state.board.size)

        def get_neighbors(row, col):
            neighbors = []
            if is_valid_piece(row + 1, col):
                neighbors.append((row + 1, col))
            if is_valid_piece(row - 1, col):
                neighbors.append((row - 1, col))
            if is_valid_piece(row, col + 1):
                neighbors.append((row, col + 1))
            if is_valid_piece(row, col - 1):
                neighbors.append((row, col - 1))
            return neighbors
        
        def is_connected(piece, neighbor_piece, row, col, nb_row, nb_col):
            if (nb_row, nb_col) == (row, col + 1):  
                return piece in right_exit and neighbor_piece in left_exit
            if (nb_row, nb_col) == (row + 1, col):  
                return piece in lower_exit and neighbor_piece in upper_exit
            if (nb_row, nb_col) == (row, col - 1):  
                return piece in left_exit and neighbor_piece in right_exit
            if (nb_row, nb_col) == (row - 1, col):  
                return piece in upper_exit and neighbor_piece in lower_exit
            return False
        
        def dfs(start_row, start_col, visited):
            stack = [(start_row, start_col)]
            while stack:
                row, col = stack.pop()
                if (row, col) in visited:
                    continue
                visited.add((row, col))
                piece = state.board.get_value(row, col)
                for neighbor in get_neighbors(row, col):
                    if neighbor in visited:
                        continue
                    nb_row, nb_col = neighbor
                    neighbor_piece = state.board.get_value(nb_row, nb_col)
                    if neighbor_piece != 'None' and is_connected(piece, neighbor_piece, row, col, nb_row, nb_col):
                        stack.append(neighbor)
        
        visited = set()
        
        dfs(0, 0, visited)
        
        if len(visited) != n*n:
            return False
        return True
       

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""   
        pass
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()

    problem = PipeMania(board)
    
    goal_node = depth_first_tree_search(problem)

    if isinstance(goal_node.state, PipeManiaState):
        goal_node.state.board.print_grid()
    elif isinstance(goal_node.state, Board):
        goal_node.state.print_grid()

    pass
