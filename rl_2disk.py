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
    def state_index_to_tuple(index: int):
        """
        index --> tuple
        eg:
            27 --> (1, 1)
        """
        if index >= 0 and index < (26 * 26):
            return (index // 26, index % 26)
        
        return False
    
    @staticmethod
    def state_tuple_to_index(tp: tuple):
        """
        inverse function of 
            state_index_to_tuple(index: int).
        eg:
            (1, 1) --> 27
        """
        index = tp[0] * 26 + tp[1]
        if index >= 0 and index < (26 * 26):
            return index
        return False
    
    @staticmethod
    def action_index_to_tuple(index: int):
        """
        eg:
            6 --> (1, 1)
        """
        if index >= 0 and index < (5 * 5):
            return (index // 5, index % 5)
    
    @staticmethod
    def action_tuple_to_index(tp: tuple):
        """
        eg:
            (1, 1) --> 6
        """
        index = tp[0] * 5 + tp[1]
        if index >= 0 and index < (5 * 5):
            return index
        return False     
    
    
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
        self.states = [] # for two disks, there are 25 * 25 states.
        self.actions = []
        self.gamma = gamma
        self.one_disk_r = None
        self.state_size_one_disk = len(self.intersections) + 1 # s= 25: "end" state.
        self.one_disk_Q = np.zeros([self.state_size_one_disk, 5])

        """two disks"""
        self.r = None
    
    def load_intersections(self):
        """Load intersection points of the square area."""
        intersections = []
        for i in range(0, self.side_len+1, self.divided_len):
            for j in range(0, self.side_len+1, self.divided_len):
                intersections.append(Point(i, j))
        self.intersections = intersections
    
    def load_points(self, point_pth="UserDistribution.txt"):
        """load point from txt.

        Args:
            point_pth (str): file path.
        """
        points = []
        with open(point_pth, 'r') as f:
            for line in f.readlines():
                if len(line.strip()) == 11:
                    points.append(Point(line.strip()[0:4], line.strip()[7:11]))
        
        self.points = points
    
    def number_points_in_disks(self, current_center_1, current_center_2):
        """calculate the number of points in the certain disks definded through param: (Point) current_center"""
        count_points = 0
        for point in self.points:
            if point.is_in_two_disks(current_center_1, current_center_2, self.radius):
                count_points += 1
                # point.print_point()
        return count_points
    
    def state_to_new(self, s, a):
        """ 
        0 for up,
        1 for down, 
        2 for left, 
        3 for rigth
        4 for end"""
        if s in range(self.state_size_one_disk) and a in range(5):
            if a == 4 or s == 25:
                return 25
            if a == 0 and s % 5 != 4:
                return s + 1
            if a == 1 and s % 5 != 0:
                return s - 1
            if a == 2 and s not in range(0, self.side_len+1):
                return s - self.side_len - 1
            if a == 3 and s not in range(self.state_size_one_disk-self.side_len-1, self.state_size_one_disk):
                return s + self.side_len + 1    
            
        
        return -1


    def calculate_r_one_disk(self, s, a):
        """calculate Q.

        Args:
            s (int): state, which is the index of intersection.
            a (int): action, 0, 1, 2, 3: for Up, down, left, right
        
        Return:
            float: return r value.
        """
        if s in range(self.state_size_one_disk) and a in range(5):
            new_state = self.state_to_new(s, a)
            if new_state == 25:
                return 0
            
            if new_state != -1:
                return self.number_points_in_disk(self.intersections[new_state]) - self.number_points_in_disk(self.intersections[s])

        return -100
    
    def initialize_two_disks(self):
        """
        states = [(i, j), ...]
            i = index of the 1st center in the list[]: intersections
            j = index of the 2nd center in the list[]: intersections
        
        actions = [(i, j), ...]
            
        """
        for i in range(self.state_size_one_disk):
            for j in range(self.state_size_one_disk):
                self.states.append((i, j))
        
        for i in range(5):
            for j in range(5):
                self.actions.append((i, j))


        r = np.zeros([len(self.states), len(self.actions)])


square = Square()
print(Functions.action_index_to_tuple(6))
print(Functions.action_tuple_to_index((1, 1)))
        
    

