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
            26 --> (1, 1)
        """
        if index >= 0 and index < (25 * 25):
            return (index // 25, index % 25)
        
        return -1
    
    @staticmethod
    def state_tuple_to_index(tp: tuple):
        """
        inverse function of 
            state_index_to_tuple(index: int).
        eg:
            (1, 1) --> 26
        """
        x = tp[0]
        y = tp[1]
        if x in range(25) and y in range(25):
            return x * 25 + y
        return -1
    
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
        x = tp[0]
        y = tp[1]
        if x in range(5) and y in range(5):
            return x * 5 + y
        return -1     
    
    
    @staticmethod
    def show_disk(current_center: Point, radius):
        
        disk = plt.Circle((current_center.get_x(),current_center.get_y()),radius)
        plt.gca().add_patch(disk)
        plt.show()
    
    @staticmethod
    def show_coverd(current_center, radius, point_list):
        x_list = []
        y_list = []
        for p in point_list:
            x_list.append(p.get_x())
            y_list.append(p.get_y())
        
        fig, ax = plt.subplots()
        plt.scatter(x_list, y_list, s=10)
        disk_r = Circle((current_center[0].get_x(),current_center[0].get_y()),radius, color="r", alpha=0.5)
        disk_b = Circle((current_center[1].get_x(),current_center[1].get_y()),radius, color="b", alpha=0.5)
        ax.add_patch(disk_r)
        ax.add_patch(disk_b)
        text_str = f"points: {square.number_points_in_disks(current_center[0], current_center[1])}"
        ax.text(1.1, 0.5, text_str, transform=ax.transAxes, verticalalignment='center', fontsize=10)
        ax.set_aspect('equal', adjustable='box')
        
       
        ax.grid()
        plt.xlim((-2, 6))
        plt.ylim((-2, 6))
        plt.xticks(np.arange(-2, 6, 1))
        plt.yticks(np.arange(-2, 6, 1))
        
        #plt.grid()
        
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

        """two disks"""
        self.states = [] # for two disks, there are 25 * 25 states.
        self.actions = [] # 5 * 5 actions.
        
        
        self.initialize_two_disks()
        self.states_size = len(self.states)
        self.actions_size = len(self.actions)
        self.r = np.zeros([len(self.states), len(self.actions)])
        self.initilize_r()
        self.Q = np.zeros_like(self.r)
    
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
        if s in range(self.state_size_one_disk - 1) and a in range(5):
            if a == 4:
                return s 
            if a == 0 and s % 5 != 4:
                return s + 1
            if a == 1 and s % 5 != 0:
                return s - 1
            if a == 2 and s not in range(0, self.side_len+1):
                return s - self.side_len - 1
            if a == 3 and s not in range(self.state_size_one_disk-self.side_len-1, self.state_size_one_disk):
                return s + self.side_len + 1    
            
        
        return -1
    
    def two_disks_states_to_new(self, s, a):
        if s in range(self.states_size) and a in range(self.actions_size):
            s1, s2 = Functions.state_index_to_tuple(s)
            a1, a2 = Functions.action_index_to_tuple(a)
            # print(s1, s2)
            # print(a1, a2)
        s1_new = self.state_to_new(s1, a1)
        s2_new = self.state_to_new(s2, a2)
        # print(s1_new, s2_new)
        
        s_new = Functions.state_tuple_to_index((s1_new, s2_new))
        return s_new


    def calculate_r(self, s, a):
        state_1, state_2 = Functions.state_index_to_tuple(s)
        new_state = self.two_disks_states_to_new(s, a)
        if new_state == -1:
            return -100
        # print(type(new_state))
        new_state_1, new_state_2 = Functions.state_index_to_tuple(new_state)


  
        return self.number_points_in_disks(self.intersections[new_state_1], self.intersections[new_state_2]) - self.number_points_in_disks(self.intersections[state_1], self.intersections[state_2])
        
    
    def initilize_r(self):
        for i in range(self.states_size):
            for j in range(self.actions_size):
                self.r[i, j] = self.calculate_r(i, j)
        # print(self.r)


                
    def initialize_two_disks(self):
        """
        states = [(i, j), ...]
            i = index of the 1st center in the list[]: intersections
            j = index of the 2nd center in the list[]: intersections
        
        actions = [(i, j), ...]
            action, 0, 1, 2, 3: for Up, down, left, right
            4 for end.
        """
        for i in range(self.state_size_one_disk - 1):
            for j in range(self.state_size_one_disk - 1):
                self.states.append((i, j))
        
        for i in range(5):
            for j in range(5):
                self.actions.append((i, j))

    def update_Q(self, s, a):
        self.Q[s, a] = self.r[s, a] + self.gamma * self.Q[s].max()
        
    def Q_learning(self):
        actions = []
        for i in range(100000):
            s = random.randint(0, self.states_size - 1)
            for action in range(self.actions_size):
                if self.r[s, action] > -50:
                    actions.append(action)
            a = actions[random.randint(0, len(actions) - 1)]
            self.update_Q(s, a)
        print(self.Q)

    def find_max(self):
        self.Q_learning()
        state = 600
        print(f"the disk is on state:{state}")
        count = 0
        states = []
        for i in range(20):
            states.append(state)
            if count > 20:
                print("fail")
                break

            q_max = self.Q[state].max()


            q_max_action = np.argmax(self.Q[state])
            
            new_state = self.two_disks_states_to_new(state, q_max_action)

            if new_state != -1:
                state = new_state
            else:
                print("fail state!")
                break
            print(f"the disk move to state{state}")
        max_index = states[-1]
        print(max_index)
        max_index_1, max_index_2 = Functions.state_index_to_tuple(max_index)
        Functions.show_coverd([self.intersections[max_index_1], self.intersections[max_index_2]], self.radius, self.points)
    


    

    




square = Square()
square.find_max()


    

