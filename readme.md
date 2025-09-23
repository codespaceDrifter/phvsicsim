this is a physics simulation app. with a Go backend and a Threejs frontend

the goal is to simulate the position, velocity, size, shape, etc of objects accurately through time. focus on only mechanical solid things right now.

TO DO:
USE PYTHON AND PYTORCH INSTEAD. NO GO, NO C++, NO NVNOPARA. USE torch.compile at function level. torch.set_grad_enabled(False) no grad globally. 

to do:
thermo.md complete with proofs
understand the code
camera selection
multi simulation frontend
- inelastic collision
- rotation



TO DO:
viewer: camera control. lock on objects. get their position, radius, and set to look at them.
new: use **A** and **D** keys to cycle locked targets. the camera snaps to the nearest object at start and moves to a good viewing distance.

# MERMAID DIAGRAM
classDiagram
class Tensor {
+int rows
+int cols
+float* data
+void fill(float)
}
class Backend {
+void MatMul(Tensor, Tensor)
}

Tensor --> Backend : used by
