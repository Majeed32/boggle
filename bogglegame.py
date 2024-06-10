"""Implements the logic of the game of boggle."""

from graphics import GraphWin
from boggleboard import BoggleBoard
from bogglecube import BoggleCube
from brandom import randomize

class BoggleGame:  
    # Description of attributes:
    # _valid_words: the set of all valid Boggle words
    # _board: the BoggleBoard
    # _found_words: a list of strings of all words found so far
    # _selected_cubes: a list of BoggleCubes selected in current turn

    __slots__ = [ "_valid_words", "_board", "_found_words", "_selected_cubes" ]

    def __init__(self, win):
        """
        Create a new Boggle Game and load in our lexicon.
        """
        # set up the set of valid words we can match
        self._valid_words = self.__read_lexicon()

        # initialize and draw a BoggleBoard
        self._board = BoggleBoard(win)
        self._board.draw_board()

        # finish __init__ method
        #initialize a list for current_word and completed_words
        self._found_words = []
        self._selected_cubes = []

    def __read_lexicon(self, lexicon_name='bogwords.txt'):
        """
        A helper method to read the lexicon and return it as a set.
        """
        # DO NOT MODIFY.
        valid_words = set()
        with open(lexicon_name) as f:
          for line in f:
            valid_words.add(line.strip().upper())

        return valid_words

    def __reset_game(self):
        """
        Updates all game state to reflect the start of a "new" game
        """
        # reset game to initial state and shake the board
        self._board.reset()
        self._selected_cubes = []
        self._found_words = []
        self._board.shake_cubes()


    def __reset_turn(self):
        """
        Reset current turn by resetting state of selected cubes 
        as well as resetting any associated grid graphics (highlighted 
        letters or colored cells) and text from current word displayed on board
        """
        # reset graphics, lower_text_area and set selected_cubes to initial state
        self._board.reset_grid_graphics() 
        self._board.set_string_to_lower_text("") 
        self._selected_cubes = []
        
    

    def __highlight_cube(self, cube, text_color, fill_color):
        """
        Highlights a given cube by setting background grid cell to fill_color
        and text in cell to text_color.
        """
        # DO NOT MODIFY.
        r, c = self._board.get_bogglecube_coords(cube)
        letter = cube.get_letter()
        self._board.set_grid_cell(r, c, letter, text_color, fill_color)

    def __add_cube_to_word(self, cube):
        """
        Extends the current word (displayed on lower text area) by
        adding the visible letter from given cube
        """
        #update selected_cubes
        self._selected_cubes.append(cube)

    def __selected_cubes_to_word(self):
        """
        Returns the word spelled by the visible face of all selected cubes
        """
        word = "" # set an accumulator variable
        #add visible faces of cube to accumulator variable to form current_word
        for cube in self._selected_cubes:
            letter = BoggleCube.get_letter(cube)
            word += letter
        return word

        

    def do_one_click(self, point):
        """
        Implements the logic for processing one click.
        Returns True if play should continue, and False if the game is over.
        """
        # see handout for a step-by-step guide on how to implement this method
        # check for exit button
        if self._board.in_exit(point):
            return False
        # check for reset button
        elif self._board.in_reset(point):
            self.__reset_game()
        # check if in_grid:
        elif self._board.in_grid(point):
            current_cube = self._board.get_bogglecube_at_point(point)
            self.__highlight_cube(current_cube, "blue", "light blue") # sets color of current_cube
            # if first click, update lower_text_area
            if len(self._selected_cubes) == 0:
                self.__add_cube_to_word(current_cube)
                word = self.__selected_cubes_to_word()
                self._board.set_string_to_lower_text(word)
            else:
                self.__highlight_cube(self._selected_cubes[-1], "green", "light green") # sets color of any cube other than current_cube
                # check validity of cube before updating lower_text_area
                if current_cube not in self._selected_cubes and self._board.is_adjacent(current_cube, self._selected_cubes[-1]):
                    self._selected_cubes.append(current_cube)
                    word = self.__selected_cubes_to_word()
                    self._board.set_string_to_lower_text(word)
                elif current_cube == self._selected_cubes[-1]:
                    word = self.__selected_cubes_to_word()
                    # check validity of word_formed before updating upper_text_area
                    if len(word) >= 3 and word in self._valid_words and word not in self._found_words:
                        self._found_words.append(word)
                        word = ("\n").join(self._found_words)
                        self._board.set_string_to_text_area(word)
                    self.__reset_turn()
                # reset turn if not adjacent
                elif not self._board.is_adjacent(current_cube, self._selected_cubes[-1]):
                    self.__reset_turn()
        # reset turn if point is outside board
        else:
            self.__reset_turn()

        return True

if __name__ == '__main__':

    # When you are ready to run on different boards,
    # insert a call to randomize() here.  BUT you will
    # find it much easier to test your code without
    # randomizing things!
    randomize()

    win = GraphWin("Boggle", 400, 400)
    game = BoggleGame(win)
    keep_going = True
    while keep_going:
        point = win.getMouse()
        keep_going = game.do_one_click(point)
