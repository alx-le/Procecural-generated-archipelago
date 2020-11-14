# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:43:56 2020

@author: kanbei
"""
import noise
import math
import numpy as np
from PIL import Image
#import pop

class world_gen:
           
    def genNMAP(self,x,y):
        noisemap = np.zeros((x,y))
        gradMap = self.genGMap()
        for i in range(y):
            for j in range(x):
                noisemap[i][j] = noise.pnoise2(i/self.scale, 
                                    j/self.scale, 
                                    octaves=self.octaves, 
                                    persistence=self.persistence, 
                                    lacunarity=self.lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=self.base)
                
        maxN = np.amax(noisemap)
        noisemap = noisemap/maxN
                
        for i in range(y):
            for j in range(x):
                noisemap[i][j] = noisemap[i][j]*abs(gradMap[i][j])
                if gradMap[i][j] > 0:
                    noisemap[i][j] *= 20
                    
        maxN = np.amax(noisemap)
        noisemap = noisemap/maxN
                
        return noisemap  
    
    def genGMap(self):
        gradMap = np.zeros((self.xDim,self.yDim))
        cntr = (self.xDim/2 , self.yDim/2)
        for i in range(self.xDim):
            for j in range(self.yDim):
                xDist = abs(i-cntr[0])
                yDist = abs(j-cntr[1])
                dist = math.sqrt(xDist*xDist + yDist*yDist)
                gradMap[i][j] = dist
        
        maxG = np.amax(gradMap)
        gradMap = gradMap/maxG
        gradMap = -gradMap
        gradMap += 0.5
        
        for i in range(self.xDim):
            for j in range(self.yDim):
                if gradMap[i][j] > 0:
                    gradMap[i][j] += 0
                    gradMap[i][j] *= 20
                elif gradMap[i][j] <= 0:
                    gradMap[i][j] *= 1
        
        
        maxG = np.amax(gradMap)
        gradMap = gradMap/maxG
        
        return gradMap
        
    def __init__(self, x = 1024, y = 1024, z = 0.1, b = 34):
        self.xDim = x
        self.yDim = y
        self.scale = 100.0
        self.octaves = 6
        self.persistence = 0.45
        self.lacunarity = 2
        self.base = b
        self.threshold = z
        self.nMap = self.genNMAP(x,y)
        self.rgbMap = np.zeros((x,y,3), dtype=np.uint8)
        self.rType = np.empty((x,y), dtype=str)
        
    def invoke(self):
        self.genMap()
        
            
    def showBgMap(self):
        img = Image.fromarray(self.rgbMap, mode='RGB')
        img.show()
        
    def retBgMap(self):
        self.genMap()
        img = Image.fromarray(self.rgbMap, mode='RGB')
        return img
    
    def retFgMap(self):
        img = Image.fromarray(self.fgMap, mode='RGBA')
        return img
        
    def genFgMap(self):
        shape = (self.xDim,self.yDim)
        bT = [255,255,255,0]
        fT = [173,255,47,100]
        
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.rType[i][j] == 'g':
                    maxim = np.amax(self.rss)
                    alp = np.rint(self.rss[i][j]/maxim*256)
                    fT = [173,255,47,alp]
                    self.fgMap[i][j] = fT
                else:
                    self.fgMap[i][j] = bT
                    
        self.updateFgMap()
    
    def genMap(self):
        shape = (self.xDim,self.yDim)
        blue = [65,105,225]
        darkblue = [0,0,128]
        green = [34,139,34]
        darkgreen = [60,109,34]
        beach = [238,214,120]
        mountain = [160,160,160]
        snow = [255,250,250]
        
        steps = [0,0.05,0.25,0.45,0.75]
        minL = self.threshold
        maxL = np.amax(self.nMap)
        boundaries = np.zeros((5,1))
        
        for s in range(len(steps)):
            boundaries[s] = minL + steps[s]*maxL
            
        for i in range(shape[0]):
            for j in range(shape[1]):
                if self.nMap[i][j] <= boundaries[0]:
                    self.rgbMap[i][j] = blue
                    self.rType[i][j] = 'f'
                elif self.nMap[i][j] > boundaries[0] and self.nMap[i][j] <= boundaries[1]:
                    self.rgbMap[i][j] = beach
                    self.rType[i][j] = 'n'
                elif self.nMap[i][j] >boundaries[1] and self.nMap[i][j] <= boundaries[2]:
                    self.rgbMap[i][j] = green
                    self.rType[i][j] = 'g'
                elif self.nMap[i][j] > boundaries[2] and self.nMap[i][j] <= boundaries[3]:
                    self.rgbMap[i][j] = darkgreen
                    self.rType[i][j] = 'w'
                elif self.nMap[i][j] > boundaries[3] and self.nMap[i][j] <= boundaries[4]:
                    self.rgbMap[i][j] = mountain
                    self.rType[i][j] = 'm'
                elif self.nMap[i][j] > boundaries[4]:
                    self.rgbMap[i][j] = snow
                    self.rType[i][j] = 's'
                    
    def showMap(self):
        bg = self.retBgMap()
        bg.show()
        
                    