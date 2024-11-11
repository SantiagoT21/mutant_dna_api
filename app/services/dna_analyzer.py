from typing import List

class MutantDNA:
  """
  This class determines if a given DNA sequence belongs to a mutant or not.
  The sequence is represented as a list of strings, where each string is a row in a square table (N x N),
  and we need to check if there is more than one sequence of four consecutive identical letters in any direction
  (horizontal, vertical, diagonal).

  Methods:
  - is_mutant() -> bool: Determines if the DNA sequence corresponds to a mutant.
  """

  def __init__(self, dna: List[str]):
    """
    Initializes the MutantDNA instance with the DNA matrix and validates it.
    :param dna: List of strings representing the DNA matrix.
    """
    self.dna = [list(row) for row in dna]
    self.size = len(dna)
    self._validate_matrix()
  
  def _validate_matrix(self):
    """
    Validates the DNA matrix to ensure it is square.
    :raises ValueError: If the matrix is not square.
    """
    if any(len(row) != self.size for row in self.dna):
        raise ValueError("All rows must have the same length.")

  def _count_sequences_in_line(self, line: List[str]) -> int:
    """
    Checks if there are sequences of 4 identical consecutive letters in the line,
    ensuring no overlapping sequences are counted. Once a sequence is found, the 
    characters are marked as used to prevent counting them again.
    
    :param line: List of characters (row, column, or diagonal).
    :return: The count of valid sequences found in the line.
    """
    count = 0
    used = [False] * len(line)

    for i in range(len(line) - 3):
      if used[i] or used[i+1] or used[i+2] or used[i+3]:
        continue  # Skip if any of the characters in the current sequence are already used
      if line[i] == line[i+1] == line[i+2] == line[i+3]:
        count += 1
        used[i:i+4] = [True] * 4  # Mark all four letters as used

    return count

  def _generate_conditions(self, pos: int, mid: int) -> tuple:
    """
    Generates row and column conditions for checking sequences.

    :param pos: Position in the row or column to check.
    :param mid: Middle index of the matrix.
    :return: Lists of conditions for the row and column.
    """
    row_conditions, col_conditions = [], []
    start_offsets = [-2, -1, 0] if self.size == 6 else [-1]

    for offset in start_offsets:
      # Generate a pattern of 4 elements from the current position with the given offset
      row_pattern = [self.dna[pos][mid + offset + i] for i in range(4)]
      col_pattern = [self.dna[mid + offset + i][pos] for i in range(4)]
      row_conditions.append(row_pattern)
      col_conditions.append(col_pattern)

    return row_conditions, col_conditions

  def _count_sequences_in_conditions(self, conditions: List[List[str]]) -> int:
    """
    Counts sequences across multiple conditions.
    
    :param conditions: List of row or column sequences to check.
    :return: Count of valid sequences across all conditions.
    """
    return sum(self._count_sequences_in_line(condition) for condition in conditions)

  def _count_sequences_in_center(self, pos: int, mid: int) -> int:
    """
    Checks the center conditions for the row and column at position `pos`.
    
    :param pos: Position in the row or column to check.
    :param mid: Middle index of the matrix.
    :return: Count of matching patterns found (0 or 1).
    """
    row_conditions, col_conditions = self._generate_conditions(pos, mid)

    return self._count_sequences_in_conditions(row_conditions) + self._count_sequences_in_conditions(col_conditions)

  def _has_sequence_in_diagonal(self, start_row: int, start_col: int, row_step: int, col_step: int) -> bool:
    """
    Checks if there is a sequence of 4 identical elements in a specific diagonal.
    
    :param start_row: Starting row index.
    :param start_col: Starting column index.
    :param row_step: Step to move in rows.
    :param col_step: Step to move in columns.
    :return: True if a diagonal sequence is found, else False.
    """
    try:
      return (
        self.dna[start_row][start_col] == 
        self.dna[start_row + row_step][start_col + col_step] == 
        self.dna[start_row + 2 * row_step][start_col + 2 * col_step] == 
        self.dna[start_row + 3 * row_step][start_col + 3 * col_step]
      )
    except IndexError:
      return False

  def _count_diagonals_with_sequences(self, start_row: int, end_row: int, start_col: int, end_col: int, row_step: int, col_step: int) -> int:
    """
    Counts valid diagonal sequences in a specified section.
    
    :param start_row: Starting row index.
    :param end_row: Ending row index.
    :param start_col: Starting column index.
    :param end_col: Ending column index.
    :param row_step: Step to move in rows.
    :param col_step: Step to move in columns.
    :return: Count of diagonal matches found.
    """
    count = 0
    for row in range(start_row, end_row):
      for col in range(start_col, end_col):
        if self._has_sequence_in_diagonal(row, col, row_step, col_step):
          count += 1
          if count == 2:
            return count
    return count

  def _count_all_diagonal_sequences(self) -> int:
    """
    Counts all diagonal sequences in both directions.
    
    :return: Total count of diagonal matches.
    """
    count  = 0
    count  += self._count_diagonals_with_sequences(0, self.size - 3, 0, self.size - 3, 1, 1)  # "Right-Down" diagonals
    count  += self._count_diagonals_with_sequences(3, self.size, 0, self.size - 3, -1, 1)  # "Right-Up" diagonals
    return count

  def _analyze_dna(self):
    """
    Performs the general DNA analysis by checking horizontal, vertical, and diagonal sequences.
    
    :return: True if at least 2 sequences of 4 identical letters are found, False otherwise.
    """
    count = 0

    for row in self.dna:
      count += self._count_sequences_in_line(row)
      if count >= 2:
        return True

    for col in range(self.size):
      column_data = [self.dna[row][col] for row in range(self.size)]
      count += self._count_sequences_in_line(column_data)
      if count >= 2:
        return True

    count += self._count_all_diagonal_sequences()
    return count >= 2

  def is_mutant(self) -> bool:
    """
    Determines if the given DNA sequence belongs to a mutant.
    
    :return: True if the DNA sequence corresponds to a mutant, False otherwise.
    """

    if self.size < 4:
      return False
    elif self.size in {5, 6}:
      mid, count = (self.size - 1) // 2, 0
      for pos in range(self.size):
        count += self._count_sequences_in_center(pos, mid)
        if count >= 2:
          return True
      count += self._count_all_diagonal_sequences()
      return count >= 2
    else:
      return self._analyze_dna()