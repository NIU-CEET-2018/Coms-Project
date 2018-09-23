#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import math

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
# - [ ] Fine tune process noise matrix, EXTREMELY IMPORTANT
# - [ ] Feed it data and plot to see if it works the way we want it to
# - [ ] Create code that organizes data into usable forms for the filter
# - [ ] Restructure to handle a crap ton of different positions and velocities of objects, maybe?
#       - Might be able to filter each object? However, that might be slower
#       - EX: KalmanFilter(object1), KalmanFilter(object2), KalmanFilter(object3), etc
# - [ ] Create a demo for next presentation

class PhysicsFilter:
    
    def __init__(self):
        self.processNoise                                                # defined in setupKalmanFilter()
        self.measurementNoise                                            # defined in setupKalmanFilter()
        self.initialStateMatrix                                          # defined in setupKalmanFilter()
        self.priorStateMatrix                                            # defined in setupKalmanFilter
        self.predictedStateMatrix                                        # defined in predict()
        self.stateTransitionxv = numpy.matrix('1, self.deltaT; 0, 1')
        self.stateTransitionxva = numpy.matrix('1, self.deltaT, 0.25*self.deltaT^2; 0, 1, 0.5*self.deltaT; 0, 0, 0.5') 
        self.priorState                                                  # originally defined in getInitialState()
        self.predictedState                                              # defined in predict()
        self.KalmanGain                                                  # defined in update()
        self.timestamp                                                   # originally defined in getInitialState()
        self.deltaT                                                      # defined in KalmanFilter()
        
    # DESCRIPTION OF VARIABLES:
    
    # BACKGROUND INFORMATION -Covariance Matrices: processNoise, measurementNoise, priorStateMatrix, predictedStateMatrix
    
    # Derivation:
    #      [[ Covar(position, position),     Covar(velocity, position),     Covar(acceleration, position)    ],
    #       [ Covar(position, velocity),     Covar(velocity, velocity),     Covar(acceleration, velocity)    ],
    #       [ Covar(position, acceleration), Covar(velocity, acceleration), Covar(acceleration, acceleration)]]
    
    # This can be re-written as: 
    #      [[ std(position)*std(position),     std(velocity)*std(position),     std(acceleration)*std(position)    ],
    #       [ std(position)*std(velocity),     std(velocity)*std(position),     std(acceleration)*std(velocity)    ],
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
    #                       [0,      1,   0.5*deltaT ],
    #                       [0,      0,        0.5   ]]
    
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
        
        randomPosition     = numpy.random.randint(min(staticPositionData), max(staticPositionData), len(staticPositionData))
        randomVelocity     = numpy.random.randint(min(staticVelocityData), max(staticVelocityData), len(staticVelocityData))
        randomAcceleration = numpy.random.randint(min(staticAccelerationData), max(staticAccelerationData), len(staticAccelerationData))
        
        self.processNoise = self.getCovarxva(randomPosition, randomVelocity, randomAcceleration)
        
    # Feed this function pre-collected data
    # Defines processNoise, measurementNoise, initialStateMatrix, priorStateMatrix
    
    def setupKalmanFilterxv(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        self.measurementNoise = self.getCovarxv(staticPositionData, staticVelocityData)
        self.priorStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        
        randomPosition = numpy.random.randint(min(staticPositionData), max(staticPositionData), len(staticPositionData))
        randomVelocity = numpy.random.randint(min(staticVelocityData), max(staticVelocityData), len(staticVelocityData))
        
        self.processNoise = self.getCovarxv(randomPosition, randomVelocity)
        
    # Feed this function pre-collected data
    # Defines processNoise, measurementNoise, initialStateMatrix, priorStateMatrix
    
    def getInitialState(self, positionData, velocityData, timestamp):
        
        accelerationData = self.calcAcceleration(velocityData)
        
        stateVectors = numpy.zeros(3,1)
        
        stateVectors[0] = numpy.average(positionData)
        stateVectors[1] = numpy.average(velocityData)
        stateVectors[2] = numpy.average(accelerationData)
        
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
    
    def getDeltaT(self, measuredTime):
        
        self.deltaT    = measuredTime - self.timestamp
        self.timestamp = measuredTime
    
    def predictxva(self):
        
        self.predictedState       = self.stateTransitionxva*self.priorState
        self.predictedStateMatrix = self.stateTransitionxva*self.priorStateMatrix*self.stateTransitionxva.T + self.processNoise
                    
    # TODO: 
    # Make this code tuple friendly, but might not be necessary because python magic
    # We might have to initialize the stateTransition as this:
    # stateTransition = [[(1,1,1), (deltaT,deltaT,deltaT), (0.25*deltaT^2,0.25*deltaT^2,0.25*deltaT^2)],
    #                    [(0,0,0), (1,1,1),                (0.5*deltaT,0.5*deltaT,0.5*deltaT)         ],
    #                    [(0,0,0), (0,0,0),                (0.5,0.5,0.5)                              ]]
       
    def predictxv(self):
        
        self.predictedState       = self.priorState*self.stateTransitionxv
        self.predictedStateMatrix = self.stateTransitionxv*self.priorStateMatrix*self.stateTransitionxv.T + self.processNoise
        
    # TODO:
    # Make this code tuple friendly
    
    def update(self, measuredState):
        
        self.KalmanGain       = self.predictedStateMatrix*(self.predictedStateMatrix + self.measurementNoise).I
        self.priorState       = self.predictedState + self.KalmanGain*(measuredState - self.predictedState)
        self.priorStateMatrix = self.predictedStateMatrix - self.KalmanGain*self.predictedStateMatrix
        
        return self.priorState
    
    def getVar(self, dataset):
        
        return math.sqrt(numpy.apply_over_axes(numpy.std,dataset))
    
    def getCovarxva(self, positionData, velocityData, accelerationData):
        
        positionVar     = self.getVar(positionData)
        velocityVar     = self.getVar(velocityData)
        accelerationVar = self.getVar(accelerationData)
        
        return numpy.diag([positionVar, velocityVar, accelerationVar])
    
    def getCovarxv(self, positionData, velocityData):
        
        positionVar = self.getVar(positionData)
        velocityVar = self.getVar(velocityData)
        
        return numpy.diag([positionVar, velocityVar])
    
    def calcAcceleration(self, velocityData):
        
        accelerationData = numpy.zeros(len(velocityData)-1)
        
        for data in accelerationData:
            accelerationData[data] = velocityData[data+1] - velocityData[data]
            
        return accelerationData
    
    # Calculates acceleration if we'd like to go that route, but I'm unsure if I modelled it correctly
    
    def calcAccelk(self, velocity):
        
        return velocity - self.priorState[1]
        
    # Calculates acceleration for one iteration
    
    def calcVelocity(self, positionData):
        
        velocityData = numpy.zeros(len(positionData)-1)
        
        for data in velocityData:
            velocityData[data] = positionData[data+1] - positionData[data]
            
        return velocityData
    
    # Calculates velocity, some of the data might not have this available
    
    def calcVelocityk(self, position):
        
        return position - self.priorState[0]
    
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
            positionData[data] = data - palm_position
            
        for data in velocityData:
            velocityData[data] = data - palm_velocity
            
        return positionData, velocityData
    
    # Puts the hand's palm to the origin and removes any possible velocities associated with palm movement
    # Acceleration doesn't get affected 
    # Probably not important to set the palm to origin with this current logic
    
    def buildStateVectorxv(self, position, velocity):
        
        stateVector = numpy.zeros(2,1)
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
            
    def buildStateVectorxva(self, position, velocity):
        
        stateVector = numpy.zeros(3,1)
        
        acceleration = self.getAccelk(velocity)
        
        stateVector[0] = position
        stateVector[1] = velocity
        stateVector[2] = acceleration
        
        return stateVector
    
    def buildStateVectorxa(self, position):
        
        stateVector = numpy.zeros(3,1)
        
        velocity     = self.getVelocityk(position)
        acceleration = self.getAccelk(velocity)
        
        stateVector[0] = position
        stateVector[1] = velocity
        stateVector[2] = acceleration
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity and acceleration
    
    def buildStateVectorx(self, position):
        
        stateVector = numpy.zeros(3,1)
        
        velocity = self.getVelocityk(position)
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity