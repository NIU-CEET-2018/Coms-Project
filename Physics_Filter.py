#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import math

# DESCRIPTION: 
# How to use in main()
# During setup
# Prompt user to keep hand still hovering over the Leap
# Poll for a bunch of frames and save as staticData
# Prompt user to finger spell over the leap
# Poll for a bunch of frames and save as movingData
# Process data a little for next function
# PhysicsFilter.setupKalmanFilter(staticPositionData, staticVelocityData, movingPositionData, movingVelocityData)
# Poll for a bunch of frames, separate data into velocities and positions arrays, get time
# get initial state -averagePosition, averageVelocity, averageAcceleration, averageTime
# Poll for another frame and process data
# Physics.KalmanFilter(measuredState, measuredTime)
# Sprinkle some sort of external logic to handle NaN aka must have to get initial state after every NaN
# Data needs to be processed a little before using the filter aka organize as a proper state vector and timestamp

#TODO:
# - [ ] Fine tune process noise matrix
# - [ ] ask murray a lot of questions about python in general
# - [ ] fix possible syntax errors
# - [ ] clean up code
# - [ ] finish up Kalman Filter Implementation
# - [ ] feed it data and plot to see if it works the way we want it to
# - [ ] stop thinking in terms of C++

class PhysicsFilter:
    
    def __init__(self):
        self.processNoise                                                # defined in setupKalmanFilter()
        self.measurementNoise                                            # defined in setupKalmanFilter()
        self.stateTransitionxv = numpy.matrix('1, self.deltaT; 0, 1')
        self.stateTransitionxva = numpy.matrix('1, self.deltaT, 0.25*self.deltaT^2; 0, 1, 0.5*self.deltaT; 0, 0, 0.5') 
        self.priorState                                                  # originally defined in getInitialState()
        self.predictedState                                              # defined in predict()
        self.priorStateMatrix                                            # defined in setupKalmanFilter()
        self.predictedStateMatrix                                        # defined in predict()
        self.KalmanGain                                                  # defined in update()
        self.timestamp                                                   # originally defined in getInitialState()
        self.deltaT                                                      # defined in KalmanFilter()
        
    # Am I using this correctly? I want an organized space to access all the Kalman Variables
    # Also, I don't know how to use "self"
    
    def setupKalmanFilterxva(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        staticAccelerationData = self.calcAcceleration(staticVelocityData)
        movingAccelerationData = self.calcAcceleration(movingVelocityData)
        
        self.measurementNoise = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.priorStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        
        randomPosition = numpy.random.randint(min(staticPositionData), max(staticPositionData), len(staticPositionData))
        randomVelocity = numpy.random.randint(min(staticVelocityData), max(staticVelocityData), len(staticVelocityData))
        randomAcceleration = numpy.random.randint(min(staticAccelerationData), max(staticAccelerationData), len(staticAccelerationData))
        
        self.processNoise = self.getCovarxva(randomPosition, randomVelocity, randomAcceleration)
        
    # Feed this function pre-collected data
    # Assumes processNoise is essentially "white noise" which may or may not be good
    # Assumes stateMatrix is variance when user is finger spelling
    # Assumes measurementNoise is variance when user is keeping her hand still
    
    def setupKalmanFilterxv(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        self.measurementNoise = self.getCovarxv(staticPositionData, staticVelocityData)
        self.priorStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        
        randomPosition = numpy.random.randint(min(staticPositionData), max(staticPositionData), len(staticPositionData))
        randomVelocity = numpy.random.randint(min(staticVelocityData), max(staticVelocityData), len(staticVelocityData))
        
        self.processNoise = self.getCovarxv(randomPosition, randomVelocity)
        
    # Feed this function pre-collected data
    # Assumes processNoise is essentially "white noise" which may or may not be good
    # Assumes stateMatrix is variance when user is finger spelling
    # Assumes measurementNoise is variance when user is keeping her hand still
    
    def KalmanFilterxva(self, measuredState, measuredTime):
        
        self.deltaT = measuredTime - self.timestamp
        self.timestamp = measuredTime
        
        self.predictxva()
        priorState = self.update(measuredState)
        
        return priorState
    
    # Kalman Filter only does one iteration
    
    def KalmanFilterxv(self, measuredState, measuredTime):
        
        self.deltaT = measuredTime - self.timestamp
        self.timestamp = measuredTime
        
        self.predictxva()
        priorState = self.update(measuredState)
        
        return priorState
    
    def getVar(self, dataset):
        
        return math.sqrt(numpy.apply_over_axes(numpy.std,dataset))
    
    # Keep her hand as still as she can get -measurement variance
    # Get her to spell her name -initial state variance
    
    def getCovarxva(self, positionData, velocityData, accelerationData):
        
        positionVar = self.getVar(positionData)
        velocityVar = self.getVar(velocityData)
        accelerationVar = self.getVar(accelerationData)
        
        return numpy.diag([positionVar, velocityVar, accelerationVar])
    
    # STATE COVARIANCE MATRIX -use the variance while she spells her name
    # Po = [[ Covar(position, position),     Covar(velocity, position),     Covar(acceleration, position)    ],
    #       [ Covar(position, velocity),     Covar(velocity, velocity),     Covar(acceleration, velocity)    ],
    #       [ Covar(position, acceleration), Covar(velocity, acceleration), Covar(acceleration, acceleration)]]
    # OR
    # Po = [[ Var(position), 0,             0                 ],
    #       [ 0,             Var(velocity), 0                 ],
    #       [ 0,             0,             Var(acceleration) ]]
    
    # Translation of  state covariance matrix P:
    # We assume that the variance of velocity doesn't correlate with variance of position or acceleration and other enumerations.
    # Position, velocity, and acceleration all have their own variances which we have measured previously.
    
    # If we assume there's correlation between the variances:
    # Po = [[ std(position)*std(position,      std(velocity)*std(position),     std(acceleration)*std(position)    ],
    #       [ std(position)*std(velocity),     std(velocity)*std(position),     std(acceleration)*std(velocity)    ],
    #       [ std(position)*std(acceleration), std(velocity)*std(acceleration), std(acceleration)*std(acceleration)]]
    
    # MEASUREMENT NOISE MATRIX -use the variance while she keeps her hand still
    # R = [[ Var(position), 0,             0                 ],
    #      [ 0,             Var(velocity), 0                 ],
    #      [ 0,             0,             Var(acceleration) ]]
    
    # Translation of measurement noise covariance matrix R:
    # We assume that the variance in our measurements as the user keeps her hand still is the variance in the sensor reading
    # We also assume that the variance of one parameter isn't correlated with the variance of another parameter
    
    # PROCESS NOISE MATRIX
    # Q = [[ Var(randNum), 0,            0           ],
    #      [ 0,            Var(randNum), 0           ],
    #      [ 0,            0,            Var(randNum)]]
    
    # Translation of process noise covariance matrix Q:
    # We quantify our confidence in our model and also account of white noise.
    # Currently using variance of random numbers but will tweak depending on the validation of data
    
    def getCovarxv(self, positionData, velocityData):
        
        positionVar = self.getVar(positionData)
        velocityVar = self.getVar(velocityData)
        
        return numpy.diag([positionVar, velocityVar])
    
    def predictxva(self):
        
        self.predictedState = self.stateTransitionxva*self.priorState
        self.predictedStateMatrix = self.stateTransitionxva*self.priorStateMatrix*self.stateTransitionxva.T + self.processNoise
                    
    # Must order the priorState in position, velocity, acceleration for this model 
    # priorState = [[position],
    #               [velocity],
    #               [acceleration]]
    
    # stateTransition = [[1, deltaT, 0.25*deltaT^2],
    #                    [0,      1,   0.5*deltaT ],
    #                    [0,      0,        0.5   ]]
    
    # Another translation of the maths above
    # priorState          stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT + 0.25*acceleration_(k-1)*deltaT^2
    # velocity_k        :                  velocity_(k-1)        + 0.5*acceleration_(k-1)*deltaT
    # acceleration_k    :                                          0.5*acceleration_(k-1)
    
    # In this model, we predict that acceleration decays with each predictive iteration.
    
    # TODO: 
    # Make this code tuple friendly
    # We might have to initialize the stateTransition as this:
    # stateTransition = [[(1,1,1), (deltaT,deltaT,deltaT), (deltaT^2,deltaT^2,deltaT^2)],
    #                    [(0,0,0), (1,1,1),                (deltaT,deltaT,deltaT)      ],
    #                    [(0,0,0), (0,0,0),                (1,1,1)                     ]]
       
    def predictxv(self):
        
        self.predictedState = self.priorState*self.stateTransitionxv
        self.predictedStateMatrix = self.stateTransitionxv*self.priorStateMatrix*self.stateTransitionxv.T + self.processNoise
        
    # Must order the stateVector in position and velocity for this model
    # priorState = [[position],
    #               [velocity]]
    
    # stateTransition = [[1, deltaT],
    #                    [0, 1     ]]
    
    # Another translation of the maths above
    # priorState          stateTransition
    # position_k        : position_(k-1) + velocity_(k-1)*deltaT
    # velocity_k        :                  velocity_(k-1)
    
    # In this model, we predict that velocity stays constant with each predictive iteration.
    
    # TODO:
    # Make this code tuple friendly? It probably already is
    
    def update(self, measuredState):
        
        self.KalmanGain = self.priorStateMatrix*(self.priorStateMatrix + self.measurementNoise).I
        self.priorState = self.predictedState + self.KalmanGain*(measuredState - self.predictedState)
        self.priorStateMatrix = (1 - self.KalmanGain)*self.priorStateMatrix
        
        return self.priorState
                
    # KalmanGain determines how well we can trust our measurement.
    # If we have full confidence in our measurement, then the new state will be the measuredState
    # If we're unsure about our measurement, then the new state will be somewhere between measuredState and predictedState

    def setPalmOrigin(self, palm_position, positionData, palm_velocity, velocityData):
        
        for data in positionData:
            positionData[data] = data - palm_position
            
        for data in velocityData:
            velocityData[data] = data - palm_velocity
            
        return positionData, velocityData
    
    # Puts the hand's palm to the origin and removes any possible velocities associated with palm movement
    # Acceleration doesn't get affected 
    # Probably not important to set the palm to origin with this current logic
    
    def calcAcceleration(self, velocityData):
        
        accelerationData = numpy.zeros(len(velocityData)-1)
        
        for data in accelerationData:
            accelerationData[data] = velocityData[data+1] - velocityData[data]
            
        return accelerationData
    
    # Calculates acceleration if we'd like to go that route, but I'm unsure if I modelled it correctly
    
    def conditionStateVector(self, stateVectors):
        
        return numpy.reshape(stateVectors, (len(stateVectors),1))
    
    # Makes sure that the stateVectors are in the correct form for matrix math

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
    