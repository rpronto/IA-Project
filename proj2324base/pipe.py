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
        self.state_id -= 1
    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, input):
        self.grid = np.array(input)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def get_grid(self):
        return self.grid
    
    def set_grid(self, grid):
        self.grid = grid
    
    def set_value(self, row: int, col: int, value):
        self.grid[row][col] = value

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.grid[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        values = ()
        upper_row = row - 1
        lower_row = row + 1
        if (upper_row >= 0) and (upper_row < self.rows):
            values += (self.grid[upper_row][col],)
        else:
            values += ('None',)
        if (lower_row >= 0) and (lower_row < self.rows):
            values += (self.grid[lower_row][col],)
        else:
            values += ('None',)
        return values
        
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        values = ()
        left_col = col - 1
        right_col = col + 1
        if (left_col >= 0) and (left_col < self.cols):
            values += (self.grid[row][left_col],)
        else:
            values += ('None',)
        if (right_col >= 0) and (right_col < self.rows):
            values += (self.grid[row][right_col],)
        else:
            values += ('None',)
        return values

    def adjacent_right_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente à direita"""
        right_col = col + 1
        if right_col < self.rows:
            return self.grid[row][right_col]
        return 'None'
        
    def adjacent_left_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente à direita"""
        left_col = col - 1
        if left_col > -1:
            return self.grid[row][left_col]
        return 'None'
        
    def adjacent_upper_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente abaixo"""
        upper_row = row - 1
        if upper_row > -1:
            return self.grid[upper_row][col]
        return 'None'
    
    def adjacent_lower_value(self, row: int, col: int) -> (str):
        """Devolve o valor imediatamente abaixo"""
        lower_row = row + 1
        if lower_row < self.rows:
            return self.grid[lower_row][col]
        return 'None'

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
        top, bottom = 0, n - 1
        left, right = 0, n - 1
        
        lim = n*4 - 4
        prev_lim = 0

        while(id > lim):
            prev_lim = lim
            n -= 2
            lim += (n*4 - 4)
            if n == 1:
                lim += 1
            top += 1
            bottom -= 1
            right -= 1
            left += 1

        new_id = id - prev_lim
        
    
        count = 0
        for col in range(left, right + 1):
            count += 1
            if(count == new_id):
                return(top, col)
        top += 1
        
        for row in range(top, bottom + 1):
            count += 1
            if(count == new_id):
                return(row, right)
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                count += 1
                if(count == new_id):
                    return(bottom, col)
            bottom -= 1
        
        if left <= right:
            for row in range(bottom, top - 1, -1):
                count += 1
                if(count == new_id):
                    return(row, left)

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
        ligacao = [LH, LV]
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
            state.decrease_state_id()
        actions = []
        id = state.state_id
        n = state.board.rows
        pos = self.get_pos(id, n)
        row = pos[0]
        col = pos[1]
        if id > n*n:
            return actions
        piece = state.board.get_value(row, col)
        if row == 0:
            if col == 0:
                if piece in [VC, FC, FE]:
                    actions.append((row, col, 0, 180))  #180
                if piece in [VE, FE, FB]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [VD, FC, FD] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [VB, FB, FD]:
                    actions.append((row, col, 0, 0))
            elif col == n - 1:
                if piece in [VD, FC, FD]:  
                    actions.append((row, col, 0, 180))  #180
                if piece in [VC, FC, FE]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [VB, FB, FD] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [VE, FB, FE]:
                    actions.append((row, col, 0, 0))
            else:
                if piece in [FC, FE, FD, BC, VC, VD]:  
                    actions.append((row, col, 0, 180))  #180
                if piece in [FC, FB, FE, BE, VC, VE]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [BD, LV, VB, VD, FC, FB, FD] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [BB, LH, FB, FE, FD, VB, VE]:
                    actions.append((row, col, 0, 0))
        elif row == n - 1:
            if col == 0:
                if piece in [VE, FB, FE]:
                    actions.append((row, col, 0, 180))  #180
                if piece in [VB, FB, FD]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [VC, FC, FE] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [VD, FC, FD]:
                    actions.append((row, col, 0, 0))  
            elif col == n - 1:
                if piece in [VB, FB, FD]:
                    actions.append((row, col, 0, 180))  #180
                if piece in [VD, FC, FD]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [VE, FB, FE] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [VC, FC, FE]:
                    actions.append((row, col, 0, 0))
            else:
                if piece in [FB, FE, FD, BB, VB, VE]:
                    actions.append((row, col, 0, 180))  #180
                if piece in [FC, FB, FD, BD, VB, VD]: 
                    actions.append((row, col, 1, 90))   #esquerda
                if piece in [FC, FB, FE, BE, VC, VE, LV] :
                    actions.append((row, col, 0, 90))   #direita  
                if piece in [FC, FE, FD, LH, BC, VC, VD]:
                    actions.append((row, col, 0, 0))
        elif col == 0:
            if piece in [VC, VE, BE, FC, FB, FE]:
                    actions.append((row, col, 0, 180))  #180
            if piece in [FB, FE, FD, BB, VB, VE]: 
                actions.append((row, col, 1, 90))   #esquerda
            if piece in [FC, FE, FD, BC, VC, VD, LH] :
                actions.append((row, col, 0, 90))   #direita  
            if piece in [LV, VD, VB, BD, FD, FB, FC]:
                actions.append((row, col, 0, 0))
        elif col == n - 1:
            if piece in [FC, FB, FD, BD, VD, VB]:
                actions.append((row, col, 0, 180))  #180
            if piece in [VC, VD, FC, FE, FD, BC]: 
                actions.append((row, col, 1, 90))   #esquerda
            if piece in [FB, FE, FD, BB, VB, VE, LH]:
                actions.append((row, col, 0, 90))   #direita  
            if piece in [LV, VE, VC, BE, FB, FC, FE]:
                actions.append((row, col, 0, 0))
        elif piece in ligacao:
            actions.append((row, col, 0, 90))
            actions.append((row, col, 0, 0))
        else:    
            actions.append((row, col, 0, 90))
            actions.append((row, col, 0, 180))
            actions.append((row, col, 1, 90))
            actions.append((row, col, 0, 0))
        state.increase_state_id()
        return actions
    
    
#    def actions_2(self, state: PipeManiaState):
#        """Retorna uma lista de ações que podem ser executadas a
#        partir do estado passado como argumento.
#        0 -> ROTATE_CLOCKWISE
#        1 -> ROTATE_COUNTERCLOCKWISE
#        90 -> 90 graus de rotação, no sentido horário ou anti-horário
#        180 -> 180 graus de rotação, no sentido horário (180 graus a posição 
#        será igual independentemente do sentido da rotação então consideramos 
#        sempre o sentido horário)
#        Peça de ligação roda sempre para a direita 90 graus (o resultado é independente do sentido)
#        """
#        ligacao = [LH, LV]
#        if isinstance(state, PipeManiaState) == False:
#            state = PipeManiaState(state)
#            state.decrease_state_id()
#        actions = []
#        id = state.state_id
#        size = state.board.rows
#        if id > n*n:
#            return actions
#        
#        min_pos = 0
#        max_pos = n - 1
#        
#        n = size
#        inc = 0
#        lim = n*4 - 4
#        while(id > lim):
#            n -= 2
#            lim += (n*4 - 4)
#            inc +=1
#            min_pos += 1
#            max_pos -= 1
#            
#        
#        new_id = id - lim
#        pos = self.get_pos(new_id, n)
#        row = pos[0] + inc
#        col = pos[1] + inc
#        piece = state.board.get_value(row, col)
#        
#        right_exit = [FD, BC, BB, BD, VB, VD, LH]
#        left_exit = [FE, BC, BB, BE, VC, VE, LH]
#        upper_exit = [FC, BC, BE, BD, VC, VD, LV]
#        lower_exit = [VE, VB, LV, BB, BE, BD, FB]
#        
#        if row == min_pos:
#            upper_piece = state.board.adjacent_upper_value(row, col)      
#            if col == max_pos:
#                if upper_piece == 'None':
#                    if piece in  
#                else:
#                    right_piece = state.board.adjacent_right_value(row, col)
#            else:                  #nao esta na ultima coluna, ver esq e cima
#                left_piece = state.board.adjacent_left_value(row, col)
#                
#                
#        if row == max_pos:
#            if col == min_pos:
#            elif col == max_pos:
#            else:
#        elif col == min_pos:
#        elif col == max_pos:
#                     
#        state.increase_state_id()
#        return actions


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
            state.decrease_state_id()
        state_copy = copy.deepcopy(state)
        row = action[0]
        col = action[1]
        new_piece = state.board.get_value(row, col)
        if action[2] != 0 or action[3] != 0:
            direction = action[2]
            degrees = action[3]
            piece = state.board.get_value(row, col)
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
            if degrees == 90:
                if direction == 0:
                    pos += 1
                else:
                    pos -=1
                    if pos < 0:
                        pos = len(tipo) - 1
            else:    
                pos += 2
            
            pos_final = pos % len(tipo)
            new_piece = tipo[pos_final]

        state_copy.board.set_value(row, col, new_piece)  
        return state_copy

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        fecho = [FC, FD, FE, FB]
        right_exit = [FD, BC, BB, BD, VB, VD, LH, 'None']
        left_exit = [FE, BC, BB, BE, VC, VE, LH, 'None']
        upper_exit = [FC, BC, BE, BD, VC, VD, LV, 'None']
        lower_exit = [VE, VB, LV, BB, BE, BD, FB, 'None']
        if isinstance(state, PipeManiaState) == False:
            state = PipeManiaState(state)
        n = state.board.rows
        for row in range(state.board.rows):
            for col in range(state.board.cols):
                piece = state.board.get_value(row, col)
                right_piece = state.board.adjacent_right_value(row, col)
                lower_piece = state.board.adjacent_lower_value(row, col)
                if piece in upper_exit:
                    if row == 0: 
                        return False 
                if piece in lower_exit:
                    if row == n - 1:
                        return False
                    if (lower_piece not in upper_exit) or ((piece in fecho) and (lower_piece in fecho)) :
                        return False 
                if piece in left_exit:
                    if col == 0:
                        return False
                if piece in right_exit:
                    if col == n - 1:
                        return False
                    if (right_piece not in left_exit) or ((piece in fecho) and (right_piece in fecho)):
                        return False
                if (right_piece in left_exit) and (piece not in right_exit) and (right_piece != 'None'):
                    return False
                if (lower_piece in upper_exit) and (piece not in lower_exit) and (lower_piece != 'None'):
                    return False
        return True
       

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        count = 0
        
        fecho = [FC, FD, FE, FB]
        right_exit = [FD, BC, BB, BD, VB, VD, LH, 'None']
        left_exit = [FE, BC, BB, BE, VC, VE, LH, 'None']
        upper_exit = [FC, BC, BE, BD, VC, VD, LV, 'None']
        lower_exit = [VE, VB, LV, BB, BE, BD, FB, 'None']
        if isinstance(node.state, PipeManiaState) == False:
            node.state = PipeManiaState(node.state)
        n = node.state.board.rows
        for row in range(node.state.board.rows):
            for col in range(node.state.board.cols):
                piece = node.state.board.get_value(row, col)
                right_piece = node.state.board.adjacent_right_value(row, col)
                lower_piece = node.state.board.adjacent_lower_value(row, col)
                if piece in upper_exit:
                    if row == 0: 
                        count += 1
                if piece in lower_exit:
                    if row == n - 1:
                        count += 1
                    if (lower_piece not in upper_exit) or ((piece in fecho) and (lower_piece in fecho)) :
                        count += 1 
                if piece in left_exit:
                    if col == 0:
                        count += 1
                if piece in right_exit:
                    if col == n - 1:
                        count += 1
                    if (right_piece not in left_exit) or ((piece in fecho) and (right_piece in fecho)):
                        count += 1
                if (right_piece in left_exit) and (piece not in right_exit) and (right_piece != 'None'):
                    count += 1
                if (lower_piece in upper_exit) and (piece not in lower_exit) and (lower_piece != 'None'):
                    count += 1
        return count 

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()

    problem = PipeMania(board)
    
    goal_node = greedy_search(problem)

    if isinstance(goal_node.state, PipeManiaState):
        goal_node.state.board.print_grid()
    elif isinstance(goal_node.state, Board):
        goal_node.state.print_grid()

    pass
