# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 106700 Afonso Cordeiro Ferreira Rosa
# 105672 Rafael Alexandre Proença Pronto

import sys
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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, input):
        self.grid = np.array(input)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

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

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

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
        fecho = [FC, FB, FE, FD]
        bifurcacao = [BC, BB, BE, BD]
        volta = [VC, VB, VE, VD]
        ligacao = [LH, LV]
        
        actions = []
        for row in range(state.board.rows):
            for col in range(state.board.cols):
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
                    elif col == state.board.cols:
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
                elif row == state.board.rows:
                    if col == 0:
                        if piece in [VE, FB, FE]:
                            actions.append((row, col, 0, 180))  #180
                        if piece in [VB, FB, FD]: 
                            actions.append((row, col, 1, 90))   #esquerda
                        if piece in [VC, FC, FE] :
                            actions.append((row, col, 0, 90))   #direita  
                        if piece in [VD, FC, FD]:
                            actions.append((row, col, 0, 0))  
                    elif col == state.board.cols:
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
                elif col == state.board.cols:
                    if piece in [FC, FB, FD, BD, VD, VB]:
                        actions.append((row, col, 0, 180))  #180
                    if piece in [VC, VD, FC, FE, FD, BC]: 
                        actions.append((row, col, 1, 90))   #esquerda
                    if piece in [FB, FE, FD, BB, VB, VE]:
                        actions.append((row, col, 0, 90))   #direita  
                    if piece in [LV, VE, VC, BE, FB, FC, FE]:
                        actions.append((row, col, 0, 0))
                elif piece in ligacao:
                    actions.append((row, col, 0, 90))
                else:    
                    actions.append((row, col, 0, 90))
                    actions.append((row, col, 0, 180))
                    actions.append((row, col, 1, 90))
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()

    state = PipeManiaState(board)

    problem = PipeMania(state.board)
    
    state.board.print_grid()

    print(problem.actions(state))
    pass
