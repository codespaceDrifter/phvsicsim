simplicity is the goal  

function types:  
no class. yes return. pure functions  
yes class yes return: pure functions
no class. no return. side effects. i.e. IO, save/load, robotics. OR state changes.  
yes class. no return. change state. (think of it as returning something new but under the hood it is memory efficient)  

basically, if a function returns things, it does not change state. if it does not return anything, it either change states of struct or does IO. 

naming convention:
PascalCase all variables, structs, and functions. everything is public.
camelCase all files and packages