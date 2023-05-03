# [0] is price
#[1] is healthiness
from enum import Enum
class Topping(Enum):
  """
  A Topping enum that holds the toppings that can be added to a burger. 
  Each Topping member is represented as a tuple with the price value as the first element and the healthiness value as the second element
  """
  # ABSTRACT DATA TYPES Using tuples because values are constant 
  chicken = (3, 0.7)
  tomato = (1.0, 0.8)
  bacon = (1.5, -0.5)
  flaxseed = (0.5, 1.0) 
  lettuce=(0.3,1.0)#default topping in healthy burger
  cheese=(0.5,-0.3)
  egg=(1.0,0.5)#default topping in healthy burger and basic burger
