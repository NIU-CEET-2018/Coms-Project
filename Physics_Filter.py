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
# Index Joint Angle 1,  Index Joint Angle 2, Index Joint Angle 3
# Middle Deviation 1,   Middle Deviation 2,   Middle Deviation 3
# Middle Joint Angle 1, Middle Joint Angle 2, Middle Joint Angle 3 
# Ring Deviation 1,     Ring Deviation 2,     Ring Deviation 3
# Ring Joint Angle 1,   Ring Joint Angle 2, Ring Joint Angle 3
# Pinky Deviation 1,    Pinky Deviation 2,    Pinky Deviation 3
# Pinky Joint Angle 1,  Pinky Joint Angle 2, Pinky Joint Angle 3
# Time Stamp

handParts = ["palmNormXKF", "palmNormYKF","palmNormZKF",
             "palmDirXKF", "palmDirYKF", "palmDirZKF",
             "palmXKF", "palmYKF", "palmZKF", 
             "thumbDev1KF", "thumbDev2KF", "thumbDev3KF", 
             "thumbJoint1KF","thumbJoint2KF",
             "pointerDev1KF", "pointerDev2KF", "pointerDev3KF", 
             "pointerJoint1KF","pointerJoint2KF", "pointerJoin3KF",
             "middleDev1KF", "middleDev2KF", "middleDev3KF",
             "middleJoint1KF", "middleJoint2KF", "middleJoint3KF",
             "ringDev1KF", "ringDev2KF","ringDev3KF",
             "ringJoint1KF", "ringJoint2KF", "ringJoint3KF",
             "pinkyDev1KF", "pinkyDev2KF","pinkyDev3KF",
             "pinkyJoint1KF", "pinkyJoint2KF", "pinkyJoinT3KF"]

def initializeHand(object): 
    #for part in range(len(handParts)):
    part = 0
    while part < len(handParts):
        handParts[part] = Physics_Filter(handParts[part])
        part = part + 1
    # Initializes all the parts of the hand for the filter
    
def dataSorter(absoluteFilePath):
    # this was brute forced, I'll deal with it later
        
    rawData = pandas.read_csv(absoluteFilePath)
    headers = rawData.columns.tolist()
        
    palmNormalX       = numpy.array(rawData[:][headers[0]].values.tolist())
    palmNormalY       = numpy.array(rawData[:][headers[1]].values.tolist())
    palmNormalZ       = numpy.array(rawData[:][headers[2]].values.tolist())

    palmDirectionX    = numpy.array(rawData[:][headers[3]].values.tolist())
    palmDirectionY    = numpy.array(rawData[:][headers[4]].values.tolist())
    palmDirectionZ    = numpy.array(rawData[:][headers[5]].values.tolist())

    palmCenterX       = numpy.array(rawData[:][headers[6]].values.tolist())
    palmCenterY       = numpy.array(rawData[:][headers[7]].values.tolist())
    palmCenterZ       = numpy.array(rawData[:][headers[8]].values.tolist())

    palmVelocityX     = numpy.array(rawData[:][headers[9]].values.tolist())
    palmVelocityY     = numpy.array(rawData[:][headers[10]].values.tolist())
    palmVelocityZ     = numpy.array(rawData[:][headers[11]].values.tolist())

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
    indexJointAngle3  = numpy.array(rawData[:][headers[22]].values.tolist())

    middleDeviation1  = numpy.array(rawData[:][headers[23]].values.tolist())
    middleDeviation2  = numpy.array(rawData[:][headers[24]].values.tolist())
    middleDeviation3  = numpy.array(rawData[:][headers[25]].values.tolist())

    middleJointAngle1 = numpy.array(rawData[:][headers[26]].values.tolist())
    middleJointAngle2 = numpy.array(rawData[:][headers[27]].values.tolist())
    middleJointAngle3 = numpy.array(rawData[:][headers[28]].values.tolist())
        
    ringDeviation1    = numpy.array(rawData[:][headers[29]].values.tolist())
    ringDeviation2    = numpy.array(rawData[:][headers[30]].values.tolist())
    ringDeviation3    = numpy.array(rawData[:][headers[31]].values.tolist())

    ringJointAngle1   = numpy.array(rawData[:][headers[32]].values.tolist())
    ringJointAngle2   = numpy.array(rawData[:][headers[33]].values.tolist())
    ringJointAngle3   = numpy.array(rawData[:][headers[34]].values.tolist())

    pinkyDeviation1   = numpy.array(rawData[:][headers[35]].values.tolist())
    pinkyDeviation2   = numpy.array(rawData[:][headers[36]].values.tolist())
    pinkyDeviation3   = numpy.array(rawData[:][headers[37]].values.tolist())

    pinkyJointAngle1  = numpy.array(rawData[:][headers[38]].values.tolist())
    pinkyJointAngle2  = numpy.array(rawData[:][headers[39]].values.tolist())
    pinkyJointAngle3  = numpy.array(rawData[:][headers[40]].values.tolist())

    timeStamp         = numpy.array(rawData[:][headers[41]].values.tolist())
                        
    canonicalData = [palmNormalX,       palmNormalY,      palmNormalZ,  
                     palmDirectionX,    palmDirectionY,   palmDirectionZ,
                     palmCenterX,       palmCenterY,      palmCenterZ,
                     palmVelocityX,     palmVelocityY,    palmVelocityZ,
                     thumbDeviation1,   thumbDeviation2,  thumbDeviation3,
                     thumbJointAngle1,  thumbJointAngle2, 
                     indexDeviation1,   indexDeviation2,  indexDeviation3, 
                     indexJointAngle1,  indexJointAngle2, indexJointAngle3,
                     middleDeviation1,  middleDeviation2, middleDeviation3, 
                     middleJointAngle1, middleJointAngle2, middleJointAngle3,
                     ringDeviation1,    ringDeviation2,   ringDeviation3, 
                     ringJointAngle1,   ringJointAngle2, ringJointAngle3,
                     pinkyDeviation1,   pinkyDeviation2,  pinkyDeviation3,   
                     pinkyJointAngle1,  pinkyJointAngle2,  pinkyJointAngle3,
                     timeStamp]

    return canonicalData

def setupKF(staticAbsoluteFilePath, movingAbsoluteFilePath):
        
    staticCanonicalData = dataSorter(staticAbsoluteFilePath)
    movingCanonicalData = dataSorter(movingAbsoluteFilePath)
    
    # setupKalmanFilter for each handPart, not sure how to condense this
    part = 0
    while part < 6:
        handParts[part].setupKalmanFilterx(staticCanonicalData[part], movingCanonicalData[part], staticCanonicalData[41], movingCanonicalData[41])
        part = part + 1
        
    handParts[6].setupKalmanFilterxv(staticCanonicalData[6], staticCanonicalData[9],  movingCanonicalData[6], movingCanonicalData[9])
    handParts[7].setupKalmanFilterxv(staticCanonicalData[7], staticCanonicalData[10],  movingCanonicalData[7], movingCanonicalData[10])
    handParts[8].setupKalmanFilterxv(staticCanonicalData[8], staticCanonicalData[11],  movingCanonicalData[8], movingCanonicalData[11])
    
    part = 9
    while part < len(handParts):
        handParts[part].setupKalmanFilterx(staticCanonicalData[part+3], movingCanonicalData[part+3], staticCanonicalData[41], movingCanonicalData[41])
        part = part + 1
    
def getInitialState(canonicalData, nextData):
    
    part = 0
    while part < len(handParts):
        handParts[part].timestamp = canonicalData[41]
        part = part + 1
    
    part = 0
    while part < len(handParts):
        handParts[part].getDeltaTk(nextData[41])
        handParts[part].priorState = numpy.zeros((2))
        part = part + 1
        
    part = 0
    while part < 6:
        handParts[part].priorState[0] = canonicalData[part]
        handParts[part].priorState[1] = handParts[part].calcVelocityk(nextData[part])
        part = part + 1  
        
    part = 6
    while part < 10:
        handParts[part].priorState[0] = canonicalData[part]
        handParts[part].priorState[1] = canonicalData[part+3]
        part = part + 1
    
    part = 9
    while part < len(handParts):
        handParts[part].priorState[0] = canonicalData[part+3]
        handParts[part].priorState[1] = handParts[part].calcVelocityk(nextData[part+3])
        part = part + 1
        
def KalmanFilter(canonicalData):

    part = 0
    while part < len(handParts):
        handParts[part].getDeltaTk(canonicalData[41])
        part = part + 1
        
    # build measuredStates
    measuredStates = numpy.zeros((len(handParts),2))
    
    part = 0
    while part < 6:
        measuredStates[part] = numpy.array([canonicalData[part], handParts[part].calcVelocityk(canonicalData[part])])
        part = part + 1
    
    part = 6
    while part < 10:
        measuredStates[part] = numpy.array([canonicalData[part], canonicalData[part+3]])
        part = part + 1
        
    part = 9
    while part < len(handParts):
        measuredStates[part] = numpy.array([canonicalData[part+3], handParts[part].calcVelocityk(canonicalData[part+3])])
        part = part + 1
        
    part = 0
    while part < len(handParts):
        handParts[part].predict()
        part = part + 1
        
    part = 0
    while part < len(handParts):
        handParts[part].update(measuredStates[part])
        part = part + 1
        
    # canonicalize processed data
    palmNormalX = handParts[0].priorState[0]
    palmNormalY = handParts[1].priorState[0]
    palmNormalZ = handParts[2].priorState[0]
    palmDirectionX = handParts[3].priorState[0]
    palmDirectionY = handParts[4].priorState[0]
    palmDirectionZ = handParts[5].priorState[0]
    palmCenterX = handParts[6].priorState[0]
    palmCenterY = handParts[7].priorState[0]
    palmCenterZ = handParts[8].priorState[0]
    palmVelocityX = handParts[6].priorState[1]
    palmVelocityY = handParts[7].priorState[1]
    palmVelocityZ = handParts[8].priorState[1]
    thumbDeviation1 = handParts[9].priorState[0]
    thumbDeviation2 = handParts[10].priorState[0]
    thumbDeviation3 = handParts[11].priorState[0]
    thumbJointAngle1 = handParts[12].priorState[0]
    thumbJointAngle2 = handParts[13].priorState[0]
    indexDeviation1 = handParts[14].priorState[0]
    indexDeviation2 = handParts[15].priorState[0]
    indexDeviation3 = handParts[16].priorState[0]
    indexJointAngle1 = handParts[17].priorState[0]
    indexJointAngle2 = handParts[18].priorState[0]
    indexJointAngle3 = handParts[19].priorState[0]
    middleDeviation1 = handParts[20].priorState[0]
    middleDeviation2 = handParts[21].priorState[0]
    middleDeviation3 = handParts[22].priorState[0]
    middleJointAngle1 = handParts[23].priorState[0]
    middleJointAngle2 = handParts[24].priorState[0]
    middleJointAngle3 = handParts[25].priorState[0]
    ringDeviation1 = handParts[26].priorState[0]
    ringDeviation2 = handParts[27].priorState[0]
    ringDeviation3 = handParts[28].priorState[0]
    ringJointAngle1 = handParts[29].priorState[0]
    ringJointAngle2 = handParts[30].priorState[0]
    ringJointAngle3 = handParts[31].priorState[0]
    pinkyDeviation1 = handParts[32].priorState[0]
    pinkyDeviation2 = handParts[33].priorState[0]
    pinkyDeviation3 = handParts[34].priorState[0]
    pinkyJointAngle1 = handParts[35].priorState[0]
    pinkyJointAngle2 = handParts[36].priorState[0]
    pinkyJointAngle3 = handParts[37].priorState[0]
    timeStamp = canonicalData[41]
    
    filteredData  = [palmNormalX,       palmNormalY,      palmNormalZ,  
                     palmDirectionX,    palmDirectionY,   palmDirectionZ,
                     palmCenterX,       palmCenterY,      palmCenterZ,
                     palmVelocityX,     palmVelocityY,    palmVelocityZ,
                     thumbDeviation1,   thumbDeviation2,  thumbDeviation3,
                     thumbJointAngle1,  thumbJointAngle2,
                     indexDeviation1,   indexDeviation2,  indexDeviation3, 
                     indexJointAngle1,  indexJointAngle2, indexJointAngle3,
                     middleDeviation1,  middleDeviation2, middleDeviation3, 
                     middleJointAngle1, middleJointAngle2, middleJointAngle3,
                     ringDeviation1,    ringDeviation2,   ringDeviation3, 
                     ringJointAngle1,   ringJointAngle2, ringJointAngle3,
                     pinkyDeviation1,   pinkyDeviation2,  pinkyDeviation3,   
                     pinkyJointAngle1,  pinkyJointAngle2, pinkyJointAngle3,
                     timeStamp]
    
    return filteredData

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
    