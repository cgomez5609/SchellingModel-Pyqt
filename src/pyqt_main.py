import random

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from agent import Agent

NUM_ROWS = 45
NUM_COLS = 45

WEALTH_PERCENTAGE = 0.15


class MainWindow(QWidget):
    def __init__(self, num_of_agent_classes, num_agents_per_class, satisfaction_threshold):
        super().__init__()
        self.setFixedSize(800, 800)
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(1)
        if num_of_agent_classes > 5:
            print("Classes cannot exceed 5. This will be set to 5")
            self.num_of_agent_classes = 5
        else:
            self.num_of_agent_classes = num_of_agent_classes
        self.iteration = 1
        self.T = satisfaction_threshold
        if num_agents_per_class * self.num_of_agent_classes > 1000:
            print(f"For classes of {self.num_of_agent_classes} it cannot exceed 200 per class type")
            print("This will be set to 200")
            self.num_agents_per_class = 200
        else:
            self.num_agents_per_class = num_agents_per_class
        self.agents = list()
        self.agents_count = 0
        self.setup_up_grid()
        self.setLayout(self.grid)
        self.setWindowTitle("Schelling Model")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.change_agents_location()
            # self.grid.update()
            # self.show()

    def setup_up_grid(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                agent = Agent(type="-", row=i, col=j, T=self.T)
                agent.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(agent, i, j)
        self.initial_set_up()

    def initial_set_up(self):
        for class_type in range(1, self.num_of_agent_classes+1):
            num_of_wealthy_agents = int(self.num_agents_per_class * WEALTH_PERCENTAGE)
            for c_type in range(self.num_agents_per_class):
                added = False
                while not added:
                    row = random.randint(0, NUM_ROWS - 1)
                    col = random.randint(0, NUM_COLS - 1)
                    item = self.grid.itemAtPosition(row, col).widget()
                    if item.type == "-":
                        if num_of_wealthy_agents > 0:
                            new_agent = Agent(type=str(class_type), row=row, col=col, T=self.T, wealth=True, index=self.agents_count)
                            num_of_wealthy_agents -= 1
                        else:
                            new_agent = Agent(type=str(class_type), row=row, col=col, T=self.T, index=self.agents_count)
                        self.update_grid_node(n_agent=new_agent, row=row, col=col)
                        self.agents.append(new_agent)
                        self.agents_count += 1
                        added = True

        for agent in self.agents:
            agent.satisfied(self.grid, num_rows=NUM_ROWS, num_cols=NUM_COLS)
            agent.update_info_stats()
            self.grid.itemAtPosition(agent.row, agent.col).widget().setToolTip(agent.info)

    def change_agents_location(self):
        unchanged_count = 0
        for agent in self.agents:
            agent_row = agent.row
            agent_col = agent.col
            if not agent.is_satisfied:
                added = False
                while not added:
                    row = random.randint(0, NUM_ROWS - 1)
                    col = random.randint(0, NUM_COLS - 1)
                    item = self.grid.itemAtPosition(row, col).widget()
                    if item.type == "-":
                        agent.row = row
                        agent.col = col
                        self.update_grid_node_iter(n_agent=agent, row=agent.row, col=agent.col,
                                                   prev_row=agent_row, prev_col=agent_col)
                        added = True
            else:
                unchanged_count += 1
        print("Number of agents unchanged:", unchanged_count)

        print()
        print("Iteration", self.iteration)
        self.iteration += 1

        for agent in self.agents:
            agent.satisfied(self.grid, num_rows=NUM_ROWS, num_cols=NUM_COLS)
            agent.update_info_stats() # update tooltip info
            self.grid.itemAtPosition(agent.row, agent.col).widget().setToolTip(agent.info)

    def update_grid_node(self, n_agent, row, col):
        self.grid.itemAtPosition(row, col).widget().type = n_agent.type
        self.grid.itemAtPosition(row, col).widget().setText(n_agent.type)
        self.grid.itemAtPosition(row, col).widget().setStyleSheet(n_agent.agent_style)

    def update_grid_node_iter(self, n_agent, row, col, prev_row, prev_col):
        self.grid.itemAtPosition(row, col).widget().type = n_agent.type
        self.grid.itemAtPosition(row, col).widget().setText(n_agent.type)
        self.grid.itemAtPosition(row, col).widget().setStyleSheet(n_agent.agent_style)
        # remove agent from previous grid node
        self.grid.itemAtPosition(prev_row, prev_col).widget().type = "-"
        self.grid.itemAtPosition(prev_row, prev_col).widget().setText("-")
        self.grid.itemAtPosition(prev_row, prev_col).widget().setStyleSheet("")

    def count_the_wealthy(self):
        total = 0
        for agent in self.agents:
            if agent.is_wealthy:
                total += 1
        print("Number of wealthy agents:", total)

