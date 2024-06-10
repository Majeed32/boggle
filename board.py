'''board.py: The Board class provides a basic game board interface, including
useful methods for creating and manipulating a grid of squares, methods for
converting screen coordinates to grid coordinates and vice versa, and methods
for setting and getting text to/from various locations outside of the grid.  It
also draws an exit and reset button and provides methods for checking for mouse
clicks inside of those regions.'''

from graphics import *
## NOTE:  graphics module methods are in camelCase as implemented originally

class Board:
    # _win: graphical window on which we will draw our board
    # _xinset: avoids drawing in corner of window
    # _yinset: avoids drawing in corner of window
    # _rows: number of rows in grid of squares
    # _cols: number of columns in grid of squares
    # _size: edge size of each square
    # _grid: _rows x _cols grid of text rectangles for displaying letters
    # _text_area: area on right hand side of grid to display text
    # _upper_word: area to display text above grid
    # _lower_word: area to display text below grid
    # _reset_button: clickable rectangle with text "RESET"
    # _exit_button: clickable rectangle with text "EXIT"

    __slots__ = [ '_xinset', '_yinset', '_rows', '_cols', '_size', \
                  '_grid', '_win', '_exit_button', '_reset_button', \
                  '_text_area', '_lower_word', '_upper_word']

    def __init__(self, win, xinset=50, yinset=50, rows=3, cols=3, size=50):
        # update class attributes
        self._xinset = xinset; self._yinset = yinset
        self._rows = rows; self._cols = cols
        self._size = size
        self._win = win
        self.make_board()


    # getter methods for attributes
    def get_win(self):
        return self._win

    def get_xinset(self):
        return self._xinset

    def get_yinset(self):
        return self._yinset

    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def get_size(self):
        return self._size

    def get_board(self):
        return self

    def get_grid_cell(self, row, col):
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols :
            return None
        return self._grid[row][col]

    def set_grid_cell(self, row, col, text, text_color="black", fill_color="white"):
        """
        Update the graphical representation on a single grid cell
        """
        cell = self._grid[row][col]
        cell.setText(text)
        cell.setTextColor(text_color)
        cell.setFillColor(fill_color)

    def reset_grid_graphics(self) :
        """
        Resets the text color and fill color of all cells to their
        default values.
        """
        for row in range(self._rows):
            for col in range(self._cols):
                self._grid[row][col].setTextColor("black")
                self._grid[row][col].setFillColor("white")

    def __make_text_area(self, point, fontsize=18, color="black", text=""):
        """Creates a text area"""
        text_area = Text(point, text)
        text_area.setSize(fontsize)
        text_area.setTextColor(color)
        text_area.setStyle("normal")
        return text_area

    def _make_textrect(self, point1, point2, fillcolor="white", text="", textcolor="black"):
        """Creates a rectangle with text in the center"""
        rect = Rectangle(point1, point2, fillcolor)

        text = Text(rect.getCenter(), text)
        text.setTextColor(textcolor)
        
        return TextRect(rect, text)

    def __make_text_areas(self):
        self._text_area = self.__make_text_area(Point(self._xinset * self._rows + self._size * 2,
                                                   self._yinset + 50), 14)
        #draw the text area below grid
        self._lower_word = self.__make_text_area(Point(160, 275))
        #draw the text area above grid
        self._upper_word = self.__make_text_area(Point(160, 25), color="red")
        
    def __make_grid(self):
        """Creates a row x col grid, filled with empty squares"""
        self._grid = [ [None for col in range(self._cols)] for row in range(self._rows) ]
        for x in range(self._cols):
            for y in range(self._rows):
                # create first point
                p1 = Point(self._xinset + self._size * x, 
                           self._yinset + self._size * y)
                # create second point
                p2 = Point(self._xinset + self._size * (x + 1), 
                           self._yinset + self._size * (y + 1))
                # create rectangle and add to graphical window
                self._grid[y][x] = self._make_textrect(p1, p2)

    def __make_buttons(self):
        """Create reset and exit buttons"""
        p1 = Point(50, 300); p2 = Point(130, 350)
        self._reset_button = self._make_textrect(p1, p2, text="RESET")
        p3 = Point(170, 300); p4 = Point(250, 350)
        self._exit_button = self._make_textrect(p3, p4, text="EXIT")        

    def make_board(self):
        """Create the board with the grid, text areas, and buttons"""
        self.__make_grid()
        self.__make_text_areas()
        self.__make_buttons()

    def __draw_buttons(self):
        """Draw reset and exit buttons"""
        self._reset_button.draw(self._win)
        self._exit_button.draw(self._win)

    def __draw_text_areas(self):
        """Draw the text areas to the right/lower/upper side of main grid"""
        self._text_area.draw(self._win)
        self._lower_word.draw(self._win)
        self._upper_word.draw(self._win)

    def __draw_grid(self):
        """Draws the row x col grid"""
        for r in range(self._rows):
            for c in range(self._cols):
                self._grid[r][c].draw(self._win)

    def draw_board(self):
        """Create the board with the grid, text areas, and buttons"""
        self._win.setBackground("white smoke")
        self.__draw_text_areas()
        self.__draw_buttons()
        self.__draw_grid()

    # convert Point to grid position (tuple)
    def get_position(self, point):
        '''
        Converts a window location (Point) to a grid position (tuple).
        Note: Grid positions are always returned as row, col
        Negative row or column values may be returned, indicating
        that point falls outside of the grid area
        '''
        px = point.getX()
        py = point.getY()

        if py < self._yinset:
            row = -1
        else:
            row = int((py - self._yinset) / self._size)

        if px < self._xinset:
            col = -1
        else:
            col = int((px - self._xinset) / self._size)
        return (row, col)

    # check for click inside specific rectangular region
    def __in_textrect(self, point, textrect):
        '''
        Returns True if a Point (point) exists inside a specific
        Rectangle (rect) on screen.
        '''
        px = point.getX()
        py = point.getY()
        r_left = textrect.getP1().getX()
        r_top = textrect.getP1().getY()
        r_right = textrect.getP2().getX()
        r_bottom = textrect.getP2().getY()

        return px > r_left and px < r_right and py > r_top and py < r_bottom

    # check for click in grid
    def in_grid(self, point):
        '''
        Returns True if a Point (point) exists inside the grid of squares.
        '''
        pt_x = point.getX()
        pt_y = point.getY()
        max_y = self._size * (self._rows + 1)
        max_x = self._size * (self._cols + 1)
        return pt_x <= max_x and pt_y <= max_y and pt_x >= self._xinset and pt_y >= self._yinset

    # clicked in exit button?
    def in_exit(self, point):
        '''
        Returns true if point is inside exit button (rectangle)
        '''
        return self.__in_textrect(point, self._exit_button)

    # clicked in reset button?
    def in_reset(self, point):
        '''
        Returns true if point is inside exit button (rectangle)
        '''
        return self.__in_textrect(point, self._reset_button)

    # set text to text area on right
    def get_string_from_text_area(self):
        '''
        Get text from text area to right of grid.
        '''
        return self._text_area.getText()

    # set text to text area on right
    def set_string_to_text_area(self, text):
        '''
        Sets text to text area to right of grid. Overwrites existing text.
        '''
        self._text_area.setText(text)

    # add text to text area below grid
    def get_string_from_lower_text(self):
        '''
        Get text from text area below grid.
        '''
        return self._lower_word.getText()


    # add text to text area below grid
    def set_string_to_lower_text(self, text):
        '''
        Set text to text area below grid.  Overwrites existing text.
        '''
        self._lower_word.setText( text )

    # add text to text area above grid
    def get_string_from_upper_text(self):
        '''
        Get text from text area above grid.
        '''
        return self._upper_word.getText()

    # set text to text area above grid
    def set_string_to_upper_text(self, text):
        '''
        Set text to text area above grid. Overwrites existing text.
        '''
        self._upper_word.setText(text)

if __name__ == "__main__":
    win = GraphWin("Board", 400, 400)

    # create new board with default values
    board = Board(win)

    # draw Board
    board.draw_board()

    # set string above grid
    board.set_string_to_upper_text("Upper text")

    # set and update string below grid
    board.set_string_to_lower_text("Lower text")

    # set string to text area to right of grid
    board.set_string_to_text_area("Text area")

    keep_going = True
    # loop and return info about mouse clicks until exit is clicked
    while keep_going:
        # wait for a mouse click
        point = win.getMouse()

        # calculate x and y value from point
        x,y = point.getX(), point.getY()

        # close window and exit if exit button is clicked
        if board.in_exit(point):
            print("Exiting...")
            keep_going = False

        # did we click reset?
        elif board.in_reset(point):
            print("Reset button clicked")
            board.reset_grid_graphics()

        # are we in the grid? if so, print coor and grid position
        elif board.in_grid(point):
            row,col = board.get_position(point)
            print("Clicked coord {} or grid ({},{})".format((x,y), row, col))

            board.set_grid_cell(row, col, "", "white", "green")

        #else just print info about mouse click
        else:
            print("Clicked coord {} which is not in grid".format((x,y)))
