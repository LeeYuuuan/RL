from typing import Union
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import random

class Point:
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def print_point(self):
        """print the coordinate of the point."""
        print(f"{self.x},{self.y}")
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def is_in_disk(self, disk_center, disk_radius):
        """if point is covered by disk

        Args:
            disk_center (Point): disk center point.
            disk_radius (float): radius of the disk.

        Returns:
            Bool: return True if disk covers the point, vice versa.
        """
        distance_square = Functions.calculate_square_distance(self, disk_center)
        if distance_square < (disk_radius ** 2): # the inequality sign depends on how to defind "cover"
            return True
        else:
            return False
        
    def is_in_two_disks(self, disk_center_1, disk_center_2, disk_radius):
        """
        if point is coverd by two disks.
        return:
            Bool: True if disks cover the point.
        """
        distance_square_1 = Functions.calculate_square_distance(self, disk_center_1)
        distance_square_2 = Functions.calculate_square_distance(self, disk_center_2)
        if distance_square_1 < (disk_radius ** 2) or distance_square_2 < (disk_radius ** 2):
            return True
        else:
            return False
        

class Functions:
    
    @staticmethod
    def show_point(point_list):
        x_list = []
        y_list = []
        for p in point_list:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        plt.xlim((-2, 6))
        plt.ylim((-2, 6))
        plt.xticks(np.arange(-2, 6, 1))
        plt.yticks(np.arange(-2, 6, 1))
        plt.scatter(x_list, y_list)
        plt.grid()
        plt.show()
    
    @staticmethod
    def print_point_list(point_list):
        """print the coordinates of all points."""
        for p in point_list:
            p.print_point()
    
    @staticmethod
    def calculate_square_distance(point_1: Point, point_2: Point) -> float:
        """calculate distance between point_1 and point_2."""
        return (point_1.get_x() - point_2.get_x()) ** 2 + (point_1.get_y() - point_2.get_y()) **2
    
    
    @staticmethod
    def show_disk(current_center: Point, radius):
        
        disk = plt.Circle((current_center.get_x(),current_center.get_y()),radius)
        plt.gca().add_patch(disk)
        plt.show()
    
    @staticmethod
    def show_coverd_state(current_center: Union[Point, list], radius, point_list):

        x_list = []
        y_list = []
        for p in point_list:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        
        fig, ax = plt.subplots()
        plt.scatter(x_list, y_list, s=10)
        if isinstance(current_center, list):
            # print(type(current_center))
            disk_r = Circle((current_center[0].get_x(),current_center[0].get_y()),radius, color="r", alpha=0.5)
            disk_b = Circle((current_center[1].get_x(),current_center[1].get_y()),radius, color="b", alpha=0.5)
            ax.add_patch(disk_r)
            ax.add_patch(disk_b)
            text_str = f"rad disk: {square.number_points_in_disk(current_center[0])}\nblue disk: {square.number_points_in_disk(current_center[1])}"
            ax.text(1.1, 0.5, text_str, transform=ax.transAxes, verticalalignment='center', fontsize=10)


        else:
            disk = plt.Circle((current_center.get_x(),current_center.get_y()),radius, color="r", alpha=0.5)
            ax.add_patch(disk)
            text_str = f"points: {square.number_points_in_disk(current_center)}"
            ax.text(1.1, 0.5, text_str, transform=ax.transAxes, verticalalignment='center', fontsize=10)

        # plt.gca().add_patch(disk)
        
        ax.set_aspect('equal', adjustable='box')
        
       
        ax.grid()
        plt.xlim((-2, 6))
        plt.ylim((-2, 6))
        plt.xticks(np.arange(-2, 6, 1))
        plt.yticks(np.arange(-2, 6, 1))
        
        #plt.grid()
        
        plt.show()

class Square:
    def __init__(self, side_len=4, divided_len=1, radius=1.2, gamma=0.8):
        self.side_len = side_len
        self.divided_len = divided_len
        self.radius = radius

        self.intersections = []
        self.points = [] 
        self.load_intersections()
        self.load_points()

        # q-learning
        self.gamma = gamma
        self.one_disk_r = None
        self.state_size_one_disk = len(self.intersections) + 1 # s= 25: "end" state.
        self.one_disk_Q = np.zeros([self.state_size_one_disk, 5])


square = Square()
        
    

