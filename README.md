This Python script implements the search algorithms Depth-First Search, Breadth-First Search, Iterative Deepening Depth-First Search, Greedy Search, and A* (with Misplaced and Manhattan heuristics).

In the "input.txt" file, the text should be structured as follows:
```
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15
```
where the lines represent the initial and final configurations of the board, respectively.

Execute the following command in the command line:
```python 15puzzle.py <search_algorithm> <input_file>```

Example: ```python 15puzzle.py DFS input.txt``` runs the program with a Depth-First Search algorithm using the input from the file "input.txt".

The following will be printed in the terminal:
- The initial and final states given as input to the program.
- A message stating whether it is possible or not to reach the final state from the initial state.
- A message displaying the algorithm being applied and its maximum depth.
- A message when the algorithm finds the goal state and the number of steps required to reach it.
- Representation of the "path" that takes the board from the initial state to the final state.
- The program's execution time
