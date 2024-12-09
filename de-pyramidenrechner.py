#pyramidenrechner von https://github.com/users/ArminiusKratiphilus
import math
import numpy as np
import matplotlib.pyplot as plt

class ImpossibleBodyError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class cone:
    def __init__(self,elev=None,height=None): #elevation angle in degrees
        self.elev = elev
        self.height = height
        
        if self.elev == None and self.height != None:
            self.elev_str = "Höhe von "+str(self.height)
            self.Z = self.height
        elif self.elev != None and self.height == None:
            self.elev_str = "Steigung von "+str(self.elev)+"°"
            self.elev = math.pi*float(self.elev)/180
        else:
            raise ImpossibleBodyError("Es muss entweder die Steigung oder die Höhe definiert sein.",(elev,height))
            
        if self.height != None:
            if self.Z < 0:
                raise ImpossibleBodyError("Kegelhöhe darf nicht kleiner als 0 sein.",height)
        if self.elev != None:
            if self.elev >= 90 or self.elev < 0:
                raise ImpossibleBodyError("Steigungswinkel muss im Intervall [0,90) liegen.",elev)
        
        print("\nKegel mit einer "+self.elev_str+":")
        self.xy_points = [[math.cos(x),math.sin(x),0] for x in np.linspace(0,2*math.pi,360)]
        if self.elev != None:
            self.Z = math.tan(self.elev)
            self.diagonal = math.sqrt(1+self.Z**2)
            self.papercraft_angle = 2*math.pi*math.cos(self.elev)
        if self.height != None:
            self.elev = math.atan(self.Z)
            self.diagonal = math.sqrt(1+self.Z**2)
            self.papercraft_angle = 2*math.pi/self.diagonal
        self.z_point = [0,0,self.Z]
        self.radius = 1
        self.xy_papercraft_points = [[self.diagonal*math.cos(x),self.diagonal*math.sin(x),0] for x in np.linspace(0,self.papercraft_angle,359,endpoint=True)]
        print("   Winkel:")
        print("      Papiervorlagen-Bogenwinkel: "+str(180*self.papercraft_angle/math.pi)+"°")
        print("      Papiervorlagen-Bogenwinkel im Bogenmaß: "+str(self.papercraft_angle))
        print("      Steigungswinkel: "+str(180*self.elev/math.pi))
        print("   Kegelpunkte:")
        #for i in range(len(self.xy_points)):
        #    print("      Bodenpunkt-"+str(i+1)+" : "+str(self.xy_points[i]))
        print("      Spitzenpunkt : "+str(self.z_point))
        print("   Papiervorlage-Punkte:")
        #for i in range(len(self.xy_papercraft_points)):
        #    print("      Punkt-"+str(i+1)+" : "+str(self.xy_papercraft_points[i]))
        print("      Ursprung : [0, 0]")
        print("   Längen normiert auf den RADIUS:") #standard
        print("      Radius : "+str(self.radius))
        print("      Höhe : "+str(self.Z))
        print("      Diagonale : "+str(self.diagonal))
        print("   Längen normiert auf die HÖHE:")
        print("      Radius : "+str(self.radius/self.Z))
        print("      Höhe : "+str(1))
        print("      Diagonale : "+str(self.diagonal/self.Z))
        print("   Längen normiert auf die DIAGONALE:")
        print("      Radius : "+str(self.radius/self.diagonal))
        print("      Höhe : "+str(self.Z/self.diagonal))
        print("      Diagonale : "+str(1))
        
    def plot_papercraft(self):
        plt.figure("2d plot der Papiervorlage des Kegels")
        paper = plt.axes(xlabel="x",ylabel="y")
        xy = self.xy_papercraft_points
        for i in range(len(xy)-1):
            paper.plot([xy[i][0],xy[i+1][0]],[xy[i][1],xy[i+1][1]],color="black")
        paper.plot([xy[0][0],0],[xy[0][1],0],color="black")
        paper.plot([xy[-1][0],0],[xy[-1][1],0],color="black")
        paper.set_aspect("equal")
        plt.show()
    
    def plot_3d(self):
        plt.figure("3d plot des Kegels")
        space = plt.axes(projection="3d",xlabel="x",ylabel="y",zlabel="z")
        space.grid()
        xy = self.xy_points
        z = self.z_point
        space.scatter(0,0,0,s=15,color="black",marker="+") #origin
        space.scatter(0,0,self.z_point[2],s=30,color="blue",alpha=0.3)
        n = 0
        for i in range(len(xy)-1):
            space.plot([xy[i][0],xy[i+1][0]],[xy[i][1],xy[i+1][1]],[xy[i][2],xy[i+1][2]],color="blue")
            n += 1
            if n == 1:
                space.plot([xy[i][0],z[0]],[xy[i][1],z[1]],[xy[i][2],z[2]],color="red")
            if n == 36:
                n = 0
        space.set_aspect("equal")
        plt.show()
        
class pyramid:
    def __init__(self,sides=4,surface_elev=None,edge_elev=None,height=None): #elevation angles in degrees
        self.N = int(sides)
        self.surface_elev = surface_elev
        self.edge_elev = edge_elev
        self.height = height
        
        if self.surface_elev == None and self.edge_elev == None and self.height != None:
            self.elev_str = "Höhe von "+str(self.height)
            self.Z = self.height
        elif self.surface_elev == None and self.edge_elev != None and self.height == None:
            self.elev_str = "Kantensteigung von "+str(self.edge_elev)+"°"
            self.edge_elev = math.pi*float(self.edge_elev)/180
        elif self.surface_elev != None and self.edge_elev == None and self.height == None:
            self.elev_str = "Flächensteigung von "+str(self.surface_elev)+"°"
            self.surface_elev = math.pi*float(self.surface_elev)/180
        else:
            raise ImpossibleBodyError("Es muss entweder eine Steigung oder die Höhe definiert sein.",(surface_elev,edge_elev,height))
            
        if self.N <= 2:
            raise ImpossibleBodyError("Eine Pyramide kann nicht weniger als drei Manteldreiecke haben.",sides)
        if self.height != None:
            if self.Z < 0:
                raise ImpossibleBodyError("Pyramidenhöhe darf nicht kleiner als 0 sein.",height)
        if self.edge_elev != None:
            if self.edge_elev >= 90 or self.edge_elev < 0:
                raise ImpossibleBodyError("Steigungswinkel muss im Intervall [0,90) liegen.",edge_elev)
        if self.surface_elev != None:
            if self.surface_elev >= 90 or self.surface_elev < 0:
                raise ImpossibleBodyError("Steigungswinkel muss im Intervall [0,90) liegen.",surface_elev)
            
        print("\nPyramide mit "+str(self.N)+" Manteldreiecken und einer "+self.elev_str+":")
        self.xy_points = [[math.cos(n*2*math.pi/self.N),math.sin(n*2*math.pi/self.N),0] for n in range(self.N)]
        if self.surface_elev != None:
            self.Z = math.sin(2*math.pi/self.N)*math.sqrt(((1/math.cos(self.surface_elev))**2-1)/(2*(1-math.cos(2*math.pi/self.N))))
            self.edge_elev = math.atan(self.Z)
        if self.edge_elev != None:
            self.Z = math.tan(self.edge_elev)
            self.surface_elev = math.acos(math.sqrt(1/(1+2*(1-math.cos(2*math.pi/self.N))*(self.Z/math.sin(2*math.pi/self.N))**2)))
        self.z_point = [0,0,self.Z]
        self.radius = 1
        self.basewidth = math.sqrt((self.xy_points[0][0]-self.xy_points[1][0])**2+(self.xy_points[0][1]-self.xy_points[1][1])**2)
        self.diagonal = math.sqrt((self.xy_points[0][0])**2+(self.xy_points[0][1])**2+(self.Z)**2)
        self.papercraft_angle = math.acos((self.xy_points[1][0]+self.Z**2)/(math.sqrt(self.Z**2+1)*math.sqrt(self.Z**2+self.xy_points[1][0]**2+self.xy_points[1][1]**2)))
        self.xy_papercraft_points = [[math.cos(n*self.papercraft_angle),math.sin(n*self.papercraft_angle)] for n in range(self.N+1)]
        print("   Winkel:")
        print("      Manteldreieckswinkel am Spitzenpunkt: "+str(180*self.papercraft_angle/math.pi)+"°")
        print("      Papiervorlagen-Bogenwinkel: "+str(self.N*180*self.papercraft_angle/math.pi)+"°")
        print("      Winkel der Bodensegmente am Ursprung: "+str(360/self.N)+"°")
        print("      Kantensteigung: "+str(180*self.edge_elev/math.pi)+"°")
        print("      Flächensteigung: "+str(180*self.surface_elev/math.pi)+"°")
        print("   Pyramidenpunkte:")
        for i in range(len(self.xy_points)):
            print("      Bodenpunkt-"+str(i+1)+" : "+str(self.xy_points[i]))
        print("      Spitzenpunkt : "+str(self.z_point))
        print("   Papiervorlage-Punkte:")
        for i in range(len(self.xy_papercraft_points)):
            print("      Punkt-"+str(i+1)+" : "+str(self.xy_papercraft_points[i]))
        print("      Ursprung : [0, 0]")
        print("   Dreiecksabstände normiert auf den RADIUS:") #standard
        print("      Radius : "+str(self.radius))
        print("      Basisbreite : "+str(self.basewidth))
        print("      Diagonale : "+str(self.diagonal))
        print("      Pyramidenhöhe : "+str(self.Z))
        print("   Dreiecksabstände normiert auf die BASISBREITE:")
        print("      Radius : "+str(self.radius/self.basewidth))
        print("      Basisbreite : "+str(1))
        print("      Diagonale : "+str(self.diagonal/self.basewidth))
        print("      Pyramidenhöhe : "+str(self.Z/self.basewidth))
        print("   Dreiecksabstände normiert auf die DIAGONALE:")
        print("      Radius : "+str(self.radius/self.diagonal))
        print("      Basisbreite : "+str(self.basewidth/self.diagonal))
        print("      Diagonale : "+str(1))
        print("      Pyramidenhöhe : "+str(self.Z/self.diagonal))
        print("   Dreiecksabstände normiert auf die HÖHE:")
        print("      Radius : "+str(self.radius/self.Z))
        print("      Basisbreite : "+str(self.basewidth/self.Z))
        print("      Diagonale : "+str(self.diagonal/self.Z))
        print("      Pyramidenhöhe : "+str(1))
    
    def plot_papercraft(self):
        plt.figure("2d plot der Papiervorlage der Manteldreiecke")
        paper = plt.axes(xlabel="x",ylabel="y")
        xy = self.xy_papercraft_points
        i = 0
        for p in xy:
            if i < self.N:
                paper.plot([xy[i][0],xy[i+1][0]],[xy[i][1],xy[i+1][1]],color="black")
            paper.plot([p[0],0],[p[1],0],color="black")
            i += 1
        paper.set_aspect("equal")
        plt.show()
    
    def plot_3d(self):
        plt.figure("3d plot der Pyramide mit "+str(self.N)+" Manteldreiecken")
        space = plt.axes(projection="3d",xlabel="x",ylabel="y",zlabel="z")
        space.grid()
        xy = self.xy_points
        z = self.z_point
        space.scatter(0,0,0,s=15,color="black",marker="+") #origin
        space.scatter(z[0],z[1],z[2],s=30,color="red",alpha=0.3)
        i = -1
        for p in xy:
            space.scatter(p[0],p[1],p[2],s=30,color="blue",alpha=0.3)
            space.plot([xy[i][0],xy[i+1][0]],[xy[i][1],xy[i+1][1]],[xy[i][2],xy[i+1][2]],color="blue")
            space.plot([p[0],z[0]],[p[1],z[1]],[p[2],z[2]],color="red")
            i += 1
        space.set_aspect("equal")
        plt.show()


#pyramid(sides=4,edge_elev=45).plot_3d() #example
#pyramid(sides=4,height=2).plot_papercraft() #example

pyr = pyramid(sides=14,surface_elev=45)
pyr.plot_3d()
pyr.plot_papercraft()
        
#con = cone(elev=60)
#con.plot_3d()
#con.plot_papercraft()

