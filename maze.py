from random import randint

class Maze(object):
  """
    Perfect maze generator class
    - Class used to generate and store the Maze.
    - Implemented as a matrix (2 dimensions array) of _Cell
    - Uses the Depth-First algorithm
  """
  def __init__(self, length, width):
    super(Maze, self).__init__()
    if length <= 0 or width <= 0 :
      raise ValueError("dimensions of the maze must be stricly positive")
    self.__length = length
    self.__width = width

  def generate(self):
    """
      Main method that generate the maze
    """

    self.__generate_matrix()
    self.__generate_maze()
    # Since its a perfect maze, every cell is reachable, thus we can pick start
    # and end at the end of the algorithm
    self.__pick_start_end()

  def __generate_matrix(self):
    self.__matrix = []

    for i in range(self.__length):
      row = []
      for j in range(self.__width):
        cell = _Cell((i, j))
        if j == 0 :
          cell.set_borders(_Cell.WEST, True)
        elif j == self.__width - 1 :
          cell.set_borders(_Cell.EAST, True)
        if i == 0 :
          cell.set_borders(_Cell.NORTH, True)
        elif i == self.__length - 1 :
          cell.set_borders(_Cell.SOUTH, True)
        row.append(cell)
      self.__matrix.append(row)

  def __generate_maze(self):
    cell_stack = []
    cell_to_visit = []
    matrix = self.__matrix

    for row in self.__matrix :
      for column in row :
        cell_to_visit.append(column)

    # Chosing randomly one cell to start with
    i = randint(0, self.__length - 1)
    j = randint(0, self.__width - 1)
    current_cell = matrix[i][j]
    current_cell.visited = True
    cell_to_visit.remove(current_cell)

    while cell_to_visit :
      not_visited = self.__any_neighbor_available(current_cell)
      if not_visited :
        next_cell = not_visited[randint(0, len(not_visited) - 1)]
        next_cell.knock_down_wall(
          self.__get_relative_direction(next_cell, current_cell))
        current_cell.knock_down_wall(
          self.__get_relative_direction(current_cell, next_cell))
        cell_stack.append(current_cell)
        cell_to_visit.remove(next_cell)
        next_cell.visited = True
        current_cell = next_cell
      else :
        current_cell = cell_stack.pop()

  def __get_relative_direction(self, from_cell, to_cell):
    xa, ya = from_cell.coordinates
    xb, yb = to_cell.coordinates
    direction = (xb - xa, yb - ya)

    if direction == (-1, 0):
      return _Cell.NORTH
    elif direction == (1, 0):
      return _Cell.SOUTH
    elif direction == (0, 1):
      return _Cell.EAST
    elif direction == (0, -1):
      return _Cell.WEST

  def __any_neighbor_available(self, current_cell):
    """
      Check if there is any neighbor of the current_cell which was has not been
      yet visited, and return a list of those.
    """
    i, j = current_cell.coordinates
    matrix = self.__matrix
    not_visited = []
    if i < self.__length - 1 and not matrix[i+1][j].visited :
      not_visited.append(matrix[i+1][j])
    if i > 0 and not matrix[i-1][j].visited :
      not_visited.append(matrix[i-1][j])
    if j < self.__width - 1 and not matrix[i][j+1].visited :
      not_visited.append(matrix[i][j+1])
    if j > 0 and not matrix[i][j-1].visited :
      not_visited.append(matrix[i][j-1])

    return not_visited

  def __pick_start_end(self):
    """
      Pick randomly a start and an end to the maze, ensuring start and end will
      be on the opposed sides of the maze
    """
    roll = randint(0, 1)
    if roll == 1:
      start = randint(0, self.__width - 1)
      end = randint(0, self.__width - 1)
      self.__matrix[0][start].set_borders(_Cell.NORTH, False)
      self.__matrix[self.__length - 1][end].set_borders(_Cell.SOUTH, False)
    else :
      start = randint(0, self.__length - 1)
      end = randint(0, self.__length - 1)
      self.__matrix[start][0].set_borders(_Cell.WEST, False)
      self.__matrix[end][self.__width - 1].set_borders(_Cell.EAST, False)

  def draw(self):
    """
      Draw the maze with ascii art (or something like that ...)
    """
    matrix = self.__matrix
    hr = " "
    for row in matrix:
      line = ""
      for column in row:
        if matrix.index(row) == 0:
          if column.is_there_a_wall(_Cell.NORTH):
            hr += "_ "
          else :
            hr += "  "
        if column.is_there_a_wall(_Cell.WEST):
          line += "'"
        else :
          line += " "
        if column.is_there_a_wall(_Cell.SOUTH):
          line += "_"
        else :
          line += " "
      if row[len(row) - 1].is_there_a_wall(_Cell.EAST) :
        line += " '"
      if matrix.index(row) == 0:
        print(hr)
      print(line)

class _Cell(object):
  """
    Cell implementation needed for the maze
  """

  # Implementation of the four directions
  NORTH = 0
  SOUTH = 1
  EAST = 2
  WEST = 3

  def __init__(self, coordinates):
    super(_Cell, self).__init__()
    self.__walls = [1,1,1,1]
    self.__borders = [0,0,0,0]
    if isinstance(coordinates, tuple) :
      if len(coordinates) != 2:
        raise ValueError("value of a cell must be a tuple of two coordinates")
    elif coordinates is None :
        raise ValueError("value of a cell must not be None")
    else:
        raise ValueError("value of a cell must be a tuple")
    self.coordinates = coordinates
    self.visited = False

  def set_borders(self, direction, value):
    """
      Updates the borders of a cell
    """
    if value :
      self.__borders[direction] = 1
      self.__walls[direction] = 1
    else :
      self.__borders[direction] = 0
      self.__walls[direction] = 0

  def is_there_a_wall(self, direction):
    return self.__walls[direction]

  def knock_down_wall(self, direction):
    """
      Choose randomly a wall to knock down among all available for knock down.
      For defensive programming, it uses any_wall_still_up to ensure that we are
      knocking down a wall that is available.
    """


    self.__walls[direction] = 0

class MazeGenerationError(Exception):
  """
    Error fired during any step of the maze generation and related to bad a bad
    use of the methods given to the user.
  """

  def __init__(self, message):
    super(BlockSanityError, self).__init__(message)



