# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 106700 Afonso Cordeiro Ferreira Rosa
# 105672 Rafael Alexandre Proença Pronto

import sys
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
        self.grid = input
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
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

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
    board.print_grid()
    print(board.adjacent_vertical_values(1,1))
    print(board.adjacent_horizontal_values(2,2))
    pass
