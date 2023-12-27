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
    def action_to_del_coordinate(a):
        """ 0 for up, 1 for down, 2 for left, 3 for rigth"""
        if a == 0:
            return [0, 1]
        if a == 1:
            return [0, -1]
        if a == 2:
            return [-1, 0]
        if a == 3:
            return [1, 0]
        else:
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
        
# 设置图例
        ax.set_aspect('equal', adjustable='box')
        
       
        ax.grid()
        plt.xlim((-2, 6))
        plt.ylim((-2, 6))
        plt.xticks(np.arange(-2, 6, 1))
        plt.yticks(np.arange(-2, 6, 1))
        
        #plt.grid()
        
        plt.show()




# show_point(load_point())
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
        
    
    def number_points_in_disk(self, current_center):
        """calculate the number of points in the certain disks definded through param: (Point) current_center"""
        count_points = 0
        for point in self.points:
            if point.is_in_disk(current_center, self.radius):
                count_points += 1
                # point.print_point()
        return count_points

    def hard_code_implementation(self):
        """calculate every number of points covered by a disk centered on each each intersection"""
        number_points_list = []
        for intersection in self.intersections:
            number_points_list.append(self.number_points_in_disk(intersection))
        print(number_points_list)
        max_value = max(number_points_list)
        max_index = number_points_list.index(max_value)
        # max_intersection = self.intersections[max_index]
        # print(len(number_points_list))
        return max_index
    

    """For Q-learning"""
    def coordi_is_legal(self, coordi):
        
        for c in coordi:
            if c not in range(0, self.side_len+1):
                return False
        return True
                

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
    
    def initialize_one_disk_r(self):
        """ 
        initialize reward matrix for one disk
        state * action = 26 * 5 (25 + end, 4 + end)
        """
        r_mtx = np.zeros([self.state_size_one_disk, 5])
        for i in range(self.state_size_one_disk):
            for j in range(5):
                r_mtx[i, j] = self.calculate_r_one_disk(i, j)
        
        self.one_disk_r = r_mtx
    
    def update_one_disk_Q(self, s, a):
        self.one_disk_Q[s, a] = self.one_disk_r[s, a] + self.gamma * self.one_disk_Q[s].max()
        
    def one_disk_Q_learning(self):
        self.initialize_one_disk_r()
        actions = []
        for i in range(1000):
            s = random.randint(0, 24)
            for action in range(5):
                if self.one_disk_r[s, action] > -50:
                    actions.append(action)
            a = actions[random.randint(0, len(actions) - 1)]
            self.update_one_disk_Q(s, a)
        print(self.one_disk_Q)

    
    def one_disk_find_max(self):
        self.one_disk_Q_learning()
        state = 13
        print(f"the disk is on state:{state}")
        count = 0
        states = []
        while state != 25:
            states.append(state)
            if count > 20:
                print("fail")
                break

            q_max = self.one_disk_Q[state].max()


            q_max_action = np.argmax(self.one_disk_Q[state])
            
            new_state = self.state_to_new(state, q_max_action)

            if new_state != -1:
                state = new_state
            else:
                print("fail state!")
                break
            print(f"the disk move to state{state}")
        max_index = states[-1]
        Functions.show_coverd_state(self.intersections[max_index], self.radius, self.points)
        # plt.imshow(self.one_disk_Q ,cmap='hot',interpolation='nearest')
        # plt.show()
            



    def test_block(self):
        test_point = self.points[0]
        test_intersection = self.intersections[1]
        # print(f"square of distances:{Functions.calculate_square_distance(test_point, test_intersection)}")
        # print(self.number_points_in_disk(test_intersection))
        # Functions.show_coverd_state([test_intersection, self.intersections[2]], self.radius, self.points)
        max_index = self.hard_code_implementation()
        # Functions.show_coverd_state(self.intersections[max_index], self.radius, self.points)
        # print(self.Q_one_disk(5, 3))
        self. initialize_one_disk_r()
        print(self.one_disk_r)
        print(self.one_disk_Q[0].max())

        
            

square = Square()
# Functions.show_point(square.points)
# square.test_block()
# square.hard_code_implementation()
# square.one_disk_Q_learning()
square.one_disk_find_max()



