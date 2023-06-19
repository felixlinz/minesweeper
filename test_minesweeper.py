from minesweeper import Minesweeper
from minesweeper import Sentence
from minesweeper import MinesweeperAI


# Sentence
sentence1 = Sentence({1,2,3,4,5}, 3)
sentence2 = Sentence({1,2,3}, 1)
sentence3 = Sentence({4,5,6,7}, 0)
sentence4 = Sentence({8,9,7}, 3)

def test_known_mines():
    assert sentence1.known_mines() == False
    assert sentence2.known_mines() == False
    assert sentence3.known_mines() == False
    assert sentence4.known_mines() == {8,9,7}

def test_known_safes():
    assert sentence1.known_safes() == False
    assert sentence2.known_safes() == False
    assert sentence3.known_safes() == {4,5,6,7}
    assert sentence4.known_safes() == False

def test_mark_mine():
    sentence1.mark_mine(1)
    assert sentence1.cells == {2,3,4,5}
    assert sentence1.count == 2
    sentence1.cells = {1,2,3,4,5}
    sentence1.count = 3
    sentence2.mark_mine(4)
    assert sentence2.cells == {1,2,3}
    assert sentence2.count == 1

def test_mark_safe():
    sentence3.mark_safe(7)
    assert sentence3.cells == {4,5,6}
    assert sentence3.count == 0
    sentence3.cells = {4,5,6,7}
    sentence3.mark_safe(1)
    assert sentence3.cells == {4,5,6,7}

# AI Agent
player = MinesweeperAI()

def test_neighbouring_cells():
    assert player.neighbouring_cells((0,0)) == {(0,1), (1,0), (1,1)}
    assert player.neighbouring_cells((6,6)) == {(5,5), (5,6), (5,7), (6,5), (6,7), (7,5), (7,6), (7,7)}

def test_add_knowledge():
    player.add_knowledge((0,0), 2)
    assert player.moves_made == {(0,0)}
    assert player.safes == {(0,0)}
    player.add_knowledge((0,1),2)
    assert player.mines == {(1,0),(1,1)}
    assert player.safes == {(0,0),(0,1),(0,2),(1,2)}

def test_make_safe_move():
    player.safes = {(4,5)}
    assert player.make_safe_move() == (4,5)
    player.safes = set()
    assert player.make_safe_move() == None