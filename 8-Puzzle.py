import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton
import heapq
import tkinter as tk
from tkinter import messagebox
import time

sol=[]

class PuzzleWindow(QWidget):
    grid_values = []
    text_box = None
    stop_flag = False
    stop_running_in_terminal = False
    dynamic_colors = []

    def __init__(self):
        super().__init__()

        # Set up the grid layout for the buttons
        self.grid_layout = QGridLayout()  # A new QGridLayout is created
        # This means that any child widgets added to the PuzzleWindow will be arranged according to this grid layout.
        self.setLayout(self.grid_layout)

        # Set up the font and color for the tiles defined in current method
        self.font_size = 20
        self.font = QFont('Arial', self.font_size)
        self.colors = [QColor('#FF6B6B'), QColor('#FFE66D'), QColor('#6ECB63'), QColor('#6ECB9F'), QColor('#6ED1CB'), QColor('#7C6ED1'), QColor('#D16EAD'), QColor('#D16E6E'), QColor('#D1A86E')]

        self.create_tiles()

        self.text_box = QLineEdit()
        # Add text2 to row 1, column 1
        self.grid_layout.addWidget(self.text_box, 3, 0, 1, 3)

        self.read_button = QPushButton("Read Input")
        self.read_button.clicked.connect(self.read_input)
        self.grid_layout.addWidget(self.read_button, 4, 0, 1, 3)

        self.rdo_A = QPushButton("Solve by hamming")
        self.rdo_A.clicked.connect(self.start_H)
        self.grid_layout.addWidget(self.rdo_A, 5, 0, 1, 3)

        self.rdo_manh = QPushButton("Solve by manhatten")
        self.rdo_manh.clicked.connect(self.start_M)
        self.grid_layout.addWidget(self.rdo_manh, 6, 0, 1, 3)

        # Add a "Stop" button to stop solving
        self.stop_button = QPushButton("Stop")
        # self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_solving)
        self.grid_layout.addWidget(self.stop_button, 8, 0, 1, 3)

        self.path_solution = QPushButton("Display step-by-step solve")
        self.path_solution.clicked.connect(self.solution)
        self.grid_layout.addWidget(self.path_solution, 9, 0, 1, 3)

        # Set the window properties
        self.setWindowTitle("8-Puzzle")
        self.setGeometry(100, 100, 320, 380)
        self.show()

    def start_H(self):
        switch = 'H'
        self.start_solving(switch)

    def start_M(self):
        switch = 'M'
        self.start_solving(switch)

    def check_solvable(self, state):
        List = list(map(int, state))
        inversion_count = 0
        blank_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if List[j] != blank_value and List[i] != blank_value and List[i] > List[j]:
                    inversion_count += 1
        if (inversion_count % 2 == 0):
            print("Solvable")
            self.rdo_A.setEnabled(True)
            self.rdo_manh.setEnabled(True)
        else:
            messagebox.showinfo(message="This state is not solvable!")
            self.rdo_A.setEnabled(False)
            self.rdo_manh.setEnabled(False)

    def read_input(self):
        # Get the text from the text box and split it by spaces
        self.stop_flag = False
        self.grid_values = []
        self.dynamic_colors = [QColor('#FFFFFF') for i in range(9)]
        for i in range(3):
            for j in range(3):
                button_in_grid = self.grid_layout.itemAtPosition(i, j).widget()
                button_in_grid.setText('')
        text = self.text_box.text()
        values = list(text)
        print(values)
        self.check_solvable(values)
        values = [values[i:i+3]
                for i in range(0, len(values), 3)]  # reshape the list to 3 by 3
        for i in range(3):
            self.grid_values.append(values[i])
            for j in range(3):
                button_in_grid = self.grid_layout.itemAtPosition(i, j).widget()
                if self.grid_values[i][j] != '0':
                    button_in_grid.setText(self.grid_values[i][j])
                    self.dynamic_colors[int(
                        self.grid_values[i][j])] = self.colors[i * 3 + j]
                else:
                    button_in_grid.setStyleSheet(
                        "background-color: %s; color: black;" % self.dynamic_colors[0].name())

        self.stop_running_in_terminal = False
        print(self.grid_values)

    def create_tiles(self):
        # Create the buttons and add them to the layout
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = QPushButton()
                button.setFixedSize(80, 80)
                button.setFont(self.font)
                index = i * 3 + j
                button.setStyleSheet("background-color: %s; color: black;" % self.colors[index].name())
                self.grid_layout.addWidget(button, i, j)
                self.buttons.append(button)

    def update_tiles(self):
        for i in range(3):
            for j in range(3):
                button_in_grid = self.grid_layout.itemAtPosition(i, j).widget()
                if self.grid_values[i][j] == '0':
                    button_in_grid.setText('')
                    button_in_grid.setStyleSheet("background-color: %s; color: black;" % self.dynamic_colors[0].name())
                else:
                    button_in_grid.setText(self.grid_values[i][j])
                    index = int(self.grid_values[i][j])
                    button_in_grid.setStyleSheet("background-color: %s; color: black;" % self.dynamic_colors[index].name())
                    # button_in_grid.update()
                QApplication.processEvents()

    def start_solving(self, switch):
        # switch = 'M'
        intial_state = list(map(lambda x: list(map(int, x)), self.grid_values))
        # create an instance of the Node class and assigns it to the variable puz
        puz = puzzle(intial_state)
        self.sol = puz.solve(switch)  # start the solving processself.grid_values
        self.stop_running_in_terminal = False

    def solution(self):
        while len(sol) != 0:
            node = sol.pop()
            self.grid_values = list(map(lambda row: list(map(str, row)), node.state))
            self.update_tiles()
            time.sleep(1)

    def stop_solving(self):
        text = ''
        for i in range(3):
            for j in range(3):
                text = text + self.grid_values[i][j]
        self.text_box.clear()
        self.text_box.setText(text)
        self.stop_flag = True
        self.stop_running_in_terminal = True

    def closeEvent(self, event):
        self.stop_running_in_terminal = True
        print("Goodbye!")
        event.accept()
##################################################################################################################


class Node:
    def __init__(self, state, switch, parent=None, move=0,  depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.heuristic = self.Heuristic(switch)
        self.score = self.depth+self.heuristic

    def __lt__(self, other):
        return self.score < other.score

    def Heuristic(self, switch):
        if switch == 'M':
            goel_state = {0: (2, 2), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4:(1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1)}
            result = 0
            for i in range(3):
                for j in range(3):
                    for k in range(8):
                        if self.state[i][j] == k:
                            result = result + abs(i - goel_state[k][0]) + abs(j - goel_state[k][1])
                            break
            return result
        elif switch == 'H':
            distance = 0
            for i in range(3):
                for j in range(3):
                    if self.state[i][j] != 0 and self.state[i][j] != 3*i + j + 1:
                        distance += 1
            return distance

    def get_moves(self):
        moves = []
        i, j = self.get_blank_position()
        if i > 0:
            moves.append('up')
        if i < 2:
            moves.append('down')
        if j > 0:
            moves.append('left')
        if j < 2:
            moves.append('right')
        return moves

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def move_blank(self, direction, switch):
        i, j = self.get_blank_position()
        # create a new copy of the state
        new_state = [row[:] for row in self.state]
        # swap
        if direction == 'up':
            new_state[i][j], new_state[i - 1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down':
            new_state[i][j], new_state[i + 1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left':
            new_state[i][j], new_state[i][j - 1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right':
            new_state[i][j], new_state[i][j + 1] = new_state[i][j+1], new_state[i][j]
        return Node(new_state, switch, self, direction, self.depth + 1)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))


class puzzle:

    def __init__(self, iput_state):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.initial_state = iput_state

    def path(self, node, sol):
        current_node = node
        sol.append(current_node)
        if current_node.depth == 0:
            return
        else:
            self.path(current_node.parent, sol)

    def solve(self, switch):
        start_node = Node(self.initial_state, switch)
        if start_node.heuristic == 0:
            return start_node
        heap = []
        visited = set()
        heapq.heappush(heap, start_node)
        while heap:
            QApplication.processEvents()
            if window.stop_flag:
                return
            if window.stop_running_in_terminal:
                return
            current_node = heapq.heappop(heap)
            window.grid_values = list(map(lambda row: list(map(str, row)), current_node.state))
            window.update_tiles()
            visited.add(current_node)
            if current_node.heuristic == 0:
                self.path(current_node,sol)
                return 
            for move in current_node.get_moves():
                child_node = current_node.move_blank(move, switch)
                if child_node not in visited:
                    heapq.heappush(heap, child_node)
        return None

##################################################################################################################
app = QApplication(sys.argv)
window = PuzzleWindow()
sys.exit(app.exec_())
