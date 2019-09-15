# soft-body-simulator
A soft body physics simulator using the model of a spring matrix, with each node connect to the 8 surrounding nodes with a damped spring

Notes
----------------
    -Deformation beyond a certain point (depends on configuration) will lead to the matrix folding, this is a property
    of the model being used, along with the nodes having 2 degrees of freedom

    -having a spring matrix where its dimensions are (1,x) or (x,1) will yield an elastic rope simulation, however the
    damping and spring constant configuration will have to be adjusted to yield physically accurate results

    -the fps determines the cap fps along with the timestep used by the physic simulation (higher fps means smaller time step
    which means a more accurate simulation). fps config does not determine the speed of the simulation however if the simulation lags
    below the cap fps then the simulation will run slower  
----------------