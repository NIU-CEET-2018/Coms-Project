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
# Maybe resetStateMatrix() if we observe dispersion or whatever? Or you know, create a better state transition model

# NOTE: 
# Sprinkle some sort of external logic to handle NaN aka must have to get initial state after every NaN
# Data needs to be processed a little before using the filter aka organize as a proper state vector and timestamp

#TODO:
# - [x] Figure out how to process a matrix within a matrix the way I want to
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
# - [x] Feed it data and plot to see if it works the way we want it to 
# - [/] Create code that organizes data into usable forms for the filter
#       - That is also another half check mark as I'm not exactly sure how the incoming data is setup in detail
# - [ ] Restructure to handle a crap ton of different positions and velocities of objects, maybe?
#       - Might be able to filter each object? However, that might be slower
#       - EX: KalmanFilter(object1), KalmanFilter(object2), KalmanFilter(object3), etc
#       - Murray wants it to be this canonical form
#
#         [ palm position, 
#           palm angle (normal vec), 
#           each finger's angle of bend and angle of deviation from straight (wiggle waggle angle), 
#           the d/dt of each of those ] 
#
# - [x] Create a demo for next presentation
# - [ ] Learn more about class and subclass structures
#       - Specialized filters for the palm normal vector and the others as they may be modelled differently
#       - Each datapoint gets their own processNoise, measurementNoise, and other Kalman variables without overwriting others

# NOTE to SELF: How to model each hand part

# PALM POSITION
# - From data, extrapolate change in position / velocity
# - State Vectors will be position and velocity
# - Use stateTransitionxv as model
# stateTransitionxv = [[1, deltaT],
#                      [0, 1     ]]

# PALM NORMAL VECTOR
# - What assumptions can be made about the behavior of palm normal vector?
#   - State Vectors will most likely be NORMAL VECTOR and change in NORMAL VECTOR
#   - Dampen the change in NORMAL VECTOR as hand will generally be facing the leap sensor while signing
#     (There are only a handful of letters that it would impact a little)
#     - As long as the state transition model is semi close, it should filter ok
# - Use modified stateTransionxv as model with a decaying change in NORMAL VECTOR
# - stateTransitionxv = [[1, 0.5*deltaT],
#                        [0, 0.5       ]]

# FINGERS
# - What assumptions can be made about the behavior of the fingers?
#   - State Vectors will be bend angle and change in bend angle
#   - Assume that the d/dt remains the same and angle will change accordingly
#   - Use stateTransitionxv as model
# stateTransitionxv = [[1, deltaT],
#                      [0, 1     ]]

class Physics_Filter(object):
        
    def __init__(self):
        self.processNoise         = 0                                        # defined in setupKalmanFilter()
        self.measurementNoise     = 0                                        # defined in setupKalmanFilter()
        self.initialStateMatrix   = 0                                        # defined in setupKalmanFilter()
        self.priorStateMatrix     = 0                                        # defined in setupKalmanFilter
        self.predictedStateMatrix = 0                                        # defined in predict()
        self.deltaT               = 0                                        # defined in KalmanFilter()        
        self.stateTransitionxv    = numpy.array(([1, self.deltaT], [0, 1]))
        self.stateTransitionxva   = numpy.array(([1, self.deltaT, 0.25*self.deltaT**2], [0, 1, 0.5*self.deltaT], [0, 0, 0.5]))
        self.priorState           = 0                                        # originally defined in getInitialState()
        self.predictedState       = 0                                        # defined in predict()
        self.KalmanGain           = 0                                        # defined in update()
        self.timestamp            = 0                                        # originally defined in getInitialState()
        self.canonicalForm        = 0
        
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
    
    # canonicalForm
    # Organized list of the variables of interest
    #         [ palm position, 
    #           palm angle (normal vec), 
    #           each finger's angle of bend and angle of deviation from straight (wiggle waggle angle), 
    #           the d/dt of each of those ] 
    
    # OTHERS
    # timestamp, deltaT
    
    # Keeps track of time
    
    class FilteredHand(object):
        
        def __init__(self):
            self.palmPosition                = [0,0,0]
            self.palmDirection               = [0,0,0]
            self.pointerFingerDirection      = [0,0,0] 
            self.middleFingerDirection       = [0,0,0]
            self.ringFingerDirection         = [0,0,0]
            self.pinkyFingerDirection        = [0,0,0]
            self.thumbFingerDirection        = [0,0,0]
            self.pointerFingerDeltaDirection = [0,0,0]
            self.middleFingerDeltaDirection  = [0,0,0]
            self.ringFingerDeltaDirection    = [0,0,0]
            self.pinkyFingerDeltaDirection   = [0,0,0]
            self.thumbFingerDeltaDirection   = [0,0,0]
        
    # subclass of Physics_Filter to make putting variables into canonical form easier
    
    #################################################################################
    #                           super rough draft                                   #
    #################################################################################
    
    def setupKF(self, canonicalData):
        
        # process canonicalData
        # setupKalmanFilter for each datapoint
        # hopefully they don't overwrite each other
        
    def KalmanFilter(self, canonicalForm, measuredTime):
        
        # process canonicalForm
        # predict each datapoint
        # update each datapoint
        # hopefully they don't overwrite each other
        # canonicalize processed data
        
        return filteredCanonicalForm 
    
    def setupKalmanFilterxva(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        staticAccelerationData  = self.calcAcceleration(staticVelocityData)
        movingAccelerationData  = self.calcAcceleration(movingVelocityData)
        
        self.measurementNoise   = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.initialStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise
        
    # When position and velocity data is available and acceleration is extrapolated
    
    def setupKalmanFilterxv(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        
        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise
        
    # When position and velocity data is available
    
    def setupKalmanFilterxa(self, staticPositionData, movingPositionData, timestampData):
        
        deltaTData             = self.getDeltaT(timestampData)
        staticVelocityData     = self.calcVelocity(staticPositionData,deltaTData)
        movingVelocityData     = self.calcVelocity(movingvelocityData,deltaTData)
        staticAccelerationData = self.calcAcceleration(staticVelocityData)
        movingAccelerationData = self.calcAcceleration(movingAccelerationData)
        
        self.measurementNoise   = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.initialStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise
        
    # When only position and timestamp data is available, extrapolate velocity and acceleration
    
    def setupKalmanFilterx(self, staticPositionData, movingPositionData, timestampData):
        
        deltaTData         = self.getDeltaT(timestampData)
        staticVelocityData = self.calcVelocity(staticPositionData,deltaTData)
        movingVelocityData = self.calcVelocity(movingvelocityData,deltaTData)

        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise    
        
    # When only position and timestamp data is available, extrapolate velocity
    
    def setupKalmanFilterDEMO(self, staticPositionData, staticVelocityData, staticAccelerationData, movingPositionData, movingVelocityData, movingAccelerationData):
        
        self.measurementNoise   = self.getCovarxva(staticPositionData, staticVelocityData, staticAccelerationData)
        self.initialStateMatrix = self.getCovarxva(movingPositionData, movingVelocityData, movingAccelerationData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise
        
    # Essentially the same logic as the others, but specifically made for the demo
    
    def getInitialStatexva(self, positionData, velocityData, timestamp):
        
        accelerationData = self.calcAcceleration(velocityData)
        
        stateVectors = numpy.zeros((3,1,3))
        
        stateVectors[0] = numpy.average(positionData, axis=0)
        stateVectors[1] = numpy.average(velocityData, axis=0)
        stateVectors[2] = numpy.average(accelerationData, axis=0)
        
        self.timestamp = timestamp
        
        self.priorState = stateVectors
        
    # Filter needs to get a decent initial state value in order to be accurate
    # Therefore, Leap will need to poll for a few frames and estimate the state
    # Defines initial priorState
    # When position and velocity data is available, extrapolate acceleration
    
    def getInitialStatexv(self, positionData, velocityData, timestamp):
        
        stateVectors = numpy.zeros((2,1,3))
        
        stateVectors[0] = numpy.average(positionData, axis=0)
        stateVectors[1] = numpy.average(velocityData, axis=0)
        
        self.timestamp = timestamp
        
        self.priorState = stateVectors
        
    # When position and velocity data is available
    
    def getInitialStatexa(self, positionData, timestamp):
        
        deltaTData       = self.getDeltaT(timestamp)
        velocityData     = self.calcVelocity(positionData,deltaTData)
        accelerationData = self.calcAcceleration(velocityData,deltaTData)
        
        stateVectors = numpy.zeros((3,1,3))
        
        stateVectors[0] = numpy.average(positionData, axis=0)
        stateVectors[1] = numpy.average(velocityData, axis=0)
        stateVectors[2] = numpy.average(accelerationData, axis=0)
        
        self.timestamp = timestamp
        
        self.priorState = stateVectors
        
    # When only position and timestamp data is available, extrapolate velocity and acceleration
    
    def getInitialStatex(self, positionData, timestamp):
        
        deltaTData   = self.getDeltaT(timestamp)
        velocityData = self.calcVelocity(positionData,deltaTData)
        
        stateVectors = numpy.zeros((2,1,3))
        
        stateVectors[0] = numpy.average(positionData, axis=0)
        stateVectors[1] = numpy.average(velocityData, axis=0)
        
        self.timestamp = timestamp
        
        self.priorState = stateVectors
    
    def KalmanFilterxva(self, measuredState, measuredTime):
        
        self.timestamp = measuredTime
        self.deltaT    = self.getDeltaTk(measuredTime)
        self.predictxva()
        
        priorState = self.update(measuredState)
        
        return priorState
    
    # Kalman Filter only does one iteration
    
    def KalmanFilterxv(self, measuredState, measuredTime):
        
        self.timestamp = measuredTime
        self.deltaT    = self.getDeltaTk(measuredTime)
        self.predictxv()
        
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
        
        self.predictedState = numpy.zeros((3,3))
        
        index = 0
        while index < 3:
            self.predictedState[:,index] = numpy.dot(self.stateTransitionxva[:,:,index],self.priorState[:,index])
            index = index+1
        
        intermediateMatrix = self.priorStateMatrix
        
        index = 0
        while index < 3:
            intermediateMatrix[:,index] = numpy.dot(self.stateTransitionxva[:,:,index], self.priorStateMatrix[:, index])
            index = index+1

        self.predictedStateMatrix = self.priorStateMatrix
 
        index = 0
        while index < 3:
            self.predictedStateMatrix[:,index] = numpy.dot(intermediateMatrix[:,index], self.stateTransitionxva[:,:,index].T) + self.processNoise[:,index]
            index = index+1
       
    def predictxv(self):
        
        self.predictedState = numpy.zeros((3,3))
        
        index = 0
        while index < 3:
            self.predictedState[:,index] = numpy.dot(self.stateTransitionxv[:,:,index],self.priorState[:,index])
            index = index+1
        
        intermediateMatrix = self.priorStateMatrix
        
        index = 0
        while index < 3:
            intermediateMatrix[:,index] = numpy.dot(self.stateTransitionxv[:,:,index], self.priorStateMatrix[:, index])
            index = index+1

        self.predictedStateMatrix = self.priorStateMatrix
            
        index = 0
        while index < 3:
            self.predictedStateMatrix[:,index] = numpy.dot(intermediateMatrix[:,index], self.stateTransitionxv[:,:,index].T) + self.processNoise[:,index]
            index = index+1
    
    def predictxvaDEMO(self, stateTransition):
        
        self.stateTransition = stateTransition 

        self.predictedState = numpy.zeros((3,3))
        
        index = 0
        while index < 3:
            self.predictedState[:,index] = numpy.dot(self.stateTransition[:,:,index],self.priorState[:,index])
            index = index+1
            
        # predictedState = stateTransition dot priorState
        
        intermediateMatrix = self.priorStateMatrix
        
        index = 0
        while index < 3:
            intermediateMatrix[:,index] = numpy.dot(self.stateTransition[:,:,index], self.priorStateMatrix[:, index])
            index = index+1
            
        index = 0
        
        self.predictedStateMatrix = self.priorStateMatrix
        while index < 3:
            self.predictedStateMatrix[:,index] = numpy.dot(intermediateMatrix[:,index], self.stateTransition[:,:,index].T) + self.processNoise[:,index]
            index = index+1  
            
        # predictedStateMatrix = stateTransition dot priorStateMatrix dot stateTransition Transposed + processNoise
    
    def update(self, measuredState):
        
        scalingFactor = self.predictedStateMatrix+self.measurementNoise
        
        inv = scalingFactor

        index = 0

        while index < 3:
            inv[:,:,index] = numpy.linalg.inv(scalingFactor[:,:,index])
            index = index+1
        
        index = 0
        
        self.KalmanGain = self.predictedStateMatrix
        
        while index < 3:
            self.KalmanGain[:,:,index] = numpy.dot(self.predictedStateMatrix[:,:,index], inv[:,:,index])
            index = index+1
            
        index = 0
        
        # KalmanGain = predictedStateMatrix dot inverse of (predictedStateMatrix + measurementNoise)
        
        while index < 3:
            self.priorState[:,index] = self.predictedState[:,index] + numpy.dot(self.KalmanGain[:,:,index],numpy.subtract(measuredState[:,index],self.predictedState[:,index]))
            index = index+1
            
        # priorState = predictedState + KalmanGain dot (measuredState - predictedState)
        
        intermediateArray = self.KalmanGain
        
        index = 0
        
        while index < 3:
            intermediateArray[:,:,index] = numpy.dot(self.KalmanGain[:,:,index], self.predictedStateMatrix[:,:,index])
            index = index+1
            
        self.priorStateMatrix = numpy.subtract(self.predictedStateMatrix,intermediateArray)
        
        # priorStateMatrix = predictedStateMatrix - (KalmanGain dot predictedStateMatrix)
        
        return self.priorState 

    def getDeltaTk(self, measuredTime):
        
        self.deltaT    = measuredTime - self.timestamp
        self.timestamp = measuredTime
        
    # Gets deltaT for one iteration
    
    def getDeltaT(self, timestampData):
                                                                       
        return numpy.diff(timestampData)      
        
    # Gets a deltaT array
    
    def getVar(self, dataset):
        
        return numpy.var(dataset,axis=0)
    
    def getCovarxva(self, positionData, velocityData, accelerationData):
        
        covarMatrix = numpy.zeros((3,3,3))
        
        covarMatrix[0,0,:] = self.getVar(positionData)
        covarMatrix[1,1,:] = self.getVar(velocityData)
        covarMatrix[2,2,:] = self.getVar(accelerationData)
        
        return covarMatrix
    
    def getCovarxv(self, positionData, velocityData):
        
        covarMatrix = numpy.zeros((2,2,3))
        
        covarMatrix[0,0,:] = self.getVar(positionData)
        covarMatrix[1,1,:] = self.getVar(velocityData)
        
        return covarMatrix
    
    def calcAcceleration(self, velocityData):
            
        return numpy.diff(velocityData, axis=0) 
    
    # Calculates acceleration if we'd like to go that route, but I'm unsure if I modelled it correctly
    # Calculates an acceleration array
    
    def calcAccelk(self, velocity):
        
        return velocity - self.priorState[1]
        
    # Calculates acceleration for one iteration
    
    def calcVelocity(self, positionData, deltaTData):
        
        return numpy.diff(positionData, axis=0) / deltaTData
    
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
    
    def buildStateVectorxv(self, position, velocity):
        
        stateVector = numpy.zeros((2,1,3))
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
            
    def buildStateVectorxva(self, position, velocity):
        
        stateVector = numpy.zeros((3,1,3))

        stateVector[0] = position
        stateVector[1] = velocity
        stateVector[2] = self.getAccelk(velocity)
        
        return stateVector
    
    # For data that has position and velocity and extrapolates acceleration
    
    def buildStateVectorxa(self, position, deltaT):
        
        stateVector = numpy.zeros((3,1,3))

        stateVector[0] = position
        stateVector[1] = self.getVelocityk(position, deltaT)
        stateVector[2] = self.getAccelk(velocity)
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity and acceleration
    
    def buildStateVectorx(self, position, deltaT):
        
        stateVector = numpy.zeros((2,1,3))
        
        velocity = self.getVelocityk(position, deltaT)
        
        stateVector[0] = position
        stateVector[1] = velocity
        
        return stateVector
    
    # For data that only contains position and extrapolates velocity
    
    def dataProcessor(self, spot, array):
        
        return [x[spot] for x in array]
            
    # Separates the state vectors into their respective position, velocity, and acceleration
    # OR separates the (x,y,z) components 
    
    def deTuplizer(self, list_of_tups):
        
        return [list(tup) for tup in list_of_tups]
    
    # turns a list of tuples into a list of lists
    
    def deTuplizerk(self, tup):
        
        return list(tup)
    
    # turns a tup into a list
    
    def canonicalize(self, self.FilteredHand):
        
        numData = 12
        
        canonicalForm = numpy.zeros((numData, 3))
        
        canonicalForm[0] = self.FilteredHand.palmPosition
        canonicalForm[1] = self.FilteredHand.palmDirection
        canonicalForm[2] = self.FilteredHand.pointerFingerDirection
        canonicalForm[3] = self.FilteredHand.middleFingerDirection
        canonicalForm[4] = self.FilteredHand.ringFingerDirection
        canonicalForm[5] = self.FilteredHand.pinkyFingerDirection
        canonicalForm[6] = self.FilteredHand.thumbFingerDirection
        canonicalForm[7] = self.FilteredHand.pointerFingerDeltaDirection
        canonicalForm[8] = self.FilteredHand.middleFingerDeltaDirection
        canonicalForm[9] = self.FilteredHand.ringFingerDeltaDirection
        canonicalForm[10] = self.FilteredHand.pinkyFingerDeltaDirection
        canonicalForm[11] = self.FilteredHand.thumbFingerDeltaDirection
        
        return canonicalForm
    
    # returns all the hand variables in canonical form.
    # is this how I call a subclass within a class? I might need to organize it differently.
    