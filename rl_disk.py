import numpy as np
from matplotlib import pyplot as plt



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
  



# show_point(load_point())
class Square:
    def __init__(self, side_len=4, divided_len=1, radius=1.2):
        self.side_len = side_len
        self.divided_len = divided_len
        
        self.intersections = []
        self.points = [] 
        self.load_intersections()
        self.load_points()
        
    
    def load_intersections(self):
        """Load intersection points of the square area."""
        intersections = []
        for i in range(0, self.side_len, self.divided_len):
            for j in range(0, self.side_len, self.divided_len):
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
        
    
    def calculate_points_in_disk(self, current_center):
        for point in self.points:
            

Functions.show_point(Square().points)