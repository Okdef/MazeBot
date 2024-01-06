#Tests.py
#this will be used for unit tests

import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0,0,num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

    def test(self):
        num_cols = 5
        num_rows = 5
        m2 = Maze(0,0,num_rows,num_cols,10,10)
        visit_check = []
        for i in range(len(m2._cells)):
            for j in range(len(m2._cells[i])):
                visit_check.append(m2._cells[i][j].visited)
        self.assertEqual(visit_check, [False]*(num_rows*num_cols))
if __name__ == "__main__": unittest.main()

