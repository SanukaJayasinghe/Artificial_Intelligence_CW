from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from search_methods import node_to_path, depth_first_search, a_star_search, Node


class Cell(str, Enum):
    EMPTY = " - "
    BLOCKED = " | "
    START = " S "
    GOAL = " G "
    PATH = " * "


class MazePosition(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int = 6, columns: int = 6, sparseness: float = 0.2,
                 start: MazePosition = MazePosition(1, 1), goal: MazePosition = MazePosition(4, 3)) -> None:
        # define basic instance variables
        self.rows: int = rows
        self.columns: int = columns
        self.start: MazePosition = start
        self.goal: MazePosition = goal
        # fill the maze with empty blocks
        self.grid: List[List[Cell]] = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        # fill the maze with blocked cells
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal positions
        self.grid[start.row][start.column] = Cell.START
        self.grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        count = 0
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness and count < 5:
                    self.grid[row][column] = Cell.BLOCKED
                    count += 1

    def __str__(self) -> str:
        output: str = ""
        for row in self.grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, mp: MazePosition) -> bool:
        return mp == self.goal

    def successors(self, mp: MazePosition) -> List[MazePosition]:
        locations: List[MazePosition] = []
        if mp.row + 1 < self.rows and self.grid[mp.row + 1][mp.column] != Cell.BLOCKED: # one down
            locations.append(MazePosition(mp.row + 1, mp.column))
        if mp.row - 1 >= 0 and self.grid[mp.row - 1][mp.column] != Cell.BLOCKED: # one up
            locations.append(MazePosition(mp.row - 1, mp.column))
        if mp.column + 1 < self.columns and self.grid[mp.row][mp.column + 1] != Cell.BLOCKED: # one right
            locations.append(MazePosition(mp.row, mp.column + 1))
        if mp.column - 1 >= 0 and self.grid[mp.row][mp.column - 1] != Cell.BLOCKED: # one left
            locations.append(MazePosition(mp.row, mp.column - 1))
        return locations

    def mark(self, path: List[MazePosition]):
        for maze_position in path:
            self.grid[maze_position.row][maze_position.column] = Cell.PATH
        self.grid[self.start.row][self.start.column] = Cell.START
        self.grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazePosition]):
        for maze_position in path:
            self.grid[maze_position.row][maze_position.column] = Cell.EMPTY
        self.grid[self.start.row][self.start.column] = Cell.START
        self.grid[self.goal.row][self.goal.column] = Cell.GOAL

def manhattan_distance(goal: MazePosition) -> Callable[[MazePosition], float]:
    def distance(mp: MazePosition) -> float:
        xdist: int = abs(mp.column - goal.column)
        ydist: int = abs(mp.row - goal.row)
        return (xdist + ydist)

    return distance

if __name__ == "__main__":
    # Generation of Maze
    m: Maze = Maze()
    print("Random Search Environment (Maze)")
    print(m)
    # Depth First Search
    solution1: Optional[Node[MazePosition]] = depth_first_search(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print("No solution found using Depth First Search!")
    else:
        path1: List[MazePosition] = node_to_path(solution1)
        m.mark(path1)
        print("Depth First Search")
        print(m)
        print("Solution ")
        print(path1)
        print("Cost: ")
        print(solution1.cost)
        m.clear(path1)
    # A* Search
    distance: Callable[[MazePosition], float] = manhattan_distance(m.goal)
    solution2: Optional[Node[MazePosition]] = a_star_search(m.start, m.goal_test, m.successors, distance)
    if solution2 is None:
        print("No solution found using A* Search!")
    else:
        path2: List[MazePosition] = node_to_path(solution2)
        m.mark(path2)
        print("A* Search")
        print(m)
        print("Solution: ")
        print(path2)
        print("Cost: ")
        print(solution2.cost)
        m.clear(path2)
