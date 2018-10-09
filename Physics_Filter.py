#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import pandas

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
# - [ ] Fine tune process noise matrix, EXTREMELY IMPORTANT
# - [/] Feed it data and plot to see if it works the way we want it to
#       - Use Andrew's hand data by this weekend
# - [ ] Test newly added code by this weekend
# - [ ] Delete junk code 

# NOTE to SELF: How to model each hand part

# PALM POSITION and VELOCITY
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

# LIST OF DATA (AND ORDER) FROM ANDREW'S HAND:                    POTENTIAL STATE VECTORS
# Palm Normal x,        Palm Normal y,        Palm Normal z       <- Palm Normal Vector (extrapolate change in Normal Vector)
# Palm Direction x,     Palm Direction y,     Palm Direction z    <- ?
# Palm Center x,        Palm Center y,        Palm Center z       <- Palm Position, pair together with velocity in filter
# Palm Velocity x,      Palm Velocity y,      Palm Velocity z     <- Palm Velocity, pair together with position in filter
# Thumb Deviation 1,    Thumb Deviation 2,    Thumb Deviation 3   <- ?
# Thumb Joint Angle 1,  Thumb Joint Angle 2                       <- Joint angles, extrapolate change in angle
# Index Deviation 1,    Index Deviation 2,    Index Deviation 3
# Index Joint Angle 1,  Index Joint Angle 2                       <- Joint angles, extrapolate change in angle
# Middle Deviation 1,   Middle Deviation 2,   Middle Deviation 3
# Middle Joint Angle 1, Middle Joint Angle 2                      <- Joint angles, extrapolate change in angle
# Ring Deviation 1,     Ring Deviation 2,     Ring Deviation 3
# Ring Joint Angle 1,   Ring Joint Angle 2                        <- Joint angles, extrapolate change in angle
# Pinky Deviation 1,    Pinky Deviation 2,    Pinky Deviation 3
# Pinky Joint Angle 1,  Pinky Joint Angle 2                       <- Joint angles, extrapolate change in angle
# Time Stamp                                                      <- Extrapolate DeltaT

# palmNormal       - 3D
# palmDirection    - 3D
# palmPosition     - 3D
# palmVelocity     - 3D
# thumbDeviation   - 3D
# thumbJoint       - 2D
# pointerDeviation - 3D
# pointerJoint     - 2D
# middleDeviation  - 3D
# middleJoint      - 2D
# ringDeviation    - 3D
# ringJoint        - 2D
# pinkyDeviation   - 3D
# pinkyJoint       - 2D

# NOTE:
# Palm stuff uses 3D components, and the some of the joint angles uses only 2D components
# Palm stuff can be evaluated off the bat fairly easily, but there will need to be some modifications to handle joint angles

class Physics_Filter(object):

    handParts = ["palmXVKF", "palmDirKF", "palmNormKF", "pointerDevKF", "middleDevKF", "ringDevKF", "pinkyDevKF", "thumbDevKF", "pointerJointKF", "middleJointKF", "ringJointKF", "pinkyJointKF", "thumbJointKF"]
    
    def __init__(self,name):
        self.name                 = name                                     # create 13 instances for 
        self.processNoise         = 0                                        # defined in setupKalmanFilter()
        self.measurementNoise     = 0                                        # defined in setupKalmanFilter()
        self.initialStateMatrix   = 0                                        # defined in setupKalmanFilter()
        self.priorStateMatrix     = 0                                        # defined in setupKalmanFilter
        self.predictedStateMatrix = 0                                        # defined in predict()
        self.deltaT               = 0                                        # defined in KalmanFilter()        
        self.stateTransitionxv    = numpy.array(([1, self.deltaT], [0, 1]))
        self.stateTransitionxva   = numpy.array(([1, self.deltaT, 0.25*self.deltaT**2], [0, 1, 0.5*self.deltaT], [0, 0, 0.5]))
        self.stateTransition      = numpy.array(([1, 0.5*self.deltaT], [0, 0.5]))
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
    
    #################################################################################
    #                           super rough draft                                   #
    #################################################################################
    
    def initializeHand(self):
        
        for part in Handparts:
            Handparts[part] = Physics_Filter(Handparts[part])
            
    # Initializes all the parts of the hand for the filter
    
    def setupKF(self, staticAbsoluteFilePath, movingAbsoluteFilePath):
        
        staticCanonicalData = self.dataSorter(staticAbsoluteFilePath)
        movingCanonicalData = self.dataSorter(movingAbsoluteFilePath)
                
        # process canonicalData
        staticPalmPositionData  = staticCanonicalData[0]
        staticPalmVelocityData  = staticCanonicalData[1]
        staticPalmDirectionData = staticCanonicalData[2]
        staticPalmNormData      = staticCanonicalData[3]
        staticPointerDevData    = staticCanonicalData[4]
        staticMiddleDevData     = staticCanonicalData[5]
        staticRingDevData       = staticCanonicalData[6]
        staticPinkyDevData      = staticCanonicalData[7]
        staticThumbDevData      = staticCanonicalData[8]
        staticPointerJointData  = staticCanonicalData[9]
        staticMiddleJointData   = staticCanonicalData[10]
        staticRingJointData     = staticCanonicalData[11]
        staticPinkyJointData    = staticCanonicalData[12]
        staticThumbJointData    = staticCanonicalData[13]
        staticTimestampData     = staticCanonicalData[14]
        
        movingPalmPosition      = movingCanonicalData[0]
        movingPalmVelocityData  = movingCanonicalData[1]
        movingPalmDirectionData = movingCanonicalData[2]
        movingPalmNormData      = movingCanonicalData[3]
        movingPointerDevData    = movingCanonicalData[4]
        movingMiddleDevData     = movingCanonicalData[5]
        movingRingDevData       = movingCanonicalData[6]
        movingPinkyDevData      = movingCanonicalData[7]
        movingThumbDevData      = movingCanonicalData[8]
        movingPointerJointData  = movingCanonicalData[9]
        movingMiddleJointData   = movingCanonicalData[10]
        movingRingJointData     = movingCanonicalData[11]
        movingPinkyJointData    = movingCanonicalData[12]
        movingThumbJointData    = movingCanonicalData[13]
        movingTimestampData     = movingCanonicalData[14]
                
        #   - get deltaT
        staticDeltaTData = getDeltaT(staticTimestampData)
        movingDeltaTData = getDeletaT(movingTimestampData)

        # setupKalmanFilter for each handPart
        handPart[0].setupKalmanFilterxv(staticPalmPositionData, staticPalmVelocityData,  movingPalmPositionData, movingPalmVelocityData)
        handPart[1].setupKalmanFilterx(staticPalmDirectionData, movingPalmDirectionData, staticDeltaTData,       movingDeltaTData) 
        handPart[2].setupKalmanFilterx(staticPalmNormData,      movingPalmNormData,      staticDeltaTData,       movingDeltaTData) 
        handPart[3].setupKalmanFilterx(staticPointerDevData,    movingPointerDevData,    staticDeltaTData,       movingDeltaTData)
        handPart[4].setupKalmanFilterx(staticMiddleDevData,     movingMiddleDevData,     staticDeltaTData,       movingDeltaTData)
        handPart[5].setupKalmanFilterx(staticRingDevData,       movingRingDevData,       staticDeltaTData,       movingDeltaTData)
        handPart[6].setupKalmanFilterx(staticPinkyDevData,      movingPinkyDevData,      staticDeltaTData,       movingDeltaTData)
        handPart[7].setupKalmanFilterx(staticThumbDevData,      movingThumbDevData,      staticDeltaTData,       movingDeltaTData)
        handPart[8].setupKalmanFilterx(staticPointerJointData,  movingPointerJointData,  staticDeltaTData,       movingDeltaTData)
        handPart[9].setupKalmanFilterx(staticMiddleJointData,   movingMiddleJointData,   staticDeltaTData,       movingDeltaTData)
        handPart[10].setupKalmanFilterx(staticRingJointData,    movingRingJointData,     staticDeltaTData,       movingDeltaTData)
        handPart[11].setupKalmanFilterx(staticPinkyJointData,   movingPinkyJointData,    staticDeltaTData,       movingDeltaTData)
        handPart[12].setupKalmanFilterx(staticThumbJointData,   movingThumbJointData,    staticDeltaTData,       movingDeltaTData)
        
        # TODO:
        # - [ ] Probably organize this much nicer to look less messy
        # - [ ] Joint data only has 2 components, modify code a little
        
        # NOTE:
        # This was also brute forced.
        # It doesn't return anything as it's saved as variables in each of the handPart's Physics_Filter instance 
        
    def KalmanFilter(self, canonicalForm):

        measuredTime = canonicalForm[14]
        
        for part in handPart:
            handPart.getDeltaTk(measuredTime)
        
        # process canonicalForm
        palmxvMeasuredState       = [canonicalForm[0],  canonicalForm[1]]
        palmDirMeasuredState      = [canonicalForm[2],  handPart[1].calcVelocityk(canonicalForm[2],   handPart[1].deltaT)]
        palmNormMeasuredState     = [canonicalForm[3],  handPart[2].calcVelocityk(canonicalForm[3],   handPart[2].deltaT)]
        pointerDevMeasuredState   = [canonicalForm[4],  handPart[3].calcVelocityk(canonicalForm[4],   handPart[3].deltaT)]
        middleDevMeasuredState    = [canonicalForm[5],  handPart[4].calcVelocityk(canonicalForm[5],   handPart[4].deltaT)]
        ringDevMeasuredState      = [canonicalForm[6],  handPart[5].calcVelocityk(canonicalForm[6],   handPart[5].deltaT)]
        pinkyDevMeasuredState     = [canonicalForm[7],  handPart[6].calcVelocityk(canonicalForm[7],   handPart[6].deltaT)]
        thumbDevMeasuredState     = [canonicalForm[8],  handPart[7].calcVelocityk(canonicalForm[8],   handPart[7].deltaT)]
        pointerJointMeasuredState = [canonicalForm[9],  handPart[8].calcVelocityk(canonicalForm[9],   handPart[8].deltaT)]
        middleJointMeasuredState  = [canonicalForm[10], handPart[9].calcVelocityk(canonicalForm[10],  handPart[9].deltaT)]
        ringJointMeasuredState    = [canonicalForm[11], handPart[10].calcVelocityk(canonicalForm[11], handPart[10].deltaT)]
        pinkyJointMeasuredState   = [canonicalForm[12], handPart[11].calcVelocityk(canonicalForm[12], handPart[11].deltaT)]
        thumbJointMeasuredState   = [canonicalForm[13], handPart[12].calcVelocityk(canonicalForm[13], handPart[12].deltaT)]
        
        # predict each datapoint
        handPart[0].predictxv() #palmxv
        handPart[1].predict() #palmDir 
        handPart[2].predict() #palmNorm 
        handPart[3].predictx() #pointerDev
        handPart[4].predictx() #middleDev
        handPart[5].predictx() #ringDev
        handPart[6].predictx() #pinkyDev
        handPart[7].predictx() #thumbDev
        handPart[8].predictx() #pointerJoint
        handPart[9].predictx() #middleJoint
        handPart[10].predictx() #ringJoint
        handPart[11].predictx() #pinkyJoint
        handPart[12].predictx() #thumbJoint
        
        # update each datapoint
        handPart[0].update(palmxvMeasuredState)
        handPart[1].update(palmDirMeasuredState)
        handPart[2].update(palmNormMeasuredState)
        handPart[3].update(pointerDevMeasuredState)
        handPart[4].update(middleDevMeasuredState)
        handPart[5].update(ringDevMeasuredState)
        handPart[6].update(pinkyDevMeasuredState)
        handPart[7].update(thumbDevMeasuredState)
        handPart[8].update(pointerJointMeasuredState)
        handPart[9].update(middleJointMeasuredState)
        handPart[10].update(ringJointMeasuredState)
        handPart[11].update(pinkyJointMeasuredState)
        handPart[12].update(thumbJointMeasuredState)
        
        # canonicalize processed data
        palmPosition  = handPart[0].priorState[0]
        palmVelocity  = handPart[0].priorState[1]
        palmDirection = handPart[1].priorState[0]
        palmNormal    = handPart[2].priorState[0]
        pointerDev    = handPart[3].priorState[0]
        middleDev     = handPart[4].priorState[0]
        ringDev       = handPart[5].priorState[0]
        pinkyDev      = handPart[6].priorState[0]
        thumbDev      = handPart[7].priorState[0]
        pointerJoint  = handPart[8].priorState[0]
        middleJoint   = handPart[9].priorState[0]
        ringJoint     = handPart[10].priorState[0]
        pinkyJoint    = handPart[11].priorState[0]
        thumbJoint    = handPart[12].priorState[0]
        
        filteredCanonicalForm = [palmPosition, palmVelocity, palmDirection, palmNormal, pointerDev, middleDev, ringDev, pinkyDev, thumbDev, pointerJoint, middleJoint, ringJoint, pinkyJoint, thumbJoint, measuredTime]
        
        return filteredCanonicalForm 
    
    # TODO:
    # - [ ] Make sure the components are correct
    # - [ ] Find a way to make this shorter and cleaner looking
    
    # NOTE:
    # I also brute forced this one. I'll test and modify over the weekend.
    
    #################################################################################
    #                             end rough draft                                   #
    #################################################################################
    
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
    # Use for palm position and velocity
    
    def setupKalmanFilterx(self, staticPositionData, movingPositionData, staticTimestampData, movingTimestampData):
        
        staticDeltaTData       = self.getDeltaT(staticTimestampData)
        movingDeltaTData       = self.getDeltaT(movingTimestampData)
        staticVelocityData     = self.calcVelocity(staticPositionData,staticDeltaTData)
        movingVelocityData     = self.calcVelocity(movingPositionData,movingDeltaTData)

        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix
        
        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise    
        
    # When only position and timestamp data is available, extrapolate velocity
    # Use for finger joints
    
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
    
    def getInitialStatex(self, positionData, timestampData):
        
        deltaTData   = self.getDeltaT(timestampData)
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
    # Use for palm position and velocity
    
    def KalmanFilterxv(self, measuredState, measuredTime):
        
        self.timestamp = measuredTime
        self.deltaT    = self.getDeltaTk(measuredTime)
        self.predictxv()
        
        priorState = self.update(measuredState)
        
        return priorState
    
    # Kalman Filter only does one iteration
    # Use for palm normal vector
    
    def KalmanFilterxvaDEMO(self, measuredState, deltaT, stateTransition):
        
        self.deltaT = deltaT
        self.predictxvaDEMO(stateTransition)
        priorState  = self.update(measuredState)
        
        return priorState
    
    # Essentially the same logic as the others, but demo is a different model
       
    def predictxv(self):
        
        self.predictedState = numpy.zeros((2,3))
        
        index = 0
        while index < 3:
            self.predictedState[:,index] = numpy.dot(self.stateTransitionxv,self.priorState[:,index])
            index = index+1
        
        intermediateMatrix = self.priorStateMatrix

        index = 0
        while index < 3:
            intermediateMatrix[:,:,index] = numpy.dot(self.stateTransitionxv, self.priorStateMatrix[:, :, index])
            index = index+1

        self.predictedStateMatrix = self.priorStateMatrix
            
        index = 0
        while index < 3:
            self.predictedStateMatrix[:,:,index] = numpy.dot(intermediateMatrix[:,:,index], self.stateTransitionxv.T) + self.processNoise[:,:,index]
            index = index+1
            
    def predict(self):
        
        numComponents = numpy.ma.size(self.priorState, 1)
        self.predictedState = numpy.zeros((2,numComponents))
        
        index = 0
        while index < numComponents:
            self.predictedState[:,index] = numpy.dot(self.stateTransitionxv,self.priorState[:,index])
            index = index+1
        
        intermediateMatrix = self.priorStateMatrix

        index = 0
        while index < numComponents:
            intermediateMatrix[:,:,index] = numpy.dot(self.stateTransition, self.priorStateMatrix[:, :, index])
            index = index+1

        self.predictedStateMatrix = self.priorStateMatrix
            
        index = 0
        while index < numComponents:
            self.predictedStateMatrix[:,:,index] = numpy.dot(intermediateMatrix[:,:,index], self.stateTransition.T) + self.processNoise[:,:,index]
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
        
        numComponents = numpy.ma.size(self.priorState,1)
        
        while index < numComponents:
            inv[:,:,index] = numpy.linalg.inv(scalingFactor[:,:,index])
            index = index+1
        
        index = 0
        
        self.KalmanGain = self.predictedStateMatrix
        
        while index < numComponents:
            self.KalmanGain[:,:,index] = numpy.dot(self.predictedStateMatrix[:,:,index], inv[:,:,index])
            index = index+1
            
        index = 0
        
        # KalmanGain = predictedStateMatrix dot inverse of (predictedStateMatrix + measurementNoise)
        
        while index < numComponents:
            self.priorState[:,index] = self.predictedState[:,index] + numpy.dot(self.KalmanGain[:,:,index],numpy.subtract(measuredState[:,index],self.predictedState[:,index]))
            index = index+1
            
        # priorState = predictedState + KalmanGain dot (measuredState - predictedState)
        
        intermediateArray = self.KalmanGain
        
        index = 0
        
        while index < numComponents:
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
        numComponents = numpy.array(positionData)
        numComponents = numComponents.shape[1]
        covarMatrix = numpy.zeros((2,2,numComponents))
        
        covarMatrix[0,0,:] = self.getVar(positionData)
        covarMatrix[1,1,:] = self.getVar(velocityData)
        
        return covarMatrix
    
    def calcAcceleration(self, velocityData, deltaTData):
            
        return numpy.diff(velocityData, axis=0) / deltaTData
    
    # Calculates acceleration if we'd like to go that route, but I'm unsure if I modelled it correctly
    # Calculates an acceleration array
    
    def calcAccelk(self, velocity, deltaT):
        
        velocity = numpy.array(velocity)
        priorState = numpy.array(self.priorState[1])
        
        return numpy.subtract(velocity, priorState) / deltaT
        
    # Calculates acceleration for one iteration
    
    def calcVelocity(self, positionData, deltaTData):
        
        velocityData = numpy.diff(positionData, axis=0)
        
        data = 0
        while data < len(deltaTData):
            velocityData[data] = velocityData[data]/deltaTData[data]
            data = data + 1
        
        return velocityData
    
    # Calculates velocity, some of the data might not have this available
    # Calculates a velocity array
    
    def calcVelocityk(self, position):
        
        return list(numpy.subtract(position, self.priorState[0]) / self.deltaT)
    
    # Calculates velocity for one iteration
    
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
    
    def dataSorter(self, absoluteFilePath):
        
        # this was brute forced, I'll deal with it later
        
        rawData = pandas.read_csv(absoluteFilePath)
        headers = rawData.columns.tolist()
        
        palmNormalx       = numpy.array(rawData[:][headers[0]].values.tolist())
        palmNormaly       = numpy.array(rawData[:][headers[1]].values.tolist())
        palmNormalz       = numpy.array(rawData[:][headers[2]].values.tolist())

        palmDirectionx    = numpy.array(rawData[:][headers[3]].values.tolist())
        palmDirectiony    = numpy.array(rawData[:][headers[4]].values.tolist())
        palmDirectionz    = numpy.array(rawData[:][headers[5]].values.tolist())

        palmCenterx       = numpy.array(rawData[:][headers[6]].values.tolist())
        palmCentery       = numpy.array(rawData[:][headers[7]].values.tolist())
        palmCenterz       = numpy.array(rawData[:][headers[8]].values.tolist())

        palmVelocityx     = numpy.array(rawData[:][headers[9]].values.tolist())
        palmVelocityy     = numpy.array(rawData[:][headers[10]].values.tolist())
        palmVelocityz     = numpy.array(rawData[:][headers[11]].values.tolist())

        thumbDeviation1   = numpy.array(rawData[:][headers[12]].values.tolist())
        thumbDeviation2   = numpy.array(rawData[:][headers[13]].values.tolist())
        thumbDeviation3   = numpy.array(rawData[:][headers[14]].values.tolist())

        thumbJointAngle1  = numpy.array(rawData[:][headers[15]].values.tolist())
        thumbJointAngle2  = numpy.array(rawData[:][headers[16]].values.tolist())

        indexDeviation1   = numpy.array(rawData[:][headers[17]].values.tolist())
        indexDeviation2   = numpy.array(rawData[:][headers[18]].values.tolist())
        indexDeviation3   = numpy.array(rawData[:][headers[19]].values.tolist())

        indexJointAngle1  = numpy.array(rawData[:][headers[20]].values.tolist())
        indexJointAngle2  = numpy.array(rawData[:][headers[21]].values.tolist())

        middleDeviation1  = numpy.array(rawData[:][headers[22]].values.tolist())
        middleDeviation2  = numpy.array(rawData[:][headers[23]].values.tolist())
        middleDeviation3  = numpy.array(rawData[:][headers[24]].values.tolist())

        middleJointAngle1 = numpy.array(rawData[:][headers[25]].values.tolist())
        middleJointAngle2 = numpy.array(rawData[:][headers[26]].values.tolist())
        
        ringDeviation1    = numpy.array(rawData[:][headers[27]].values.tolist())
        ringDeviation2    = numpy.array(rawData[:][headers[28]].values.tolist())
        ringDeviation3    = numpy.array(rawData[:][headers[29]].values.tolist())

        ringJointAngle1   = numpy.array(rawData[:][headers[30]].values.tolist())
        ringJointAngle2   = numpy.array(rawData[:][headers[31]].values.tolist())

        pinkyDeviation1   = numpy.array(rawData[:][headers[32]].values.tolist())
        pinkyDeviation2   = numpy.array(rawData[:][headers[33]].values.tolist())
        pinkyDeviation3   = numpy.array(rawData[:][headers[34]].values.tolist())

        pinkyJointAngle1  = numpy.array(rawData[:][headers[35]].values.tolist())
        pinkyJointAngle2  = numpy.array(rawData[:][headers[36]].values.tolist())

        timeStamp         = numpy.array(rawData[:][headers[37]].values.tolist())

        palmNormal       = [[x,y,z] for x in palmNormalx       for y in palmNormaly      for z in palmNormalz     ]
        palmDirection    = [[x,y,z] for x in palmDirectionx    for y in palmDirectiony   for z in palmDirectionz  ]
        palmCenter       = [[x,y,z] for x in palmCenterx       for y in palmCentery      for z in palmCenterz     ]
        palmVelocity     = [[x,y,z] for x in palmVelocityx     for y in palmVelocityy    for z in palmVelocityz   ]
        thumbDeviation   = [[a,b,c] for a in thumbDeviation1   for b in thumbDeviation2  for c in thumbDeviation3 ]
        thumbJointAngle  = [[a,b]   for a in thumbJointAngle1  for b in thumbJointAngle2                          ]
        indexDeviation   = [[a,b,c] for a in indexDeviation1   for b in indexDeviation2  for c in indexDeviation3 ]
        indexJointAngle  = [[a,b]   for a in indexJointAngle1  for b in indexJointAngle2                          ]
        middleDeviation  = [[a,b,c] for a in middleDeviation1  for b in middleDeviation2 for c in middleDeviation3]
        middleJointAngle = [[a,b]   for a in middleJointAngle1 for b in middleJointAngle2                         ]
        ringDeviation    = [[a,b,c] for a in ringDeviation1    for b in ringDeviation2   for c in ringDeviation3  ]
        ringJointAngle   = [[a,b]   for a in ringJointAngle1   for b in ringJointAngle2                           ]
        pinkyDeviation   = [[a,b,c] for a in pinkyDeviation1   for b in pinkyDeviation2  for c in pinkyDeviation3 ]
        pinkyJointAngle  = [[a,b]   for a in pinkyJointAngle1  for b in pinkyJointAngle2                          ]

        canonicalData = [palmCenter, palmVelocity, palmDirection, palmNormal, indexDeviation, middleDeviation, ringDeviation, pinkyDeviation, thumbDeviation, indexJointAngle, middleJointAngle, ringJointAngle, pinkyJointAngle, thumbJointAngle, timeStamp]

        return canonicalData
    