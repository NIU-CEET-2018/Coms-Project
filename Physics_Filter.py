#!/usr/bin/python3

"""Filters out and cleans up suspicious/noisy data from a stream."""

import numpy
import pandas

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
    """An object for filtering noisy sensor data.

    Filters noisy data about physical systems using a KalmanFilter.
    """
    def __init__(self, name):
        self.name                 = name
        self.processNoise         = 0
        self.measurementNoise     = 0
        self.initialStateMatrix   = 0
        self.priorStateMatrix     = 0
        self.predictedStateMatrix = 0
        self.deltaT               = 0
        self.stateTransitionXV    = numpy.array(([1, self.deltaT], [0, 1]))
        self.stateTransitionX     = numpy.array(([1, 0.5*self.deltaT], [0, 0.5]))
        self.stateTransition      = 0
        self.priorState           = 0
        self.predictedState       = 0
        self.KalmanGain           = 0
        self.timestamp            = 0

    def setupKalmanFilterxv(self, staticPositionData, staticVelocityData, movingPositionData, movingVelocityData):
        self.stateTransition    = self.stateTransitionXV

        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix

        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise

    def setupKalmanFilterx(self, staticPositionData, movingPositionData, staticTimestampData, movingTimestampData):
        self.stateTransition   = self.stateTransitionX

        staticDeltaTData       = self.getDeltaT(staticTimestampData)
        movingDeltaTData       = self.getDeltaT(movingTimestampData)
        staticVelocityData     = self.calcVelocity(staticPositionData,staticDeltaTData)
        movingVelocityData     = self.calcVelocity(movingPositionData,movingDeltaTData)

        self.measurementNoise   = self.getCovarxv(staticPositionData, staticVelocityData)
        self.initialStateMatrix = self.getCovarxv(movingPositionData, movingVelocityData)
        self.priorStateMatrix   = self.initialStateMatrix

        confidenceFactor  = 0.5
        self.processNoise = confidenceFactor*self.measurementNoise

    def KalmanFilter(self, measuredState, measuredTime):
        self.deltaT    = self.getDeltaTk(measuredTime)
        self.predict()

        priorState = self.update(measuredState)

        return priorState

    def predict(self):
        self.predictedState       = numpy.dot(self.stateTransition,self.priorState)
        self.predictedStateMatrix = numpy.dot(numpy.dot(self.stateTransition,self.priorStateMatrix),self.stateTransition.T) + self.processNoise

    def update(self, measuredState):
        scalingFactor         = self.predictedStateMatrix + self.measurementNoise

        self.KalmanGain       = numpy.dot(self.predictedStateMatrix,numpy.linalg.inv(scalingFactor))
        self.priorState       = self.predictedState + numpy.dot(self.KalmanGain,numpy.subtract(measuredState,self.predictedState))
        self.priorStateMatrix = numpy.subtract(self.predictedStateMatrix,numpy.dot(self.KalmanGain,self.predictedStateMatrix))

        return self.priorState

    def getDeltaTk(self, measuredTime):
        self.deltaT    = measuredTime - self.timestamp
        self.timestamp = measuredTime

    def getDeltaT(self, timestampData):
        return numpy.diff(timestampData)

    def getVar(self, dataset):
        return numpy.var(dataset,axis=0)

    def getCovarxv(self, positionData, velocityData):
        covarMatrix = numpy.zeros((2,2))

        covarMatrix[0,0] = self.getVar(positionData)
        covarMatrix[1,1] = self.getVar(velocityData)

        return covarMatrix

    def calcVelocityk(self, position):
        return numpy.subtract(position, self.priorState[0]) / self.deltaT

    def calcVelocity(self, positionData, deltaTData):
        velocityData = numpy.diff(positionData, axis=0)
        
        data = 0
        
        while data < len(deltaTData):
            velocityData[data] = velocityData[data]/deltaTData[data]
            data=data+1
            
        return velocityData
    