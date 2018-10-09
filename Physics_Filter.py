#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import pandas

#TODO:
# - [ ] Fine tune process noise matrix, EXTREMELY IMPORTANT
# - [ ] Organize better

# LIST OF DATA (AND ORDER) FROM ANDREW'S HAND:                   
# Palm Normal x,        Palm Normal y,        Palm Normal z       
# Palm Direction x,     Palm Direction y,     Palm Direction z    
# Palm Center x,        Palm Center y,        Palm Center z      
# Palm Velocity x,      Palm Velocity y,      Palm Velocity z    
# Thumb Deviation 1,    Thumb Deviation 2,    Thumb Deviation 3   
# Thumb Joint Angle 1,  Thumb Joint Angle 2                      
# Index Deviation 1,    Index Deviation 2,    Index Deviation 3
# Index Joint Angle 1,  Index Joint Angle 2                    
# Middle Deviation 1,   Middle Deviation 2,   Middle Deviation 3
# Middle Joint Angle 1, Middle Joint Angle 2                      
# Ring Deviation 1,     Ring Deviation 2,     Ring Deviation 3
# Ring Joint Angle 1,   Ring Joint Angle 2                       
# Pinky Deviation 1,    Pinky Deviation 2,    Pinky Deviation 3
# Pinky Joint Angle 1,  Pinky Joint Angle 2                      
# Time Stamp                                                      

class Physics_Filter(object):
    
    def __init__(self,name):
        self.name                 = name                                    
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
            
    # Used for palm position and velocity
            
    def predict(self):
        
        numComponents = numpy.ma.size(self.priorState, 1)
        self.predictedState = numpy.zeros((2,numComponents))
        
        index = 0
        while index < numComponents:
            self.predictedState[:,index] = numpy.dot(self.stateTransition,self.priorState[:,index])
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
            
    # Used for all the rest
    
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
    
    # Used in DEMO
    
    def getCovarxv(self, positionData, velocityData):
        numComponents = numpy.array(positionData)
        numComponents = numComponents.shape[1]
        covarMatrix = numpy.zeros((2,2,numComponents))
        
        covarMatrix[0,0,:] = self.getVar(positionData)
        covarMatrix[1,1,:] = self.getVar(velocityData)
        
        return covarMatrix
    
    def calcVelocity(self, positionData, deltaTData):
        
        velocityData = numpy.diff(positionData, axis=0)
        
        data = 0
        while data < len(deltaTData):
            velocityData[data] = velocityData[data]/deltaTData[data]
            data = data + 1
        
        return velocityData
    
    # Calculates a velocity array
    
    def calcVelocityk(self, position):
        
        return list(numpy.subtract(position, self.priorState[0]) / self.deltaT)
    
    # Calculates velocity for one iteration
    