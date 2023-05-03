from abc import ABC, abstractmethod


class Order(ABC):
  """
  Attributes
----------
name: str
    The name of the item in the order.
price: float
    The price of the item in the order.
address: str
    The address of the order entered by the user.
    
Methods
-------
calculatePrice(discount: float)
    Abstract method to calculate the total price of the order, taking into account any discount.
getCombo() -> str
    Abstract method to return the combo item associated with the order.
getPrice() -> float
    Returns the total price of the item in the order.
getAddress() -> str
    Returns the order address entered by the user.
getName() -> str
    Returns the name of the item in the order.
  """

  def __init__(self, name: str, price: float, address: str, discount: float,
               id: str):
    """
      Constructor to build a Order object

      Attributes
      ----------
      name: str
  	    The name of the order
      price: float
  	    The price of the order
      address : str
  	    The address of the order entered by the user
      
    """
    # Toppings set is protected so healthy burger class can also start with a default topping, calling the addTopping() function won't work as the toppings will be written in the file whenever a burger read and created in the transactions.txt file, this will lead to the same toppings being written every time the user starts the program.
    self._name = name
    self._price = price
    self.calculatePrice(discount)
    self._address = address
    self.id = id

    super().__init__()

  #calculateprice is seperate from getprice, as calculateprice is used for calculating the total price of all burgers bought by a user ( in the function calReward()) and it is also used for showing the user the price of the burger they ordered. If the user wants to cash in reward points and get a discount, the discounted price will be shown to the user, but not when calculating the reward points as the discount parameter wont be passed in in the calLoyalty method. Therefore calculating price will set the price of the burger, including the discount, and get price willget the completed price, without any parameters being needed to pass in.
  @abstractmethod
  def calculatePrice(self, discount):
    '''
	Calculates the total price of the order
	Parameters
	----------
	discount : float
		The discount of the order, the value can be 0 if there is no discount
	Returns
	-------
	None
 
	Raises
	------
	TypeError
    if discount is not a float and the method attempts to add discount to self._price:float
	  '''
    return

  def getPrice(self) -> float:
    """
        Returns the total price of the order

        Returns
        ______
        The total price of the order
    """

    return float(self._price if self._price > 0 else 0)

  def getAddress(self):
    """
        Returns order address entered by the user

        Returns
        _______
        The order address entered by the user
    """
    return self._address

  def getName(self):
    """
        Returns name of the order

        Returns
        _______
        name of the order
    """
    return self._name
