import pygame
from pygame.locals import *
import math
import numpy as np

class Renderer:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("3D Renderer")
        self.FocalLength = 180
        self.scale = 450

        self.vertices = [
            (70, 70, 70),     # Vertex 0
            (70, -70, 70),     # Vertex 1
            (-70, -70, 70),     # Vertex 2
            (-70, 70, 70),     # Vertex 3
            (70, 70, -70),     # Vertex 4
            (70, -70, -70),     # Vertex 5
            (-70, -70, -70),     # Vertex 6
            (-70, 70, -70)      # Vertex 7
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Top face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Bottom face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting faces
        ]

        #Triangle Vertices
        self.Tvertices = [
            (20, -20, -20),   # Vertex 0 (bottom left)
            (20, -20, 20),    # Vertex 1 (bottom right)
            (-20, -20, 20),   # Vertex 2 (top right)
            (-20, -20, -20),  # Vertex 3 (top left)
            (0, 20, 0)      # Top
        ]
        #Triangle Edges
        self.Tedges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Base square
            (0, 4), (1, 4), (2, 4), (3, 4)   # Connecting edges to apex
        ]

        #Camera position i only use the camera position tbh tho 
        self.camera_position = [0.0, 0.0, 0.0]  
        self.look_at = [0.0, 0.0, 0.0]      
        self.up_vector = (0.0, 1.0, 0.0)  

        self.camera_coordinates = {
            'position': self.camera_position,
            'look_at': self.look_at,
            'up_vector': self.up_vector
        }

        self.angle = 0

    def CalculateCoords(self,vertices,C):
        FocalLength = self.FocalLength

        x, y, z = vertices

        #Matrices for X,Y and Z rotations 
        self.Y_Rotation = np.array([
            [math.cos(self.angle), 0, math.sin(self.angle)],
            [0, 1, 0],
            [-math.sin(self.angle), 0, math.cos(self.angle)]])
        
        self.Z_Rotation = np.array([
            [math.cos(self.angle), -math.sin(self.angle), 0],
            [math.sin(self.angle), math.cos(self.angle), 0],
            [0, 0, 1]])


        self.X_Rotation = np.array([
            [1, 0, 0],
            [0, math.cos(self.angle), -math.sin(self.angle)],
            [0, math.sin(self.angle), math.cos(self.angle)]])

        # Adjust coordinates based on camera position
        x -= self.camera_position[0]
        y -= self.camera_position[1]
        z -= self.camera_position[2]

        #rotated_coordinates = np.matmul(self.Z_Rotation, np.matmul(self.Y_Rotation, np.matmul(self.X_Rotation, np.array([x, y, z]))))
        if C:
            rotated_coordinates = np.matmul(self.Z_Rotation, np.matmul(self.Y_Rotation, np.matmul(self.X_Rotation, np.array([x, y, z]))))
        else:
            rotated_coordinates = np.matmul(self.X_Rotation,np.array([x, y, z]))

        # Extract rotated coordinates
        x_rotated, y_rotated, z_rotated = rotated_coordinates

        # Calculate projected coordinates
        Xprojected = (FocalLength * x_rotated) // (FocalLength + z_rotated)
        Yprojected = (FocalLength * y_rotated) // (FocalLength + z_rotated)

        return [Xprojected, Yprojected]

    def GetAllPositions(self):
        RenderCoordsC = []
        RenderCoordsT = []
        for vertices in self.vertices:
            RenderCoordsC.append(self.CalculateCoords(vertices,True))

        for vertices in self.Tvertices:
            RenderCoordsT.append(self.CalculateCoords(vertices,False))
        return RenderCoordsC,RenderCoordsT

    def convert_coordinates(self, coordinates: list[int, int]) -> list[int, int]:
        x, y = coordinates
        scale = self.scale

        PX = int((x + scale) * (self.width / (2 * scale)))
        PY = int((y + scale) * (self.height / (2 * scale)))

        return [PX, PY]

    def RenderScene(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        
        #camera_position =  self.ChangeCameraAngles

        positionsC,positionsT = self.GetAllPositions()

        colorC = (255, 255, 255)
        colorT = (83,195,189)
        for edge in self.edges:
            #Draw cube 
            start = self.convert_coordinates(positionsC[edge[0]])
            end = self.convert_coordinates(positionsC[edge[1]])
            try:
                pygame.draw.line(self.screen, colorC, start, end, 2)
            except:
                print("pass")
        
        for edge in self.Tedges:
            #Draw triangle 
            start = self.convert_coordinates(positionsT[edge[0]])
            end = self.convert_coordinates(positionsT[edge[1]])
            try:
                pygame.draw.line(self.screen, colorT, start, end, 2)
            except:
                print("pass") 
        
                
        self.angle += 0.0001
        pygame.display.update()

    def MainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                #Right
                self.camera_position[0] -= 0.1
            if keys[K_d]:
                #Left 
                self.camera_position[0] += 0.1
            if keys[K_SPACE]:
                #Up
                self.camera_position[1] -= 0.1
            if keys[K_LSHIFT]:
                #Down
                self.camera_position[1] += 0.1
            if keys[K_w]:
                #forwards
                self.camera_position[2] += 0.1
            if keys[K_s]:
                #forwards
                self.camera_position[2] -= 0.1
            self.RenderScene()

if __name__ == "__main__":
    renderer = Renderer()
    renderer.MainLoop()