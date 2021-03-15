from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QToolTip

import enum


class AgentStyle(enum.Enum):
    AGENT_STYLE_1 = "border: 1px solid black; background-color: Plum; border-radius: 5px; color: white; width: 100px;"
    AGENT_STYLE_1_W = "border: 1px solid black; background-color: Orchid; border-radius: 5px; color: white; width: 100px;"

    AGENT_STYLE_2 = "border: 1px solid black; background-color: Cyan; border-radius: 5px; color: white;"
    AGENT_STYLE_2_W = "border: 1px solid black; background-color: DarkCyan; border-radius: 5px; color: white;"

    AGENT_STYLE_3 = "border: 1px solid black; background-color: SteelBlue; border-radius: 5px; color: white;"
    AGENT_STYLE_3_W = "border: 1px solid black; background-color: SlateBlue; border-radius: 5px; color: white;"

    AGENT_STYLE_4 = "border: 1px solid black; background-color: Magenta; border-radius: 5px; color: white;"
    AGENT_STYLE_4_W = "border: 1px solid black; background-color: MediumOrchid; border-radius: 5px; color: white;"

    AGENT_STYLE_5 = "border: 1px solid black; background-color: Turquoise; border-radius: 5px; color: white;"
    AGENT_STYLE_5_W = "border: 1px solid black; background-color: Teal; border-radius: 5px; color: white;"

QToolTip.setFont(QFont('SansSerif', 12))

class Agent(QLabel):
    def __init__(self, type, row, col, T, wealth=False, index=None):
        super().__init__(type)
        self.type = type
        self.index = index
        self.row = row
        self.col = col
        self.is_satisfied = False
        self.to_be_satisfied = T
        self.agent_style = None
        self.info = "empty"
        self.is_wealthy = wealth
        self.interests = None
        if self.type == "1":
            self.agent_style = AgentStyle.AGENT_STYLE_1.value
            if self.is_wealthy:
                self.agent_style = AgentStyle.AGENT_STYLE_1_W.value
            self.info = f"""<b>Agent {self.type}</b>
                                    <p>satisfied:{self.is_satisfied}</p>"""
        elif self.type == "2":
            self.agent_style = AgentStyle.AGENT_STYLE_2.value
            if self.is_wealthy:
                self.agent_style = AgentStyle.AGENT_STYLE_2_W.value
            self.info = f"""<b>Agent {self.type}</b>
                                                <p>satisfied:{self.is_satisfied}</p>"""
        elif self.type == "3":
            self.agent_style = AgentStyle.AGENT_STYLE_3.value
            if self.is_wealthy:
                self.agent_style = AgentStyle.AGENT_STYLE_3_W.value
            self.info = f"""<b>Agent {self.type}</b>
                                                <p>satisfied:{self.is_satisfied}</p>"""
        elif self.type == "4":
            self.agent_style = AgentStyle.AGENT_STYLE_4.value
            if self.is_wealthy:
                self.agent_style = AgentStyle.AGENT_STYLE_4_W.value
            self.info = f"""<b>Agent {self.type}</b>
                                                <p>satisfied:{self.is_satisfied}</p>"""
        elif self.type == "5":
            self.agent_style = AgentStyle.AGENT_STYLE_5.value
            if self.is_wealthy:
                self.agent_style = AgentStyle.AGENT_STYLE_5_W.value
            self.info = f"""<b>Agent {self.type}</b>
                                                <p>satisfied:{self.is_satisfied}</p>"""

    def update_info_stats(self):
        self.info = f"""<b>Agent {self.type}</b>
                    <p>satisfied:{self.is_satisfied}</p>
                    <p>wealth:{self.is_wealthy}</p>
                    <p>interests:{self.interests}</p>"""

    def satisfied(self, grid, num_rows, num_cols):
        row_length = num_rows
        col_length = num_cols
        satisfaction_count = 0
        nodes = list()

        if self.row-1 >= 0:  # UP
            satisfaction_count += self.calculate_satisfaction(row=self.row-1, col=self.col, grid=grid)
            nodes.append("up")
        if self.col+1 < col_length:  # RIGHT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row, col=self.col+1, grid=grid)
            nodes.append("right")
        if self.row+1 < row_length:  # DOWN
            satisfaction_count +=  self.calculate_satisfaction(row=self.row+1, col=self.col, grid=grid)
            nodes.append("down")
        if self.col-1 >= 0:  # LEFT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row, col=self.col-1, grid=grid)
            nodes.append("left")

        if self.row-1 >= 0 and self.col-1 >= 0:  # UP/LEFT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row-1, col=self.col-1, grid=grid)
            nodes.append("up/left")
        if self.row-1 >= 0 and self.col+1 < col_length:  # UP/RIGHT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row-1, col=self.col+1, grid=grid)
            nodes.append("up/right")
        if self.row+1 < row_length and self.col+1 < col_length:  # DOWN/RIGHT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row+1, col=self.col+1, grid=grid)
            nodes.append("down/right")
        if self.row+1 < row_length and self.col-1 >= 0:  # DOWN/LEFT
            satisfaction_count +=  self.calculate_satisfaction(row=self.row+1, col=self.col-1, grid=grid)
            nodes.append("down/left")

        if satisfaction_count >= self.to_be_satisfied:
            # print(f"Agent at row {self.row} and col {self.col} of type {self.type} is satisfied")
            # print(nodes)
            self.is_satisfied = True
        else:
            self.is_satisfied = False
            # print(f"Agent at row {self.row} and col {self.col} of type {self.type} is not satisfied")

    def calculate_satisfaction(self, row, col, grid):
        total = 0
        item = grid.itemAtPosition(row, col).widget()
        if item.type == self.type:
            total += 1
        # if item.is_wealthy:
        #     total += 3
        return total
