import pprint
import random

class Building(object):
    '''
    This is a Docstring for the Building class.
    This Class will create an instance of an Elevator and it will hold all of all the Customer Objects.
    
    The customerMap(self) method will organise all of the Customer Objects into the Floorplan Dictionary with each key
    acting as a floor number with a value of a list that contains all of the customers who are on that floor.

    The run(self) method will check the Elevator instance to confirm what floor it is on, and then it will move the
    waiting customers on that floor onto the Elevator. It will then remove them from the waiting Floorplan list.
    If there are any Customer Objects that have a destination floor that is the same as the Elevators Current floor,
    we will then add them to the customerFinished list and remove them from the Elevator.
    '''
    def __init__(self, floors = 0):
        self.floors = floors
        self.custList = []
        self.customerFinished = []
        self.elevator = Elevator(self.floors)   
        self.floorplan = {}
        
    def __str__(self):
        return f'This Building has 0 to {self.floors} floors and the elevator is currently on floor {self.elevator.currentFloor}'

    def __repr__(self):
        return self.__str__()

    def customerMap(self):
        for cust in self.custList:
            self.key = cust.currentFloor

            if self.key in self.floorplan:
                self.floorplan[self.key].append(cust)
            else:   
                self.floorplan[self.key] = [] 
                self.floorplan[self.key].append(cust)     
        pprint.pprint(self.floorplan)

    def run(self):
        # These are to help seporate each iteration in the terminal
        print('\n')
        print('#'*60)
        print('#'*60)

        #if the customer current floor is the same as the elevator current floor,
        #then move that customer onto the elevator.
        try:
            for i in self.floorplan[self.elevator.ElevatorFloor]:
                self.elevator.elevatorPassengers.append(i)       
            if self.elevator.ElevatorFloor in self.floorplan:
                del self.floorplan[self.elevator.ElevatorFloor] 
        except KeyError:
            print("There is no one on this floor")

        #if the customer destination floor is the same as the elevator current floor,
        #then move that Customer off the elevator.
        for passenger in self.elevator.elevatorPassengers:
            if passenger.destinationFloor == self.elevator.ElevatorFloor:
                self.customerFinished.append(passenger)
             
        # Remove the finished customers from the elevator list.
        for finishedPassenger in self.customerFinished:
            if finishedPassenger in self.elevator.elevatorPassengers:
                  self.elevator.elevatorPassengers.remove(finishedPassenger)        
        
        # Print Customers Waiting -- Customers in Elevator -- Customers finished.
        print("\n Customers Waiting:   (The Key is their Floor)")
        pprint.pprint(self.floorplan)

        print("Customers in Elevator:")
        for i in self.elevator.elevatorPassengers:
            print(i)
                  
        print("\n Customers Finished:")
        pprint.pprint(self.customerFinished)

        print('#'*60)
        print('#'*60)
        #self.elevator.moveElevator()
        self.elevator.alternativeMoveElevator()
       
class Elevator(object):
    '''
    This is a Docstring for the Elevator class.
    This elevator will store all of the Customer Objects into a list. 
    This list will be used to create the floorplan dictionary.

    An instance of the Elevator can have its floor moved by calling the moveElevator(self) method.
    We will move the elevator incrementally upwards until we reach the top and then back down to the bottom
    '''
    def __init__(self, floors=0):
        self.move = 1 # this will decide if the elevator will move up(1) or down(-1). Default is up.
        self.floors = floors # Holds the number of floors the evelator can travel too.
        self.elevatorPassengers = [] # this list will hold the customers currently in the elevator
        self.ElevatorFloor = 0 # this is the current floor of the elevator. We will give it a default 0 (ground floor)
        self.elevatorDirection = 0

    def __str__(self):
        return f'Elevator is on Floor {self.ElevatorFloor} and currently has {len(self.elevatorPassengers)} Passengers on board.'

    def __repr__(self):
        return self.__str__()

    def moveElevator(self):
        if self.ElevatorFloor == 0:
            self.elevatorDirection = 1
        if self.ElevatorFloor == self.floors:
            self.elevatorDirection = -1
        if self.elevatorDirection == 0:
            self.elevatorDirection = -1

        self.ElevatorFloor += self.elevatorDirection

    # This is an alternative movement of the elevator.
    # We still start at the ground floor, if there is no one in the elevator we will refer back to the moveElevator() method.
    # But if there is a customer in the elevator, we will check all of their destination floors. the elevator will move to
    # most common destination floor.
    def alternativeMoveElevator(self):
        destinationList = []
        if len(self.elevatorPassengers) !=0:
            for each in self.elevatorPassengers:
                destinationList.append(each.destinationFloor)
            mostCommonFloor = max(set(destinationList), key=destinationList.count)
            self.ElevatorFloor = mostCommonFloor
        else:
            self.moveElevator()

class Customer(object):
    '''
    This is a Docstring for the Customer class.
    This class will take in a number of floors and a customer ID. We will use the 
    floors to create a random floor that the Customer is starting from(currentFloor)
    and where they want to go (destinationFloor)
    We will also ensure that there will be no Customers who have a destination Floor the same as their
    Current floor. Because that's just silly.
    '''
    #create a customer. Customer has a current floor, and a destination floor.
    def __init__(self, floors, custID):
        self.ID = custID
        self.floors = floors
        self.currentFloor = random.randint(0, self.floors) 
        self.destinationFloor = random.randint(0, self.floors)
        while(self.currentFloor == self.destinationFloor):
            self.destinationFloor = random.randint(0, self.floors)

    def __str__(self):
        return f'I am a Customer NO: {self.ID} ----. I am on Floor:{self.currentFloor} and i want to go to floor {self.destinationFloor}'

    def __repr__(self):
        return self.__str__()

def main():
    '''
    this is the main Docstring.
    We will ask the user how many floors the building has and howe many customers are in the building.
    We will later ensure the number of floors will start from 0.
    A try/except is used to ensure that only a postive integer can be inputted.
    We will create a customer object for each waiting customer.

    '''
    correctInputFloor = False
    correctInputCust = False
    while(correctInputFloor != True):
        try:
            floorCount = int(input('How many Floors: '))
            if floorCount <= 0:
                raise ValueError
            else:
                correctInputFloor = True
        except ValueError:
            print('**ERROR** You need a positive interger.')
    while(correctInputCust != True):
        try:
            customerCount = int(input('How many customers: '))
            if customerCount <= 0:
                raise ValueError
            else:
                correctInputCust = True
        except ValueError:
            print('**ERROR** You need a positive interger.')
    floorCount -= 1
    print("\n GENERATING: Floors: 0 to "+str(floorCount)+" -- Total waiting customers: "+str(customerCount)+"") 
    build = Building(floorCount)
    IDcounter = 1
    for i in range (customerCount):
        build.custList.append(Customer(floorCount, IDcounter))
        IDcounter += 1
   
    build.customerMap() 
    # while the waiting customers(floorplan) and and Elevator passengers (elevatorPassengers) still have customers,
    # we will keep moving the elevator and get every customer to their destination.
    while (len(build.floorplan) != 0) or (len(build.elevator.elevatorPassengers) != 0):
        customerCount = (input(f'\n Elevator is now moving to Floor({build.elevator.ElevatorFloor}). Click Enter to add or remove Customers from this Floor.'))
        build.run()

if __name__ == "__main__":
    main()
       