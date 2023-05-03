#-----------------------------------------------------------------------------
# Name:        ICS4UO Extending data Structures-Cosmos Burgers
# Purpose:     To provide an interface between customers, orders and delivery people. Main features include allowing individual customers to order and delivery people to track which orders they delivered. Demonstrates my knowledge of abstract classes, inheritance, polymorphism, composition and classes.
#
# References: 	This program is an extension of of ICS4UO data Structures. This program uses the NumPy/SciPy style of documentation as found
#				here: https://numpydoc.readthedocs.io/en/latest/format.html with
#				some minor modifications based on Python 3 function annotations
#				(the -> notation).
#
# Author:      Joshua Chou
# Created:     18-April-2023
# Updated:     25-April-2023
#-----------------------------------------------------------------------------

#Seperated into modules to increase readability, organization and decrease potential bugs
import uuid
from Topping import Topping
from burger import Hamburger, HealthyBurger
from SalesCalculator import SalesCalculator
from sides import Fries, Sushi
from Order import Order
#used to decide wether the user can use their reward points
import random


def createType(burgerType: str, toppings_enum: set[Topping], address: str,
               side: str, id: str) -> Hamburger:
  """
    Creates a burger object based on the burger type and toppings

    Parameters
	  ----------
    burger_type: Hamburger 
      string representing the burger type ("basic" or "healthy")
    toppings_enum: Set[Topping]
      set of Topping enum members representing the toppings
    address:string
      address attatched to the order
    side:str
      side of the burger
    Returns
	  -------
	  Hamburger or Healthyburger object if the parameter burgerType was a valid type
		None otherwise 

   """
  if burgerType == "basic":
    burger = Hamburger(set(toppings_enum), address, 0, side, id)
  elif burgerType == "healthy":
    burger = HealthyBurger(set(toppings_enum), address, side, id)
  else:
    print(f"Invalid Order type: {burgerType}")
    return None
  return burger


def writeOrder(order: str):
  """
  A simple function that writes the type of order eg. fries,sushi in the file
  
  Parameter
  ________
  order:str
    A string representation of the order type
  Raises
  ______
  IOError:
    If there is an issue with opening or writing to the transactions.txt file. For example, if the file does not exist, or the program does not have permissions to write to the file.
  Returns
  ______
  None
  """
  with open("transactions.txt", 'a') as outfile:
    outfile.write(f",{order}")


def getValidInput(valids, prompt):
  """
   Repeatedly asks user for input until a valid input is entered, then the function returns the valid input
  
  Parameter
  ________
  valids:str[]
    A list of strings representing the inputs that are considered valid
  prompt:str
    The prompt that will be shown to the user
  Returns
  ______
  user_input:str
    A string of the valid input entered by the user
  """
  while True:
    user_input = input(prompt).lower()
    if user_input in valids:
      return user_input


def getDiscount():
  """
  Calculates the discount (if any) based on reward points of the user, and returns the discount
  
   Returns
   ______
   discount:float
   """

  discount = 0.0
  #"Lottery feature" see if user can use their reward points 1 in 5 chance
  use_points = random.randint(1, 5)  #set value to 1 for testing
  if use_points == 1:  #User can use reward points
    discount = SalesCalculator.calReward() / 8
  return discount


def displayOrder(order: Order, discount: float):
  """
  Prints the user order in the console, along with any discounts
  Parameters
  __________
  order:Order
    order to print
  discount:float
    discount of the order
   Returns
   ______
   None
  """
  if discount > 0:
    print(f"you saved ${'{:.2f}'.format(discount)} ")
    print(
      f"The price of your {order.getName()} is ${'{:.2f}'.format(order.getPrice())}!"
    )
  else:
    print(order)


with open("README.md", 'r') as instructions:
  instructions = instructions.readlines()
for line in instructions:
  print(line)
print("\n")
while True:
  user = input("Are you a customer or a delivery person (enter c or d)")
  if user == 'c' or user == 'd':
    break

#list of compound data types (burger objects) used to store all burgers ordered
order_list = []
with open('transactions.txt', 'r') as transactions:
  content = transactions.readlines()
  content=[x for x in content if x.strip()]
  i = 0
  #Print previous burgers that customer personally bought and add to order_list
  user_address = None
  if user == 'c':
    user_address = input("Enter your address")
  print("Order history saved in transactions.txt file" if user ==
        'c' else "Delivery List:")
  for line in content:
    line = line.strip().lower()  #remove any trailing spaces/ empty lines and convert all to lowercase for program to proprely read
    full_order = line.split(":")
    #if not enough info
    if len(full_order)<=1:
      continue;
   
    line = full_order[0]  # order should always be first section
    id = full_order[-1]  # id should always be last
    #check to see if there is a side. Side should be second section, however, if the second section is the id instead (in the case of no side), then there is no side
    side = None
    if full_order[1] != id:
      side = full_order[1]


    line = line.split(',')
    if not line or len(
        line
    ) < 2:  #go on to next order if does not contain sufficient information
      continue
    address = line[0]
    if address == user_address or user == 'd':  #only print burgers that customer bought, print all burgers if user is a delivery man
      type = line[1]
      order = None
      if type == "healthy" or type == "basic":
        #ABSTRACT DATA TYPES a set is effectivly used to ensure that no 2 toppings are the same(When toppings are passed into the constructor, duplicates or ignored, the same applies for the addTopping() method ).
        # A tuple is also used to store the values
        toppings = set(line[2:])
        #convert toppings to enum members
        toppingsEnum = []
        for topping in toppings:
          try:
            enum_member = Topping[
              topping.strip()]  #strip extra spaces in topping in file
            toppingsEnum.append(enum_member)
          except KeyError:
            print(f"Invalid topping: {topping}")
            topping = None
          #build burger object based on toppings (collected above) and burger type
        order = createType(type, toppingsEnum, address, side, id)
      elif type == "fries":
        try:
          amount = line[2]  # Indexerror
          order = Fries(int(amount), address, 0, id)  #typeerror
        except (
            IndexError, ValueError
        ):  #insifficient, correct values will always be passed in (bool)
          continue

      elif type == "sushi":
        try:
          order = Sushi(
            bool(line[2]), line[3], address, 0, id
          )  #discout is absorbed by the company, delivery person still makes the same
        except IndexError:  #insufficient info
          continue
      if order != None:
        
        if user == 'c':
          print(order)
          order_list.append(order)
        elif user == 'd':
          with open ("delivered.txt",'r') as delivered:
            ids=delivered.readlines()
          ids = [id.strip() for id in ids]
          if order.id not in ids: # if not yet delivered this order
            print(f"{i+1}. deliver {order} to {order.getAddress()}")
            i += 1
            order_list.append(order)
          
        # list for delivery person to use ( find amount of money they will make, track what orders they completed )

SalesCalculator = SalesCalculator(order_list)
if user == 'c':
  print(f"you have {SalesCalculator.calReward()} Reward points")
#program flow
if user == 'c':
  while True:  #ACCEPTING ORDERS

    with open("transactions.txt", 'a') as addresses:
      addresses.write(f"\n{user_address}")
    order_type = input("Enter your order (fries,sushi,burger)").lower()

    if order_type == "fries":  #FRIES
      writeOrder("fries")
      while True:
        try:
          amount = abs(int(input("How many fries do you want?")))
          break
        except ValueError:
          continue
      discount = getDiscount()
      order = Fries(amount, user_address, discount,None)
      displayOrder(order, discount)
      with open("transactions.txt", 'a') as fries:
        fries.write(f",{str(amount)}")
      # setPrice(order)

    elif order_type == "sushi":  #SUSHI
      writeOrder("sushi")
      choice_avacado = getValidInput(
        ['y', 'n'], "Do you want avacado with your sushi (y/n)")
      size = getValidInput(["snack", "party"],
                           "Enter the size of your sushi (snack,party)")
      with_avacado = True if choice_avacado == 'y' else 'n'
      #get discount (if there is any) based on reward points
      discount = getDiscount()
      #create order
      order = Sushi(with_avacado, size, user_address, discount,None)
      displayOrder(order, discount)
      with open("transactions.txt", 'a') as sushi:
        sushi.write(f",{str(with_avacado)},{size}")
      # setPrice(order)  #sets price of sushi using the discount

    elif order_type == "burger":
      burgerType = input("Enter the type of burger (basic/healthy)")
      order = createType(
        burgerType, set(), user_address,
        None,None)  #set side to None for now, then wait for user to enter side. Set id for none, as the id will soon be written in the file, the id is not needed in the object when creating orders
      if order != None:
        print(order)
        writeOrder(burgerType)

      else:
        continue
      toppings_menu = list(Topping)
      for i in range(len(toppings_menu)):
        print(f"{i+1}. {toppings_menu[i].name}")
      while True:
        try:
          choice = int(
            input(
              "Choose a topping to add to your burger (enter a number). Enter 0 to quit"
            ))
        except ValueError:
          print("enter valid number")
          continue
        if choice == 0:
          #let user use some of the enhanced funcionality (healtiness/price of burger)
          print(order)
          #write orderid in fiel

          while True:
            try:
              #COMBO FUNCionality HERE
              choice = int(
                input(
                  "Enter 1 to get a combo. Enter 2 to get the healthiness level. Enter 0 for none."
                ))
            except ValueError:
              continue
            if choice == 1:

              side = getValidInput(
                ["sushi", "fries"],
                "COMBO-choose a side (fries/sushi) along with your burger for only $13"
              )
              order.side=order.setSide(side)
             
              print(f"{order} now only costs $14")
              with open("transactions.txt", 'a') as combo:
                combo.write(f":{side}")
              break
            elif choice == 2:
              print(
                f"The healthiness level is {order.calculateHealthiness()}/4"
                if isinstance(order, HealthyBurger) else
                "Calculating healthiness is only for Healthy burger")
              break
            elif choice == 0:
              break
            else:
              continue
          break
        try:
          topping = toppings_menu[int(choice - 1)]
          #write order in file only if not already in toppings list
          order.addTopping(topping)

        except IndexError:
          print("Enter valid topping number")
          continue
        print(order)
    id = uuid.uuid1()
    with open("transactions.txt", 'a') as ids:
      ids.write(f":{id}")

      #let delivery person track which orders they completed
elif user == 'd':
  print(f"You will make ${SalesCalculator.calDeliverySalary(10)}")  #flate rate
  while True:
    try:
      index = int(input("Enter order number you have completed: "))
    except ValueError:
      print("Enter a number")
      continue
    try:

      with open ("delivered.txt",'a') as d:
        d.write(f"{order_list[index-1].id}\n")
      del order_list[index - 1]
      with open("delivered.txt",'r') as d:
        delivered=d.readlines()
        
      if len(delivered)==3: # set to low amountn of deliverys for testing purposes
        print("YOU HAVE BEEN PROMOTED!")
      if len(order_list) < 1:
        print(
          "Yay, you have delivered all your orders! It's time to take a break")
        break
    except IndexError:
      print("Enter valid order number")
      continue
    print("orders left to complete:")

    for i in range(len(order_list)):
      print(f"{i+1}. {order_list[i]} to {order_list[i].getAddress()}")
