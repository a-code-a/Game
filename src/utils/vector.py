"""
Vector utility class for 2D vector operations.
"""
import math


class Vector2:
    """A 2D vector class for position, velocity, and direction calculations."""
    
    def __init__(self, x=0.0, y=0.0):
        """Initialize a new Vector2 object.
        
        Args:
            x (float): The x component of the vector.
            y (float): The y component of the vector.
        """
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        """Add two vectors.
        
        Args:
            other (Vector2): The vector to add.
            
        Returns:
            Vector2: A new vector that is the sum of this vector and other.
        """
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtract a vector from this vector.
        
        Args:
            other (Vector2): The vector to subtract.
            
        Returns:
            Vector2: A new vector that is the difference of this vector and other.
        """
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiply this vector by a scalar.
        
        Args:
            scalar (float): The scalar to multiply by.
            
        Returns:
            Vector2: A new vector that is this vector scaled by scalar.
        """
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """Divide this vector by a scalar.
        
        Args:
            scalar (float): The scalar to divide by.
            
        Returns:
            Vector2: A new vector that is this vector divided by scalar.
        """
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other):
        """Check if two vectors are equal.
        
        Args:
            other (Vector2): The vector to compare with.
            
        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        """Return a string representation of this vector.
        
        Returns:
            str: A string representation of this vector.
        """
        return f"Vector2({self.x}, {self.y})"
    
    def __repr__(self):
        """Return a string representation of this vector.
        
        Returns:
            str: A string representation of this vector.
        """
        return self.__str__()
    
    def length(self):
        """Calculate the length (magnitude) of this vector.
        
        Returns:
            float: The length of this vector.
        """
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def length_squared(self):
        """Calculate the squared length of this vector.
        
        This is faster than length() when you just need to compare lengths.
        
        Returns:
            float: The squared length of this vector.
        """
        return self.x * self.x + self.y * self.y
    
    def normalize(self):
        """Normalize this vector (make it a unit vector).
        
        Returns:
            Vector2: A new vector that is the normalized version of this vector.
        """
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
    
    def distance_to(self, other):
        """Calculate the distance between this vector and another.
        
        Args:
            other (Vector2): The other vector.
            
        Returns:
            float: The distance between this vector and other.
        """
        return (other - self).length()
    
    def dot(self, other):
        """Calculate the dot product of this vector and another.
        
        Args:
            other (Vector2): The other vector.
            
        Returns:
            float: The dot product of this vector and other.
        """
        return self.x * other.x + self.y * other.y
    
    def to_tuple(self):
        """Convert this vector to a tuple.
        
        Returns:
            tuple: A tuple (x, y) representing this vector.
        """
        return (self.x, self.y)
    
    def to_int_tuple(self):
        """Convert this vector to a tuple of integers.
        
        Returns:
            tuple: A tuple (int(x), int(y)) representing this vector.
        """
        return (int(self.x), int(self.y))
