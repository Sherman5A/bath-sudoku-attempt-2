# Sudoku Solver:

My implementation to solve Sudokus uses constraint propagation combined with a backtracking search and minimum remaining
values heuristics.

# Constraint Propagation:

In constraint propagation, when a variable's value is modified, the other related variable's domains are modified
accordingly, and are examined for any inconsistencies in constraints. This reduces the search's search space (IBM, 2022). 
However, constraint propagation alone can not solve harder Sudokus. Therefore, a search algorithm will be needed to
handle the rest of the search.

# Backtracking Algorithm:

Backtracking algorithms solve problems through searching repeatedly for possible solutions. When there is a failure
in satisfying the problem's constraints, the search reverts (backtracks) and resumes at the most recent point with 
untested choices (IBM, 2022).

# My Implementation:

## Overview:

Algorithm:
- Constraint propagation with backtracking search
Heuristics:
- Minimum remaining values

Constraints:
- No duplicate values in rows, columns, or 3x3 squares.
- Every square must have a value.

## Explanation:

Before starting to solve the Sudoku, my algorithm initialises a 9x9 array in which each element contains
a list of the digits from 1 to 9. This list represents each element's possible values. To get a list of the possible
values of the Sudoku's first element, we would access index 0, 0.

Representation of the Initial Array:

```
[
 [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, ,7 , 8, 9], ... [1, 2, 3, 4, 5, 6, 7, 8, 9]],
 [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, ,7 , 8, 9], ... [1, 2, 3, 4, 5, 6, 7, 8, 9]],
  .
  .
  .
  .
 [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, ,7 , 8, 9], ... [1, 2, 3, 4, 5, 6, 7, 8, 9]],
]
```
We then start to iterate through the elements of the given, partially filled, sudoku. The Sudoku's values are checked; 
if they are not in the digits from 1 to 9 then a failed Sudoku is returned. 
The element is then passed to a function that checks if it's value is not in the possible values array.
This prevents Sudokus which are inherently flawed by including a grid such as,

```
[2, 2, 0, 0, 0, 0, 0, 3, 0, 4]
```

Finally, we take this value and use it to remove this value from all of the other related elements, 
meaning columns, rows, and squares. If we eventually find that a element can only have one possible 
value then it is made concrete and eliminated from its related elements. Moreover, if there is only
one possible value for an empty square, then it is placed there.

```
[1, 2, 3, 4, 5, 6, 7, 8, 0]
```
9 must be placed in that empty square.

This implementation of constraint propagation is enough to solve simple Sudokus as seen in figure 1. However,
it encounters difficulty when dealing with harder Sudokus as possibilities for several values per square are introduced.

Figure 1: very easy Sudoku 0

```
[[1 0 4 3 8 2 9 5 6]  [[[1], [7], [4], [3], [8], [2], [9], [5], [6]], 
 [2 0 5 4 6 7 1 3 8]   [[2], [9], [5], [4], [6], [7], [1], [3], [8]],
 [3 8 6 9 5 1 4 0 2]   [[3], [8], [6], [9], [5], [1], [4], [7], [2]],
 [4 6 1 5 2 3 8 9 7]   [[4], [6], [1], [5], [2], [3], [8], [9], [7]],
 [7 3 8 1 4 9 6 2 5]   [[7], [3], [8], [1], [4], [9], [6], [2], [5]],
 [9 5 2 8 7 6 3 1 4]   [[9], [5], [2], [8], [7], [6], [3], [1], [4]],
 [5 2 9 6 3 4 7 8 1]   [[5], [2], [9], [6], [3], [4], [7], [8], [1]],
 [6 0 7 2 9 8 5 4 3]   [[6], [1], [7], [2], [9], [8], [5], [4], [3]],
 [8 4 3 0 1 5 2 6 9]   [[8], [4], [3], [7], [1], [5], [2], [6], [9]]
 ]                    ]
 ```

Figure 2: hard Sudoku number 2
```
[[0 2 0 0 0 6 9 0 0]   [[[1, 4, 5, 7, 8], [2], [1, 3, 4, 5, 7], [1, 7, 8], [1, 7, 8], [6], [9], [3, 4, 5, 7], [1, 3, 4, 5, 8]],                                
 [0 0 0 0 5 0 0 2 0]    [[1, 4, 7, 8], [1, 7, 8, 9], [1, 3, 4, 7], [1, 7, 8], [5], [1, 4, 8, 9], [1, 3, 4, 6, 8], [2], [1, 3, 4, 6, 8]], 
 [6 0 0 3 0 0 0 0 0]    [[6], [1, 5, 7, 8, 9], [1, 4, 5, 7], [3], [2], [1, 4, 8, 9], [1, 4, 5, 8], [4, 5, 7], [1, 4, 5, 8]],             
 [9 4 0 0 0 7 0 0 0]    [[9], [4], [1, 5, 6], [1, 5, 6, 8], [1, 3, 6, 8], [7], [2], [3, 5, 6], [1, 3, 5, 6]],                            
 [0 0 0 4 0 0 7 0 0]    [[1, 5, 8], [1, 5, 6, 8], [2], [4], [1, 3, 6, 8, 9], [1, 3, 5, 8, 9], [7], [3, 5, 6], [1, 3, 5, 6, 9]],          
 [0 3 0 2 0 0 0 8 0]    [[1, 5, 7], [3], [1, 5, 6, 7], [2], [1, 6, 9], [1, 5, 9], [1, 4, 5, 6], [8], [1, 4, 5, 6, 9]],                   
 [0 0 9 0 4 0 0 0 0]    [[2], [1, 5, 6, 7], [9], [1, 5, 6, 7, 8], [4], [1, 3, 5, 8], [3, 5, 6, 8], [3, 5, 6], [3, 5, 6, 8]],             
 [3 0 0 9 0 2 0 1 7]    [[3], [5, 6], [4, 5, 6], [9], [6, 8], [2], [4, 5, 6, 8], [1], [7]],                                              
 [0 0 8 0 0 0 0 0 2]    [[1, 4, 5, 7], [1, 5, 6, 7], [8], [1, 5, 6, 7], [1, 3, 6, 7], [1, 3, 5], [3, 4, 5, 6], [9], [2]]
]                      ] 
```

Therefore, a search was added to the program to handle the unsolved elements. A backtracking search was
used due to its simplicity and easy compatibility with the possible values list. To improve the 
efficiency of the search, a minimum remaining values heuristic was implemented. Elements with the least
amount of values are searched first. The search is complete when every length of possible values is 1.

# NumPy:

The NumPy library provided a plethora of useful utilities, especially in list manipulation. Without NumPy and its
documentation (, large parts of my code would have been significantly longer, especially when dealing with nested lists.
Furthermore, NumPy aided with the time efficiency of my program due to the libraries use of C code.

# Areas of Improvement:

This implementation uses triply nested lists; therefore, I had to use the deepcopy function from the 
copy library. This function takes large amounts processing time to complete and is used frequently in 
the search, slowing down my search considerably.
Using an alternative data structure that does not require such an intensive function to store the 
Sudoku's possible values could improve the performance of my search.

Furthermore, my code's performance could have been improved by utilising more of NumPy. A significant
portion of NumPy's functions use compiled C code. This is far faster than Python's code, improving
performance

# Other Attempts:

The initial solution for the Sudoku was a backtracking algorithm, lacking heuristics, only satisfying 
the Sudoku's constraints. The algorithm was very effective at solving very easy to medium, even more so 
than my final algorithm; however, the algorithm's speed suffered heavily in the harder puzzles, 
solving very few of them under 20 seconds.

A short attempt was made in implementing a backtracking algorithm using iteration with a minimum remaining values
heuristics. The attempt successfully solved all the algorithms. However, the implementation took over 120 seconds
to solve harder algorithms.

When researching solutions for solving the hard Sudokus, I discovered an algorithm for solving exact cover problems,
such as Sudoku called Algorithm X. However, when researching further into Algorithm X implementations (Assaf, n.d), 
I found that using the algorithm in Sudoku was very difficult, time-consuming, and hard to understand;
therefore, the experimentation was halted.

# Learning Outcomes:

This project was a great opportunity to learn about many new concepts, such as:
- Implementing backtracking and depth-first searches.
- Developing algorithms to meet times goals.
- Git branch control
- Constraint propagation
- NumPy utilities

# References:
- IBM, 2022. The constraint propagation algorithm [Online]. Available from: 
  <https://www.ibm.com/docs/en/icos/22.1.0?topic=constraints-constraint-propagation-algorithm>
  [Accessed 6 January 2023].
- IBM, 2022. Backtracking [Online]. Available from: 
  <https://www.ibm.com/docs/en/icos/22.1.0?topic=goals-backtracking>
  [Accessed 6 January 2023]
- Assaf Ali, n.d. Algorithm X in 30 lines! [Online]. Available from:
  <https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html>
  [Accessed 6 January 2023]
- NumPy Developers, n.d. NumPy user guide [Online]. Available form:
  <https://numpy.org/doc/stable/user/index.html>
  [Accessed 6 January 2023]