#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy

# HOW TO USE IN main():

# DURING SETUP
# Prompt user to keep hand still, hovering over the Leap
# Poll for a bunch of frames and save as staticData
# Prompt user to finger spell over the leap
# Poll for a bunch of frames and save as movingData
# Process data a little for next function
# PhysicsFilter.setupKalmanFilter(staticPositionData, staticVelocityData, movingPositionData, movingVelocityData)

# DURING MAIN LOOP
# Poll for a bunch of frames, separate data into velocities and positions arrays, get time
# get initial state -averagePosition, averageVelocity, averageAcceleration, averageTime
# while hand is valid {
# Poll for another frame and process data
# Physics.KalmanFilter(measuredState, measuredTime) }
# Maybe resetStateMatrix() if we observe dispersion or whatever?

# NOTE: 
# Sprinkle some sort of external logic to handle NaN aka must have to get initial state after every NaN
# Data needs to be processed a little before using the filter aka organize as a proper state vector and timestamp

#TODO:
# - [ ] Figure out how to process a matrix within a matrix the way I want to
#
#       - EX: in  = [[[px,py,pz], [vx,vy,vz], [ax,ay,az]],
#                    [[px,py,pz], [vx,vy,vz], [ax,ay,az]],
#                    [[px,py,pz], [vx,vy,vz], [ax,ay,az]]]
#
#             out = [[px,py,pz],
#                    [vx,vy,vz],
#                    [ax,ay,az]]
#
#       - Lots of unit testing each step to verify that the more complicated matrices maths the way I want it to
# - [ ] Fine tune process noise matrix, EXTREMELY IMPORTANT
# - [/] Feed it data and plot to see if it works the way we want it to <--- Works for 1D but not 3D
#       - That's a half check mark
# - [/] Create code that organizes data into usable forms for the filter
#       - That is also another half check mark
# - [ ] Restructure to handle a crap ton of different positions and velocities of objects, maybe?
#       - Might be able to filter each object? However, that might be slower
#       - EX: KalmanFilter(object1), KalmanFilter(object2), KalmanFilter(object3), etc
# - [x] Create a demo for next presentation

class Physics_Filter:
    
    def __init__(self):
        self.processNoise = 0                                                # defined in setupKalmanFilter()
        self.measurementNoise = 0                                            # defined in setupKalmanFilter()
        self.initialStateMatrix = 0                                          # defined in setupKalmanFilter()
        self.priorStateMatrix = 0                                            # defined in setupKalmanFilter
        self.predictedStateMatrix = 0                                        # defined in predict()
        self.stateTransitionxv  = numpy.array(([1, self.deltaT], [0, 1]))
        self.stateTransitionxva = numpy.array(([1, self.deltaT, 0.25*self.deltaT**2], [0, 1, 0.5*self.deltaT], [0, 0, 0.5])) 
        self.priorState = 0                                                  # originally defined in getInitialState()
        self.predictedState = 0                                              # defined in predict()
        self.KalmanGain = 0                                                  # defined in update()
        self.timestamp = 0                                                   # originally defined in getInitialState()
        self.deltaT = 0                                                      # defined in KalmanFilter()
        
    # DESCRIPTION OF VARIABLES:
    
    # BACKGROUND INFORMATION -Covariance Matrices: processNoise, measurementNoise, priorStateMatrix, predictedStateMatrix
    
    # Derivation:
    #      [[ Covar(position, position    ), Covar(velocity, position    ), Covar(acceleration, position    )],
    #       [ Covar(position, velocity    ), Covar(velocity, velocity    ), Covar(acceleration, velocity    )],
    #       [ Covar(position, acceleration), Covar(velocity, acceleration), Covar(acceleration, acceleration)]]
    
    # This can be re-written as: 
    #      [[ std(position)*std(position    ), std(velocity)*std(position    ), std(acceleration)*std(position    )],
    #       [ std(position)*std(velocity    ), std(velocity)*std(position    ), std(acceleration)*std(velocity    )],
    #       [ std(position)*std(acceleration), std(velocity)*std(acceleration), std(acceleration)*std(acceleration)]]
    
    # However, we assume that the variance of one parameter isn't correlated with the variance of another parameter.
    # Therefore, we are left with this:
    #      [[ std(position)*std(position),     0,                               0                                  ],
    #       [ 0,                               std(velocity)*std(position),     0                                  ],
    #       [ 0,                               0,                               std(acceleration)*std(acceleration)]] 
    
    # This can be re-written as:
    #     [[ Var(position), 0,             0                 ],
    #      [ 0,             Var(velocity), 0                 ],
    #      [ 0,             0,             Var(acceleration) ]]    
    
    # PROCESS NOISE MATRIX - use random numbers to simulate white noise
    # processNoise
    # Q = [[ Var(randNum), 0,            0           ],
    #      [ 0,            Var(randNum), 0           ],
    #      [ 0,            0,            Var(randNum)]]
    
    # Translation of process noise covariance matrix Q:
    # We quantify our confidence in our model and also account of white noise.
    # Currently using variance of random numbers but will tweak depending on the validation of data
    # We also assume that the variance of one parameter isn't correlated with the variance of another parameter
    # THIS PARAMETER STAYS CONSTANT
    
    # MEASUREMENT NOISE MATRIX -use the variance while she keeps her hand still
    # measurementNoise
    # R = [[ Var(position), 0,             0                 ],
    #      [ 0,             Var(velocity), 0                 ],
    #      [ 0,             0,             Var(acceleration) ]]
    
    # Translation of measurement noise covariance matrix R:
    # We assume that the variance in our measurements as the user keeps her hand still is the variance in the sensor reading
    # We also assume that the variance of one parameter isn't correlated with the variance of another parameter
    # THIS PARAMETER STAYS CONSTANT
    
    # STATE COVARIANCE MATRIX -use the variance while she spells her name
    # initialStateMatrix, priorStateMatrix, predictedStateMatrix
    # P  = [[ Var(position), 0,             0                 ],
    #       [ 0,             Var(velocity), 0                 ],
    #       [ 0,             0,             Var(acceleration) ]]
    
    # Translation of  state covariance matrix P:
    # We assume that the variance of velocity doesn't correlate with variance of position or acceleration and other enumerations.
    # Position, velocity, and acceleration all have their own variances which we have measured previously.
    
    # priorStateMatrix gets updated after every iteration.
    # The Kalman Filter makes a prediction and then compares that prediction with the measurement.
    
    # STATE TRANSITION MATRIX -how we model the process and make a prediction
    # stateTransitionxva, stateTransitionxv
    
    # stateTransitionxva = [[1, deltaT, 0.25*deltaT^2],
    #                       [0, 1,      0.5*deltaT   ],
    #                       [0, 0,      0.5          ]]
    
    # Another translation of the maths above
    # priorState          stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT + 0.25*acceleration_(k-1)*deltaT^2
    # velocity_k        :                  velocity_(k-1)        + 0.5*acceleration_(k-1)*deltaT
    # acceleration_k    :                                          0.5*acceleration_(k-1)
    
    # In this model, we predict that acceleration decays with each predictive iteration.
    
    # stateTransitionxv = [[1, deltaT],
    #                      [0, 1     ]]
    
    # Another translation of the maths above
    # priorState          stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT
    # velocity_k        :                  velocity_(k-1)
    
    # In this model, we predict that velocity stays constant with each predictive iteration.
    
    # STATE VECTORS
    # priorState, predictedState
    
    # priorState = [[position    ],
    #               [velocity    ],
    #               [acceleration]]
    
    # predictedState = [[position    ],
    #                   [velocity    ],
    #                   [acceleration]]
    
    # Variables to store states for each iteration
    
    # KALMAN GAIN
    # KalmanGain
    
    # KalmanGain = priorStateMatrix*(priorStateMatrix + measurementNoise).I

    # KalmanGain determines how well we can trust our measurement.
    # If we have full confidence in our measurement, then the new state will be the measuredState
    # If we're unsure about our measurement, then the new state will be somewhere between measuredState and predictedState
    
    # OTHERS
    # timestamp, deltaT
    
    # Keeps track of time
    
    def setupKalmanFilterxva(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        staticAccelerationData = self.calcAcceleration(staticVelocityData)
        movingAccelerationData = self.calcAcceleration(movingVelocityData)
        
        self.measurementNoise   = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.initialStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        randomPosition = numpy.zeros((len(staticPositionData),3))
        
        index = 0
        while index < len(staticPositionData):
            randomPosition[index] = numpy.random.randint(min(staticPositionData[index]), max(staticPositionData[index]), len(staticPositionData))
            index = index+1
            
        randomVelocity = numpy.zeros((len(staticVelocityData),3))
        
        index = 0
        while index < len(staticVelocityData):
            randomVelocity[index] = numpy.random.randint(min(staticVelocityData[index]), max(staticVelocityData[index]), len(staticVelocityData))
            index = index+1
            
        randomAcceleration = numpy.zeros((len(staticAccelerationData)))
        
        index = 0
        while index < len(staticAccelerationData):
            randomAcceleration[index] = numpy.random.randint(min(staticAccelerationData[index]), max(staticAccelerationData[index]), len(staticAccelerationData))
            index = index+1
        
        self.processNoise = self.getCovarxva(randomPosition, randomVelocity, randomAcceleration)
        
    # Feed this function pre-collected data
    # Defines processNoise, measurementNoise, initialStateMatrix, priorStateMatrix
    
    def setupKalmanFilterxv(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        randomPosition = numpy.zeros((len(staticPositionData),3))
        
        index = 0
        while index < len(staticPositionData):
            randomPosition[index] = numpy.random.randint(min(staticPositionData[index]), max(staticPositionData[index]), size=(len(staticPositionData)))
            index = index+1
            
        randomVelocity = numpy.zeros((len(staticVelocityData),3))
        
        index = 0
        while index < len(staticVelocityData):
            randomVelocity[index] = numpy.random.randint(min(staticVelocityData[index]), max(staticVelocityData[index]), size=(len(staticVelocityData)))
        
        self.processNoise = self.getCovarxv(randomPosition, randomVelocity)
        
    # Feed this function pre-collected data
    # Defines processNoise, measurementNoise, initialStateMatrix, priorStateMatrix
    # Might make process noise a function of measurement noise
    
    def setupKalmanFilterDEMO(self, staticPositionData, staticVelocityData, staticAccelerationData, movingPositionData, movingVelocityData, movingAccelerationData):
        
        self.measurementNoise   = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.initialStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        randomPosition = numpy.zeros((len(staticPositionData),3))
        
        index = 0
        while index < len(staticPositionData):
            randomPosition[index] = numpy.random.randint(min(staticPositionData[index]), max(staticPositionData[index]), len(staticPositionData))
            index = index+1
            
        randomVelocity = numpy.zeros((len(staticVelocityData),3))
        
        index = 0
        while index < len(staticVelocityData):
            randomVelocity[index] = numpy.random.randint(min(staticVelocityData[index]), max(staticVelocityData[index]), len(staticVelocityData))
            index = index+1
            
        randomAcceleration = numpy.zeros((len(staticAccelerationData)))
        
        index = 0
        while index < len(staticAccelerationData):
            randomAcceleration[index] = numpy.random.randint(min(staticAccelerationData[index]), max(staticAccelerationData[index]), len(staticAccelerationData))
            index = index+1
        
        self.processNoise = self.getCovarxva(randomPosition, randomVelocity, randomAcceleration)
        
    # Essentially the same logic as the others, but specifically made for the demo
    # Might make process noise a function of measurement noise
    
    def getInitialState(self, positionData, velocityData, timestamp):
        
        accelerationData = self.calcAcceleration(velocityData)
        
        stateVectors = numpy.zeros(3,1,3)
        
        stateVectors[0] = numpy.average(positionData, axis=0)
        stateVectors[1] = numpy.average(velocityData, axis=0)
        stateVectors[2] = numpy.average(accelerationData, axis=0)
        
        self.timestamp = timestamp
        
        self.priorState = stateVectors
        
    # Filter needs to get a decent initial state value in order to be accurate
    # Therefore, Leap will need to poll for a few frames and estimate the state
    # Defines initial priorState
    
    def KalmanFilterxva(self, measuredState, measuredTime):
        
        self.getDeltaT(measuredTime)
        self.predictxva()
        
        priorState = self.update(measuredState)
        
        return priorState
    
    # Kalman Filter only does one iteration
    
    def KalmanFilterxv(self, measuredState, measuredTime):
        
        self.getDeltaT(measuredTime)
        self.predictxva()
        
        priorState = self.update(measuredState)
        
        return priorState
    
    # Kalman Filter only does one iteration
    
    def KalmanFilterxvaDEMO(self, measuredState, deltaT, stateTransition):
        
        self.deltaT = deltaT
        self.predictxvaDEMO(stateTransition)
        priorState  = self.update(measuredState)
        
        return priorState
    
    # Essentially the same logic as the others, but demo is a different model
    
    def predictxva(self):
        
        self.predictedState       = numpy.dot(self.stateTransitionxva,self.priorState)
        self.predictedStateMatrix = numpy.dot(self.stateTransitionxva,numpy.dot(self.priorStateMatrix,self.stateTransitionxva.T)) + self.processNoise
       
    def predictxv(self):
        
        self.predictedState       = numpy.dot(self.priorState,self.stateTransitionxv)
        self.predictedStateMatrix = numpy.dot(self.stateTransitionxv,numpy.dot(self.priorStateMatrix,self.stateTransitionxv.T)) + self.processNoise
    
    def predictxvaDEMO(self, stateTransition):
        
        self.stateTransition = stateTransition 
        self.predictedState  = numpy.dot(self.stateTransition,self.priorState)
        self.predictedMatrix = numpy.dot(self.stateTransition,numpy.dot(self.priorStateMatrix,self.stateTransition.T)) + self.processNoise
        
    # Essentially the same logic as the others, but demo is a different model
    
    def update(self, measuredState):
        
        self.KalmanGain       = numpy.dot(self.predictedStateMatrix,numpy.linalg.inv(self.predictedStateMatrix + self.measurementNoise))
        self.priorState       = self.predictedState + numpy.dot(self.KalmanGain,numpy.subtract(measuredState,self.predictedState))
        self.priorStateMatrix = numpy.subtract(self.predictedStateMatrix,numpy.dot(self.KalmanGain,self.predictedStateMatrix))
        
        return self.priorState

    def getDeltaTk(self, measuredTime):
        
        self.deltaT    = measuredTime - self.timestamp
        self.timestamp = measuredTime
        
    # Gets deltaT for one iteration
    
    def getDeltaT(self, timestampData):
                                                                       
        return [j-i for i,j in zip(timestampData[:-1],timestampData[1:])]       
        
    # Gets a deltaT array
    
    def getVar(self, dataset):
        
        return numpy.var(dataset,axis=0)
    
    def getCovarxva(self, positionData, velocityData, accelerationData):
        
        positionVar     = self.getVar(positionData)
        velocityVar     = self.getVar(velocityData)
        accelerationVar = self.getVar(accelerationData)
        
        covarMatrix = numpy.zeros((3,3,3))
        
        covarMatrix[0,0,:] = positionVar
        covarMatrix[1,1,:] = velocityVar
        covarMatrix[2,2,:] = accelerationVar
        
        return covarMatrix
    
    def getCovarxv(self, positionData, velocityData):
        
        positionVar = self.getVar(positionData)
        velocityVar = self.getVar(velocityData)
        
        covarMatrix = numpy.zeros((2,2,3))
        
        covarMatrix[0,0,:] = positionVar
        covarMatrix[1,1,:] = velocityVar
        
        return covarMatrix
    
    def calcAcceleration(self, velocityData):
            
        return [j-i for i,j in zip(velocityData[:-1],velocityData[1:])] 
    
    # Calculates acceleration if we'd like to go that route, but I'm unsure if I modelled it correctly
    # Calculates an acceleration array
    
    def calcAccelk(self, velocity):
        
        return velocity - self.priorState[1]
        
    # Calculates acceleration for one iteration
    
    def calcVelocity(self, positionData, deltaTData):
        
        velocityData = numpy.zeros((len(positionData)-1))
        
        while data < len(positionData)-1:
            velocityData[data] = (positionData[data+1] - positionData[data]) / deltaTData[data]
            data = data+1
            
        return velocityData
    
    # Calculates velocity, some of the data might not have this available
    # Calculates a velocity array
    
    def calcVelocityk(self, position, deltaT):
        
        return (position - self.priorState[0]) / deltaT
    
    # Calculates velocity for one iteration
    
    def conditionStateVector(self, stateVectors):
        
        return numpy.reshape(stateVectors, (len(stateVectors),1))
    
    # Makes sure that the stateVectors are in the correct form for matrix math
    
    def resetStateMatrix(self):
        
        self.priorStateMatrix = self.initialStateMatrix
        
    # Makes sure that the covariance matrix doesn't diverge
    # Might not be needed, depends on how well the system is modelled
    
    def setPalmOrigin(self, palm_position, positionData, palm_velocity, velocityData):
        
        for data in positionData:
            positionData[data] = positionData[data] - palm_position
            
        for data in velocityData:
            velocityData[data] = velocityData[data] - palm_velocity
            
        accelerationData = self.calcAcceleration(velocityData)
            
        return positionData, velocityData, accelerationData
    
    # Puts the hand's palm to the origin and removes any possible velocities associated with palm movement
    # Probably not important to set the palm to origin with this current logic
    
    def buildStateVectorxv(self, position, velocity):
        
        stateVector = numpy.zeros((2,1,3))
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
            
    def buildStateVectorxva(self, position, velocity):
        
        stateVector = numpy.zeros((3,1,3))
        
        acceleration = self.getAccelk(velocity)
        
        stateVector[0] = position
        stateVector[1] = velocity
        stateVector[2] = acceleration
        
        return stateVector
    
    def buildStateVectorxa(self, position, deltaT):
        
        stateVector = numpy.zeros((3,1,3))
        
        velocity     = self.getVelocityk(position, deltaT)
        acceleration = self.getAccelk(velocity)
        
        stateVector[0] = position
        stateVector[1] = velocity
        stateVector[2] = acceleration
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity and acceleration
    
    def buildStateVectorx(self, position, deltaT):
        
        stateVector = numpy.zeros((2,1,3))
        
        velocity = self.getVelocityk(position, deltaT)
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity
    