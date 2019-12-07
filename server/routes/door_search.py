import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join

from server.routes.surface_type import SurfaceType
from server.routes.surface import Surface

class DoorSearch:
    def __init__(self, filePatch):
        self.__filePatch=filePatch

    def __getFilesNames(self):
        WayFile = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'image' + os.sep + 'doors'
     
        return [WayFile + os.sep + f for f in listdir(WayFile) if isfile(join(WayFile, f)) and f[-4:] == '.png']

    def SearchDoors (self):
        NameFileDoors = self.__getFilesNames()
        ReadImage_Gary = cv2.cvtColor(self.__filePatch, cv2.COLOR_BGR2GRAY)
        threshold = 0.80
        SetDoor = set()
        for Namedoors in NameFileDoors:
            template = cv2.imread(Namedoors)
           #print(Namedoors)
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(ReadImage_Gary, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                SetDoor.add((
                    (pt[0] // 10),
                    (pt[1] // 10),
                    (w // 10),
                    (h // 10)
                ))
               # cv2.rectangle(self.__filePatch, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
       # cv2.namedWindow("123",cv2.WINDOW_NORMAL)
       # cv2.imshow("123",self.__filePatch)
       # cv2.waitKey(0)
        return SetDoor

    def Search (self, ReadImage):
        Set=self.SearchDoors()
        for row, col, w, h in Set:
            for clear_row in range(row - 1, row + w +1):
                for clear_col in range(col - 1, col + h + 1):
                    #print (clear_row,"/",clear_col,"/",w,"/",h)
                    ReadImage[clear_col][clear_row].surface = Surface(SurfaceType.FREE_SPACE)




