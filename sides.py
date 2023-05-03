from Order import Order;
class Fries(Order):
  """
  A Fries Object that holds the amount and the address of the fries

  Attributes
  _________
  amount: int
  	    The number of fries the user orders
  address : str
  	    The address of the order entered by the user
  
  """
  def __init__(self,amount:int,address:str,discount:float,id:str):
    """
      Constructor to build a Fries object

      Attributes
      ----------
      amount: int
  	    The number of fries the user orders
      address : str
  	    The address of the order entered by the user
      
    """
    self.__amount=amount
    super().__init__("Fries",0.1,address,discount,id)

  def calculatePrice(self,discount):
    '''
	Calculates the total price of the order by multiplying the amount of fries by the cost of a single fry, then subtracting the discount
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
    self._price*=self.__amount
    self._price-=discount
  # def getCombo()->str:
  #   return "Hamburger" # to be passed in to the createType function 
  def __str__(self)->str:
      """
          Returns a string representation of the sushi order
  
          Returns
          string representation of the sushi order
      """
      return f"{self.__amount} fries for ${'{:.2f}'.format(self._price)}"
    
class Sushi(Order):
  """
  Attributes
----------
with_avocado: bool
    Indicates if the sushi roll contains avocado.
size: str
    Indicates the size of the sushi roll, either "snack" or a larger size.
address: str
    The address of the order entered by the user.
    
Methods
-------
calculatePrice(discount: float)
    Calculates the price of the sushi roll, taking into account the presence of avocado, the size of the roll, and any discount.
getCombo() -> str
    Returns the combo item associated with the Sushi order.
__str__() -> str
    Returns a string representation of the sushi order.
  """
  def __init__(self,with_avacado:bool,size:str,address:str,discount:int,id:str):
    self.__with_avacado=with_avacado
    self.__size=size
    super().__init__("Sushi",1,address,discount,id)

  def calculatePrice(self,discount):
    '''
	Calculates the total price of the order using the size and wether the sushi contains avacado
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
    if self.__with_avacado==True:
      self._price+=0.2
    self._price*=5 if self.__size=="snack" else 20
    self._price-=discount
    
  # def getCombo()->str:
  #   return "Healthy Burger"
  
  def __str__(self)->str:
      """
          Returns a string representation of the sushi order
  
          Returns
          string representation of the sushi order
      """
      return f"{self.__size} sized {self._name} with {'avacado' if self.__with_avacado==True else 'no avacado'} for ${self._price}"