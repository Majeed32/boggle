"""
Implements the functionality of a single cube on the Boggle board.
"""

from graphics import *
from board import Board
from brandom import random_int

class BoggleCube:
    """
    Represents the functionality of a Boggle cube 
    """
    # Attributes:
    #_faces: a tuple of strings that define the possible faces for display
    #_face_idx: an index into _faces (tuple of strings) that indicates which face is currently visible
    # add more attributes if needed!
    __slots__ = [ '_faces', '_face_idx' ]

    def __init__(self, faces, face_idx=0):
        """
        Constructs a new Boggle Cube with a tuple of possible faces and
        a current index that indicates which face is visible
        """
        #update class attributes
        self._faces = faces
        self._face_idx = face_idx


    def get_letter(self):
        """
        Returns letter (str) on the boogle cube face that is currently visible.
        >>> boggle_cube = BoggleCube(("A", "B", "C", "D", "E", "F"))
        >>> print(boggle_cube.get_letter())
        A
        """
        #return the visible face
        return self._faces[self._face_idx]

    def randomize(self):
        """
        Randomly sets one of the BoggleCube's faces to be visible.
        >>> cube = BoggleCube(("A", "B", "C", "D", "E", "F"))
        >>> cube.randomize()
        >>> let = cube.get_letter()
        >>> print(let in cube._faces)
        True
        """
        # randomize index of visible face
        self._face_idx = random_int(0, len(self._faces)-1)
 
    def __str__(self):
        """
        Returns a string representation of BoggleCube
        """
        # DO NOT MODIFY.
        return "BoggleCube({})".format(self.get_letter())

    def __repr__(self):
        """
        Concise string representation used when debugging
        (to keep it succinct, we just display the visible letter)
        """
        # DO NOT MODIFY.
        return self.get_letter()

    def __eq__(self, other):
        """
        Two BoggleCubes are equal if they have the same set of faces
        and if the same face is currently visible
        """
        # DO NOT MODIFY.
        return self._faces == other._faces and \
            self._face_idx == other._face_idx


if __name__ == "__main__":
    # The following code may be helpful for testing your code.
    # Visually inspect the results once you
    # are confident that the class is close to complete.
    # You are strongly encouraged to add more tests.
    
    from board import Board
    win = GraphWin("Boggle", 400, 400)
    n = 4
    board = Board(win, rows=n, cols=n)

    # Make three BoggleCube objects to place on the board
    cube1 = BoggleCube(("A", "A", "C", "I", "O", "T"))
    cube2 = BoggleCube(("B", "Y", "A", "B", "I", "L"))
    cube3 = BoggleCube(("C", "A", "D", "E", "M", "P"))

    # Update the board with the letter A, but leave default colors
    board.set_grid_cell(1,1, cube1.get_letter())

    # Update the board with the letter B, and change colors to "blue"
    board.set_grid_cell(2,1, cube2.get_letter(), "blue", "powder blue")

    # Update a TextRect with the letter C, and change colors to "green"
    board.set_grid_cell(1,3, cube3.get_letter(), "green", "DarkSeaGreen1")

    # Make the initialized board appear within the window
    board.draw_board()

    # pause for mouse click before exiting
    point = win.getMouse()
    win.close()
