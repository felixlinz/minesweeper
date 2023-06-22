import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count != 0 and self.count == len(self.cells):
            return self.cells
        return False

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return False

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -= 1
        except KeyError:
            return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        except KeyError:
            return


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark as move made, mark as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # add to knowledge base and figuere out if anything can be directly conculeded from it
        newsentence = Sentence(self.neighbouring_cells(cell), count)
        if safecells := newsentence.known_safes():
            self.safes.update(safecells)
        elif minecells := newsentence.known_mines():
            self.mines.update(minecells)
        self.knowledge.append(newsentence)
        
        if self.safes.difference(self.moves_made):
            return
        # infer new sets
        while True:
            reference_length = len(self.knowledge)
            related_sets = []
            for sentence in self.knowledge:
                subsentences = [sentence]
                for subsentence in self.knowledge:
                    if (subsentence.cells.issubset(sentence.cells)
                        and subsentence != sentence):
                        subsentences.append(subsentence)
                if len(subsentences) > 1:
                    related_sets.append(subsentences)

            # compare every comparable set
            if related_sets:
                for subsentences in related_sets:
                    parentsentence = subsentences[0]

                    for subsentence in subsentences[1:]:
                        inferred_sentence = (Sentence(
                                parentsentence.cells.symmetric_difference(
                                    subsentence.cells),
                                parentsentence.count - subsentence.count,
                            )
                        )
                        if inferred_sentence not in subsentences:
                            self.knowledge.append(inferred_sentence)
                            

                # figuere out if any other safe cells can be inferred
                safes = set()
                mines = set()

                for knowledge in self.knowledge:
                    if safecells := knowledge.known_safes():
                        for cell in safecells:
                            safes.add(cell)
                    elif minecells := knowledge.known_mines():
                        for cell in minecells:
                            mines.add(cell)
                    elif len(knowledge.cells) == 0:
                        del knowledge

                for cell in safes:
                    self.mark_safe(cell)
                for cell in mines:
                    self.mark_mine(cell)

            # remove any duplicates and other useless crap
            no_duplicates = []
            for knowledge in self.knowledge:
                if knowledge not in no_duplicates and len(knowledge.cells) > 0:
                    # adding a hash function to Sentence class might improve speed by 
                    # allowing "nu_dublicates" to be a set and avoid the slow list
                    # checking process
                    no_duplicates.append(knowledge)
            self.knowledge = list(no_duplicates)
            if len(self.knowledge) == reference_length:
                break

    def neighbouring_cells(self, cell):
        neighbours = set()
        removes = set()
        i, j = cell
        steps = [-1, 0, 1]

        for step_x in steps:
            for step_y in steps:
                neighbours.add((i + step_x, j + step_y))
        removes.add(cell)

        for neighbour in neighbours:
            x, y = neighbour
            if x not in range(self.height) or y not in range(self.width):
                removes.add(neighbour)
        return neighbours.difference(removes, self.moves_made)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try:
            move = self.safes.difference(self.moves_made).pop()
            return move
        except KeyError:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                possible_moves.add((i, j))
        try:
            return random.choice(
                list(possible_moves.difference(self.moves_made, self.mines))
            )
        except IndexError:
            return None