from Order import Order


class SalesCalculator():
  TIPS_PERCENTAGE = 0.13
  """
    Class for calculating sales
    Attributes
    ----------
    order_list:Hamburger 
	    A list of burger objects
    Methods
    -------
    calDeliverySalary(self,tips:float,flat_rate:float)->float
      Calculates and returns the amount in dollars the delivery person will earn after completing all orders
    calReward()->int
      calculates and returns the reward points earned by the customer based on their amount spent on this restaurant
  """

  def __init__(self, order_list: list[Order]):
    """
      Constructor for SalesCalculator class

      Args:
            burgers: list of Burger objects
    """
    self.__order_list = order_list

  def calDeliverySalary(self, flat_rate: float) -> float:
    """
      Calculates the amount in dollars the delivery person will make after completing all orders 
      
      Parameter
      ________
      flat_rate: amount delivery person will recieve per delivery
      Returns
      _______
       float: The amount in dollars the delivery person will earn after delivering all the orders
      Raises
      _____
      TypeError:
        if tips or flat_rate is not a float value and the method attempts to add it to salary:float 
      AttributeError:
        If the getPrice() method in the Hamburger class is non-existent 
    """
    salary = flat_rate
    if len(self.__order_list)==0:
      salary=0
    for b in self.__order_list:
      #see if it is a burger (has setside method)
      try:
        #see if it has a side
        if b.getSide()!=None:
          #add combo price instead
          salary+=13
      except: 
        salary += b.getPrice() + b.getPrice() * self.TIPS_PERCENTAGE
    return "{:.2f}".format(salary)

  def calReward(self) -> int:
    """
     calculates and returns the reward points earned by the customer based on their amount spent on this restaurant

      Returns
      _______
            int: the reward points earned by the customer
      Raises:
      AttributeError:
        If the getPrice() method in the Hamburger class is non-existent 
      
    """
    reward = 0
    for b in self.__order_list:
      reward += b.getPrice() * 2
    return int(reward)
