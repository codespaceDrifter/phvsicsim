this is a physics simulation app. with a Go backend and a Threejs frontend

the goal is to simulate the position, velocity, size, shape, etc of objects accurately through time. focus on only mechanical solid things right now.

hosted on local host 8000 for now.
to do:
1: make a common object class. in go, with the properties of size, shape (just rectangle for now, so only 3 dimensions). each time step, apply velocity to it. make a global thing that control timestep and then the global thing sends api to frontend. frontend use threejs to render. 