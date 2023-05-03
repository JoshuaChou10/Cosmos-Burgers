from Topping import Topping
from Order import Order
from sides import Fries, Sushi


class Hamburger(Order):
  BASE_PRICE = 10.0
  '''
    A Hamburger object that hold the toppings, address and name of the burger
    Attributes
    ----------
    toppings: Set[Topping]
	    The toppings the burger is comprised of
    address : str
	    The address of the order entered by the user
    side:Order
      The side of the burger
    name: str
	    The name of the burger "Basic Burger"
    Methods
    -------
    calculatePrice()
	    Calculates and sets the price of the burger
    getPrice() -> float
	    returns the total price of the burger
    stringToppings() -> str
	    returns a string of the burger toppings
    getToppings() -> set[Topping]
	    returns the set of toppings in the burger
    getAddress()->str
      returns the address of the order
    getName()->str
      returns the name of the burger
    addTopping(topping:Topping)->bool
      Attempts to add a topping to the burger
      
    '''

  def __init__(self,
               toppings: set[Topping],
               address: str,
               discount: int,
               side: str,
               id:str,
               name: str = "Hamburger"):
    """
      Constructor to build a Hamburger object

      Attributes
      ----------
      toppings: Set[Topping]
  	     The toppings the burger is comprised of
      address : str
  	    The address of the order entered by the user
      side:str
        The side with the burger
      name: str
  	    The name of the burger "Basic Burger"
    """
    self._toppings = toppings
    # Toppings set is protected so healthy burger class can also start with a default topping, calling the addTopping() function won't work as the toppings will be written in the file whenever a burger read and created in the transactions.txt file, this will lead to the same toppings being written every time the user starts the program.
    self._toppings.add(Topping.egg)
    self.side = self.setSide(side)
    super().__init__(
      name, 10.0, address, discount,id
    )  #price starts at 0, base price is used to calculate it each time a topping is added

  #calculateprice is seperate from getprice, as calculateprice is used for calculating the total price of all burgers bought by a user ( in the function calReward()) and it is also used for showing the user the price of the burger they ordered. If the user wants to cash in reward points and get a discount, the discounted price will be shown to the user, but not when calculating the reward points as the discount parameter wont be passed in in the calLoyalty method. Therefore calculating price will set the price of the burger, including the discount, and get price willget the completed price, without any parameters being needed to pass in.
  def calculatePrice(self, discount):
    '''
	Calculates the total price of the burger with it's toppings and discount
	This will increase the value of self._price and will decrease the value of discount to   self._price
	Parameters
	----------
	discount : float
		The discount of the burger, the value can be 0 if there is no discount
	Returns
	-------
	None
 
	Raises
	------
	TypeError
    if discount is not a float and the method attempts to add discount to self._price:float
	  '''
    price = self.BASE_PRICE
    for topping in self.getToppings():
      price += topping.value[0]
    price -= discount
    self._price = price

  def stringToppings(self) -> str:
    """
        Returns a string of the burger toppings

        Returns
        _______
        burger toppings seperated by commas
    """
    toppingList = ""
    for t in self._toppings:
      if t != None:
        toppingList += t.name + ", "
      if toppingList == "":
        toppingList = "no toppings"
    return toppingList.rstrip(', ')

  def getToppings(self) -> set[Topping]:
    """
        Returns the set of toppings in the burger

        Returns
        _______
        set of toppings in the burger
    """
    return self._toppings

  def addTopping(self, topping: Topping) -> bool:
    """
        Attempts to add a topping to the self.__topping set of the burger and write the order in te transactions.txt file
        Parameters
        _________
        topping:Topping
          Topping enum member to add to the burger. If the Topping is already in the set the           method will return false, otherwise it will return true
        Returns
        ______
        bool
              True if method was succesful
              False if method attempted to add an already existing topping to the set
        Raise
        _____
        TypeError
          If the topping parameter is not an instance of the Topping enum class.
        IOError
          If the transactions.txt file could not be opened or written.
        PermissionError
          If the transactions.txt file could not be opened due to permission issues or o               ther system-related errors.
  
    """
    if topping in self._toppings:
      print(f"{topping.name} is already in toppings list")
      return False
    self._toppings.add(topping)
    self.calculatePrice(0)
    with open("transactions.txt", 'a') as Tfile:
      Tfile.write(f",{topping.name}")
    return True
  def setSide(self, side:str):
    """
        Sets the side of the burger if there is a combo

        Raises
        ValueError
          if parameter is neither sushi or fries
        Returns
        None
    """
    set_side=None
    if side == "sushi":
      set_side=Sushi(False, "snack", "", 0,None) # no id needed for the side, id is only needed to se if delivery person delivered a certain order as of May 2
    elif side == "fries":
      set_side= Fries(20, "", 0,None)
    return set_side

  def getSide(self):
    """
    simple method to get side of burger
    """
    return self.side
    
  def __str__(self) -> str:
    """
        Returns a string representation of the burger

        Returns
        string representation of the burger
    """
    # print(self.side)
    
    return f"{self._name} with {self.stringToppings()} for {self._price} {'with ' +   self.side._name + ' COMBO for only $14' if self.side!=None else ''}"

  

class HealthyBurger(Hamburger):
  BASE_PRICE = 11
  """
        A HealthyBurger (subclass of Hamburger) object that hold the toppings, address, and name of the burger

        Attributes
        ----------
        price:float
          The price of the burger
        healthinessLvl: float
            The name of the burger "Healthy Burger"
            
        Methods
        -------
        calculateHealthiness()->float
          Calculates the healthiness level of the healthy burger by summing the healthy                ratings of all of its toppings.
        addTopping(topping:Topping)->bool <<override>>
            Attempts to add a topping to the burger if it is healthy 
  """

  def __init__(self, toppings, address, side, name="Healthy Burger"):
    """
      Constructor for HealthyBurger class

      Args:
          toppings: set of Topping enum members
          address: string representing the order address
    """
    # fitler any unhealthy toppings.
    for member in toppings:
      if member.value[1] < 0:
        print(f"can't add {member.name} to healthy burger ")
    toppings = {t for t in toppings if t.value[1] >= 0}
    #pass arguments into super constructor
    super().__init__(toppings, address, 0, side, name)
    #setting default instances
    self._toppings.add(Topping.lettuce)
    self.__healthinessLvl = 0
    self._price = 11.0
    #higher price than basic reflects healthier ingredients

  def calculateHealthiness(self) -> float:
    """
    Calculates the healthiness level of the healthy burger by summing the healthy ratings of all of its toppings.

    Returns
    ______
    float
          the healthiness level of the healthy burger, which is a sum of the healthy                 ratings of all of its toppings.

    """
    for topping in self.getToppings():
      self.__healthinessLvl += topping.value[1]
    return float(self.__healthinessLvl)

  #polymorphism is used
  def addTopping(self, topping: Topping):
    """
    Adds a topping to the burger if it is not considered unhealthy.

    Parameter
    ________
    topping: Topping
            A Topping object to be added to the burger.

    Returns
    ______
    bool
        True if the topping is added successfully, False otherwise.
    Override: 
    This method overrides the addTopping method in the Burger class. If the topping's     unhealthy rating (indicated by its second value) is less than 0, then it cannot be added to a healthy burger and the method returns False. Otherwise, the method calls the addTopping method of the superclass to add the topping to the burger.
    """
    if topping.value[1] < 0:
      print(f"Can't add {topping.name} to a healthy burger")
      return False
    return super().addTopping(topping)
