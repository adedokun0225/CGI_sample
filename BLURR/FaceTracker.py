from typing import Counter, OrderedDict
import numpy as np
import face_recognition
from LocalData.Settings import Settings

NAME = "name"
IDENTIFIED = "identified"
COUNTER = "counter"

class FaceTracker():

    def __init__(self) -> None:
        self.trackedFaces = dict()

    #gets the face encoding from the preferences file
    def updateEncodings(self):
        savedEnc = Settings.get(Settings.ENCODED_FACES)
        self.encodings = {}
        for person in savedEnc:
            encs = []
            for enc in savedEnc[person]:
                encs.append(np.asarray(enc))
            self.encodings[person] = encs
            
    #face recognition for the next frame, using objects from the centroid tracker
    def update(self, frame, rects, objects:OrderedDict):
        self.updateEncodings()
        self.incrementCounters(objects)
        
        #iterate over all objects and check whether they were already recognized
        for id in objects:
            if not id in self.trackedFaces or not self.trackedFaces[id][IDENTIFIED]:
                print("New face")
                #if no, search for the frame bounding the object
                rect = self.searchForFrame(objects[id], rects)
                if rect==None:
                    #if no rect was found -> add new unrecognized face
                    if not id in self.trackedFaces:
                        self.trackedFaces[id] = {NAME:None, IDENTIFIED: False, COUNTER: 0}
                    continue
                
                #get the encoding of the face in the found rect
                toCheck = face_recognition.face_encodings(frame, known_face_locations=[rect])
                #if no encoding was found -> add a new unrecognized face
                if len(toCheck)==0:
                    if not id in self.trackedFaces:
                        self.trackedFaces[id] = {NAME:None, IDENTIFIED: False, COUNTER: 0}
                else:
                    foundMatch = False
                    #otherwise iterate over all face encodings to find a match
                    for person in self.encodings:
                        results = face_recognition.compare_faces(self.encodings[person], toCheck[0])
                        result = False
                        for res in results:
                            result = result or res
                        if result:
                            #if some encoding matches the face -> mark as identified
                            foundMatch = True
                            self.trackedFaces[id] = {NAME:person, IDENTIFIED: True, COUNTER: 0}
                            print("Recognized " + str(person)) 
                            break
                    #if no match was found -> add unrecognized face
                    if not foundMatch:
                        if not id in self.trackedFaces:
                            self.trackedFaces[id] = {NAME:None, IDENTIFIED: False, COUNTER: 0}

    #update the list with the currently tracked faces
    def incrementCounters(self, objects:OrderedDict):
        toRemove = []
        for id in self.trackedFaces:
            #mark the objects that are no longer present to remove them
            if not id in objects:
                toRemove.append(id)
            else:
            #increment the frame counters of not recognized faces 
                if not self.trackedFaces[id][IDENTIFIED]:
                    self.trackedFaces[id][COUNTER]+=1
        #removed the previously marked faces
        for id in toRemove:
            self.trackedFaces.pop(id)

    #check whether all recognized faces are authorized
    def isEveryoneAuthorized(self, counterLimit=2):
        for id in self.trackedFaces:
            if not self.trackedFaces[id][IDENTIFIED] and self.trackedFaces[id][COUNTER]>=counterLimit:
                return False
        return True

    #search for a suiting rect given its midpoint
    def searchForFrame(self, midpoint, rects):
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            x = int((endX+startX)/2.0)
            y = int((endY+startY)/2.0)
            if midpoint[0]==x and midpoint[1]==y:
                return [startY, endX, endY, startX]
        return None

    def reset(self):
        self.trackedFaces = dict()

    def getFaceLocations(self, frame):
        return face_recognition.face_locations(frame)

    def getFaceEncodings(self, frame):
        return face_recognition.face_encodings(frame)


    