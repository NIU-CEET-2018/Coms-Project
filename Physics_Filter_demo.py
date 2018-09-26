#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import Physics_Filter
import matplotlib.pyplot as plt
import random

# DESCRIPTION:
# This code was written to demonstrate Physics_Filter
# Dummy data was created to be fed into the filter
# Kalman Filter is modelled a little differently for this, but general logic remains the same

# TODO:
# - [ ] Run the code and verify
# - [ ] Make the plots look prettier
#       - Create titles
#       - Create axis titles
#       - Create legends
#       - Make it colorful
# - [ ] Get this to handle 3 dimensions

# NOTE:
# The success of this relies heavily on how well we model the system and how well we quantify the covariances
# The validity of this demo doesn't guarantee us a good Kalman Filter for American Sign Language
# The ASL Kalman Filter is modelled differently than the demo Kalman Filter

# GLOBAL VARIABLES
initialPosition = 0
initialVelocity = 5
MatrixSize = 100
whiteNoiseSTDev = 9
deltaT = 0.5

# Only doing 1 dimension for now, need to figure out how to do this with 3D matrices

stateTransition = numpy.array([1,deltaT,0],[0,1,0],[0,0,0])


# stateTransition = numpy.array(([[1, 1, 1], [deltaT, deltaT, deltaT], [0, 0.5*deltaT^2, 0]], [[0, 0, 0], [1, 1, 1], [0, deltaT, 0]], [[0, 0, 0], [0, 0, 0], [0, 1, 0]]))

# DERIVATION of stateTransition:

# HORIZONTAL MOTION: (X)
# position     = initialPosition_x + initialVelocity_x*deltaT 
# velocity     = initialVelocity_x = constant
# acceleration = 0
    
# VERTICAL MOTION: (y)
# position     = initialPosition_y + initialVelocity_y*deltaT + 0.5*acceleration*deltaT^2
# velocity     = initialVelocity_y + acceleration*deltaT
# acceleration = gravity = -9.98 m/s = constant
    
# Z MOTION: 
# position     = initialPosition_z + initialVelocity_z*deltaT
# velocity     = initialVelocity_z = constant
# acceleration = 0
    
# STATE TRANSITION MATRIX:
# tuple form where tuples are organized in (x, y, z) components

# stateVectors   stateTransition
# position     : (initPos_x, initPos_y, initPos_z), (delT*initVel_x, delT*initVel_y, delT*initVel_z), (0, 0.5*delT^2*accel, 0)
# velocity     : (0,         0,         0        ), (initVel_x,      initVel_y,      initVel_z     ), (0, delT,             0)
# acceleration : (0,         0,         0        ), (0,              0,              0             ), (0, accel,            0)

# In other words, 
# stateVectors   stateTransition
# position     : (1, 1, 1), (deltaT, deltaT, deltaT), (0, 0.5*deltaT^2, 0)
# velocity     : (0, 0, 0), (1,      1,      1     ), (0, deltaT,       0)
# acceleration : (0, 0, 0), (0,      0,      0     ), (0, 1,            0)
    
# The tuples are organized in (x, y, z) components

# Another translation of the maths above
# constant velocity in the x direction with zero acceleration
# constant velocity in the z direction with zero acceleration
# constant acceleration in the y direction, simulating object falling

def main():
    
    # create dummy data to be analyzed
    measuredStates = dataGenerator(initialPosition, initialVelocity, deltaT, MatrixSize, whiteNoiseSTDev, stateTransition)
    
    # "measurementNoise" - dummy sample data of object staying still
    whiteNoise = whiteNoiseGenerator(whiteNoiseSTDev, MatrixSize)
    
    # "stateMatrix" - dummy sample data of object doing the thing it does
    randPosition = (random.randint(0,10), random.randint(0,10), random.randint(0,10))
    randVelocity = (random.randint(0,100), random.randin(50,100), random.randint(0,100))
    randProcess  = dataGenerator(randPosition, randVelocity, deltaT, MatrixSize, whiteNoiseSTDev, stateTransition)
    
    # process the data a bit
    staticPositionData     = dataProcessor(0, whiteNoise)
    staticVelocityData     = dataProcessor(1, whiteNoise)
    staticAccelerationData = dataProcessor(2, whiteNoise)
    
    movingPositionData     = dataProcessor(0, randProcess)
    movingVelocityData     = dataProcessor(1, randProcess)
    movingAccelerationData = dataProcessor(2, randProcess)
    
    # obtain measurementNoise, stateMatrix, processNoise
    Physics_Filter.setupKalmanFilterDEMO(staticPositionData, staticVelocityData, staticAccelerationData, movingPositionData, movingVelocityData, movingAccelerationData)
    
    for state in measuredStates:
        filteredData = Physics_Filter.KalmanFilterxvaDEMO(measuredStates, deltaT)
        
    cleanData = canonSimulator(initialPosition, initialVelocity, deltaT, MatrixSize, stateTransition)
    
    # real-ish
    realData = measuredStates
    
    # process data a little to plot
    realPosition     = dataProcessor(0, realData)
    realVelocity     = dataProcessor(1, realData)
    realAcceleration = dataProcessor(2, realData)
    
    filteredPosition     = dataProcessor(0, filteredData)
    filteredVelocity     = dataProcessor(1, filteredData)
    filteredAcceleration = dataProcessor(2, filteredData)
    
    cleanPosition     = dataProcessor(0, cleanData)
    cleanVelocity     = dataProcessor(1, cleanData)
    cleanAcceleration = dataProcessor(2, cleanData)

    T = numpy.arange(0, MatrixSize*deltaT, deltaT)
    
    # plot realData, filteredData, and cleanData
    # Position graphs
    plt.figure(1)
    plt.subplot(311)
    plt.plot(realPosition, T)
    plt.plot(filteredPosition, T)
    plt.plot(cleanPosition, T)
    plt.subplot(312)
    plt.plot(realVector, T)
    plt.plot(filteredVector, T)
    plt.plot(cleanVector, T)
    plt.subplot(313)
    plt.plot(realAcceleration, T)
    plt.plot(filteredAcceleration, T)
    plt.plot(cleanAcceleration, T)
    
    '''
    # process the data a bit more 
    realPositionx = dataProcessor(0, realPosition)
    realPositiony = dataProcessor(1, realPosition)
    realPositionz = dataProcessor(2, realPosition)
    
    realVelocityx = dataProcessor(0, realVelocity)
    realVelocityy = dataProcessor(1, realVelocity)
    realVelocityz = dataProcessor(2, realVelocity)
    
    realAccelerationx = dataProcessor(0, realAcceleration)
    realAccelerationy = dataProcessor(1, realAcceleration)
    realAccelerationz = dataProcessor(2, realAcceleration)
    
    # keep processing that data
    filteredPositionx = dataProcessor(0, filteredPosition)
    filteredPositiony = dataProcessor(1, filteredPosition)
    filteredPositionz = dataProcessor(2, filteredPosition)
    
    filteredVelocityx = dataProcessor(0, filteredVelocity)
    filteredVelocityy = dataProcessor(1, filteredVelocity)
    filteredVelocityz = dataProcessor(2, filteredVelocity)
    
    filteredAccelerationx = dataProcessor(0, filteredAcceleration)
    filteredAccelerationy = dataProcessor(1, filteredAcceleration)
    filteredAccelerationz = dataProcessor(2, filteredAcceleration)
    
    # almost done processing data
    cleanPositionx = dataProcessor(0, cleanPosition)
    cleanPositiony = dataProcessor(1, cleanPosition)
    cleanPositionz = dataProcessor(2, cleanPosition)
    
    cleanVelocityx = dataProcessor(0, cleanVelocity)
    cleanVelocityy = dataProcessor(1, cleanVelocity)
    cleanVelocityz = dataProcessor(2, cleanVelocity)
    
    cleanAccelerationx = dataProcessor(0, cleanAcceleration)
    cleanAccelerationy = dataProcessor(1, cleanAcceleration)
    cleanAccelerationz = dataProcessor(2, cleanAcceleration)
    
    T = numpy.arange(0, MatrixSize*deltaT, deltaT)
    
    # plot realData, filteredData, and cleanData
    # Position graphs
    plt.figure(1)
    plt.subplot(311)
    plt.plot(realPositionx, T)
    plt.plot(filteredPositionx, T)
    plt.plot(cleanPositionx, T)
    plt.subplot(312)
    plt.plot(realPositiony, T)
    plt.plot(filteredPositiony, T)
    plt.plot(cleanPositiony, T)
    plt.subplot(313)
    plt.plot(realPositionz, T)
    plt.plot(filteredPositionz, T)
    plt.plot(cleanPositionz, T)
    
    # Velocity graphs
    plt.figure(2)
    plt.subplot(311)
    plt.plot(realVelocityx, T)
    plt.plot(filteredVelocityx, T)
    plt.plot(cleanVelocityx, T)
    plt.subplot(312)
    plt.plot(realVelocityy, T)
    plt.plot(filteredVelocityy, T)
    plt.plot(cleanVelocityy, T)
    plt.subplot(313)
    plt.plot(realVelocityz, T)
    plt.plot(filteredVelocityz, T)
    plt.plot(cleanVelocityz, T)
    
    # Acceleration graphs
    plt.figure(3)
    plt.subplot(311)
    plt.plot(realAccelerationx, T)
    plt.plot(filteredAccelerationx, T)
    plt.plot(cleanAccelerationx, T)
    plt.subplot(312)
    plt.plot(realAccelerationy, T)
    plt.plot(filteredAccelerationy, T)
    plt.plot(cleanAccelerationz, T)
    plt.subplot(313)
    plt.plot(realAccelerationz, T)
    plt.plot(filteredAccelerationz, T)
    plt.plot(filteredAccelerationz, T)
    
    # A lot of repetitive stuff here, but too lazy to make look clean. Don't judge. I brute forced all the way. 
    '''
def dataProcessor(spot, array):
    
    data = [x[spot] for x in array]
    
    return data
                    
def whiteNoiseGenerator(std, matrixSize):
    
    return numpy.random.normal( (0,0,0), std, size=matrixSize )
    
    # The mean of white noise is theoretically 0
    
def canonSimulator(initialPos, initialVel, deltaT, matrixSize, stateTransition):
    
    measuredState       = numpy.zeros(matrixSize)
    gravity             = -9.98
    initialAcceleration = (0, gravity, 0)
    initialState        = [initialPos, initialVel, initialAcceleration]
    measuredState[0]    = initialState
    
    index = 0
    
    while index < matrixSize: 
        measuredState[index+1] = stateTransition*measuredState[index] 
        index += index
        
    return measuredState

def dataGenerator(initialPos, initialVel, deltaT, matrixSize, whiteNoiseSTD, stateTransition):
    
    whiteNoise           = whiteNoiseGenerator(whiteNoiseSTD, matrixSize)
    canonSimulation      = canonSimulator(initialPos, initialVel, deltaT, matrixSize, stateTransition)
    noisyCanonSimulation = canonSimulation + whiteNoise
    
    return noisyCanonSimulation

if __name__ == "__main__":
    main()
