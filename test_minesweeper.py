import pytest
from minesweeper import Minesweeper
from minesweeper import Sentence
from minesweeper import MinesweeperAI

testboard = Minesweeper()
player = MinesweeperAI()

assert player.neighbouring_cells((0,0)) == {(0,1), (1,0), (1,1)}
