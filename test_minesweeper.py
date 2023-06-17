import pytest
from minesweeper import Minesweeper
from minesweeper import Sentence
from minesweeper import MinesweeperAI

testboard = Minesweeper()
player = MinesweeperAI()

def test_neighbouring_cells():
    assert player.neighbouring_cells((0,0)) == {(0,1), (1,0), (1,1)}
    assert player.neighbouring_cells((6,6)) == {(5,5), (5,6), (5,7), (6,5), (6,7), (7,5), (7,6), (7,7)}
