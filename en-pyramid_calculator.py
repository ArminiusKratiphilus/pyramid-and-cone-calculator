#pyramid calculator by https://github.com/users/ArminiusKratiphilus
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
            self.elev_str = "height: "+str(self.height)
            self.Z = self.height
        elif self.elev != None and self.height == None:
            self.elev_str = "slope "+str(self.elev)+"°"
            self.elev = math.pi*float(self.elev)/180
        else:
            raise ImpossibleBodyError("slope or height must be defined",(elev,height))
            
        if self.height != None:
            if self.Z < 0:
                raise ImpossibleBodyError("height of cone can't be less than 0",height)
        if self.elev != None:
            if self.elev >= 90 or self.elev < 0:
                raise ImpossibleBodyError("slope angle must be in the interval [0,90)",elev)
        
        print("\ncone with "+self.elev_str+":")
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
        print("   angles:")
        print("      papercraft arc angle: "+str(180*self.papercraft_angle/math.pi)+"°")
        print("      papercraft arc angle in rad: "+str(self.papercraft_angle))
        print("      pitch angle: "+str(180*self.elev/math.pi))
        print("   cone points:")
        #for i in range(len(self.xy_points)):
        #    print("      ground point "+str(i+1)+" : "+str(self.xy_points[i]))
        print("      tip point : "+str(self.z_point))
        print("   papercraft point:")
        #for i in range(len(self.xy_papercraft_points)):
        #    print("      Punkt-"+str(i+1)+" : "+str(self.xy_papercraft_points[i]))
        print("      origin : [0, 0]")
        print("   lenghts normed by RADIUS:") #standard
        print("      radius : "+str(self.radius))
        print("      height : "+str(self.Z))
        print("      diagonal : "+str(self.diagonal))
        print("   lenghts normed by HEIGHT:")
        print("      radius : "+str(self.radius/self.Z))
        print("      height : "+str(1))
        print("      diagonal : "+str(self.diagonal/self.Z))
        print("   lenghts normed by DIAGONAL:")
        print("      radius : "+str(self.radius/self.diagonal))
        print("      height : "+str(self.Z/self.diagonal))
        print("      diagonal : "+str(1))
        
    def plot_papercraft(self):
        plt.figure("2d plot of the cone papercraft stencil")
        paper = plt.axes(xlabel="x",ylabel="y")
        xy = self.xy_papercraft_points
        for i in range(len(xy)-1):
            paper.plot([xy[i][0],xy[i+1][0]],[xy[i][1],xy[i+1][1]],color="black")
        paper.plot([xy[0][0],0],[xy[0][1],0],color="black")
        paper.plot([xy[-1][0],0],[xy[-1][1],0],color="black")
        paper.set_aspect("equal")
        plt.show()
    
    def plot_3d(self):
        plt.figure("3d of the cone")
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
            self.elev_str = "height "+str(self.height)
            self.Z = self.height
        elif self.surface_elev == None and self.edge_elev != None and self.height == None:
            self.elev_str = "edge slope "+str(self.edge_elev)+"°"
            self.edge_elev = math.pi*float(self.edge_elev)/180
        elif self.surface_elev != None and self.edge_elev == None and self.height == None:
            self.elev_str = "surface slope "+str(self.surface_elev)+"°"
            self.surface_elev = math.pi*float(self.surface_elev)/180
        else:
            raise ImpossibleBodyError("a slope or a height must be defined",(surface_elev,edge_elev,height))
            
        if self.N <= 2:
            raise ImpossibleBodyError("a pyramid can't have few than three mantle triangles",sides)
        if self.height != None:
            if self.Z < 0:
                raise ImpossibleBodyError("pyramid height can't be less than 0",height)
        if self.edge_elev != None:
            if self.edge_elev >= 90 or self.edge_elev < 0:
                raise ImpossibleBodyError("slope angle must be in the interval [0,90)",edge_elev)
        if self.surface_elev != None:
            if self.surface_elev >= 90 or self.surface_elev < 0:
                raise ImpossibleBodyError("slope angle must be in the interval [0,90)",surface_elev)
            
        print("\npyramid with "+str(self.N)+" mantle triangles and "+self.elev_str+":")
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
        print("   angles:")
        print("      mantle triangle angle at the tip: "+str(180*self.papercraft_angle/math.pi)+"°")
        print("      papercraft arc angle: "+str(self.N*180*self.papercraft_angle/math.pi)+"°")
        print("      angle of the ground segments at the origin: "+str(360/self.N)+"°")
        print("      edge slope: "+str(180*self.edge_elev/math.pi)+"°")
        print("      surface slope: "+str(180*self.surface_elev/math.pi)+"°")
        print("   pyramid points:")
        for i in range(len(self.xy_points)):
            print("      ground point "+str(i+1)+" : "+str(self.xy_points[i]))
        print("      tip point : "+str(self.z_point))
        print("   papercraft points:")
        for i in range(len(self.xy_papercraft_points)):
            print("      point "+str(i+1)+" : "+str(self.xy_papercraft_points[i]))
        print("      origin : [0, 0]")
        print("   triangle lengths normed by RADIUS:") #standard
        print("      radius : "+str(self.radius))
        print("      base width : "+str(self.basewidth))
        print("      diagonal : "+str(self.diagonal))
        print("      pyramid height : "+str(self.Z))
        print("   triangle lengths normed by BASE WIDTH:")
        print("      radius : "+str(self.radius/self.basewidth))
        print("      base width : "+str(1))
        print("      diagonal : "+str(self.diagonal/self.basewidth))
        print("      pyramid height : "+str(self.Z/self.basewidth))
        print("   triangle lengths normed by DIAGONAL:")
        print("      radius : "+str(self.radius/self.diagonal))
        print("      base width : "+str(self.basewidth/self.diagonal))
        print("      diagonal : "+str(1))
        print("      pyramid height : "+str(self.Z/self.diagonal))
        print("   triangle lengths normed by HEIGHT:")
        print("      radius : "+str(self.radius/self.Z))
        print("      base width : "+str(self.basewidth/self.Z))
        print("      diagonal : "+str(self.diagonal/self.Z))
        print("      pyramid height : "+str(1))
    
    def plot_papercraft(self):
        plt.figure("2d plot of the mantle triangles' papercraft")
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
        plt.figure("3d plot of the pyramid with "+str(self.N)+" mantle triangles")
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

