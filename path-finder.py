import curses
from curses import wrapper
import queue
import time


maze = [
    ["|", "|", "O", "|", "|", "|", "|", "|", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", "|"],
    ["|", " ", "|", "|", " ", "|", "|", " ", "|"],
    ["|", " ", "|", " ", " ", " ", "|", "|", "|"],
    ["|", " ", "|", " ", "|", " ", "|", " ", "|"],
    ["|", " ", "|", " ", "|", " ", "|", " ", "|"],
    ["|", " ", "|", " ", "|", " ", "|", " ", "|"],
    ["|", " ", " ", " ", " ", " ", " ", " ", "|"],
    ["|", "|", "|", "|", "X", "|", "|", "|", "|"]
]


def maze_print(maze, stdscr, path = []):
    cyan = curses.color_pair(1)
    magenta = curses.color_pair(2)

    # goes through maze and adds every coordinate

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*3, 'X', magenta)
            else:
                stdscr.addstr(i, j*3, value, cyan)


def start_find(maze, start):
    # finds the starting point (O) in the maze

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    
    return None


def path_find(maze, stdscr):
    start = 'O'
    end = 'X'

    start_point = start_find(maze, start)

    q = queue.Queue() # define first-in, first-out data structure
    q.put((start_point, [start_point]))

    visited = set()

    while not q.empty():
        current_point, path = q.get()
        row, col = current_point

        stdscr.clear()
        maze_print(maze, stdscr, path)
        time.sleep(0.3)
        stdscr.refresh()

        if maze[row][col] == end:
            return path
        
        neighbours = neighbours_find(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            
            r, c = neighbour
            if maze[r][c] == '|':
                continue

            new_path = path + [neighbour] # adds neighbour to path
            q.put((neighbour, new_path))
            visited.add(neighbour) # adds neighbour as a destination the path finder has already been


def neighbours_find(maze, row, col):
    neighbours = []

    if row > 0: # finds the cell above
        neighbours.append((row - 1, col))

    if row + 1 < len(maze): # finds cell below
        neighbours.append((row + 1, col))

    if col > 0: # finds cell to left
        neighbours.append((row, col - 1))
    
    if col + 1 < len(maze[0]): # finds cell to right
        neighbours.append((row, col + 1))
    
    return neighbours


def main(stdscr):
    #creates a colour
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    path_find(maze, stdscr)
    stdscr.getch()


wrapper(main)
