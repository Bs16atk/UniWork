# Adam Kent MSc Computer Science 201443064
import datetime
import random
import string

class BasicAccount():
    #The number of people in the world
    numPeople = 0
    
    def __init__(self, theName, theacNum, thebalance, thecardNum, thecardExp):
        self.name = theName
        self.acNum = int(theacNum)
        self.balance = float(thebalance)
        self.cardNum = thecardNum
        self.cardExp = tuple(thecardExp)
        BasicAccount.numPeople += 1 #increment the number of people in the world by 1
        print("The account holder is {self.name}! and their balance is £{self.balance}".format(self=self))

    def __str__(self):
        return 'The account holder is {self.name}! and their balance is £{self.balance}'.format(self=self)
 
    def getAvailableBalance(self):
        print("Your balance is £", self.balance)

    def deposit(self, theamount):
        """
        Adds amount to the balance
        """
        self.amount = float(theamount)
        print("Updating", self.name,"'s balance by £", theamount)
        self.balance = self.balance + theamount
        print("New balance = £",self.balance)

    def withdraw(self, thewithdrawal):
        """
        Withdraws amount to the balance
        """
        self.withdrawal = float(thewithdrawal)
        if thewithdrawal <= self.balance:
            print(self.name, "has withdrew £",thewithdrawal)
            self.balance = self.balance - thewithdrawal
            print("New balance is £", self.balance)
        else:
            print("You do not have that amount in your available balance")

    def getBalance(self):
        """
        Returns the balance of the account as a float.
        """
        print("Your balance is £", self.balance)

    def getName(self):
        return 'The account holder is {self.name}!'

    def getAcNum(self):
        
        return 'The account number is {self.acNum}'

    def issueNewCard(self):
        self.cardNum = ''.join(random.choice(string.digits) for _ in range (16))
        print("The new card number is " + self.cardNum)
        newDate = datetime.datetime.now()
        newDateYear = newDate.year + 3
        self.cardExp = (newDate.month, newDateYear - 2000)
        print("The new card is valid until", self.cardExp)

    def closeAccount(self):
        return self.withdraw(self.balance)

class PremiumAccount(BasicAccount):
    def __init__(self, theName, theacNum, thebalance, thecardNum, thecardExp, theoverdraft, theoverdraftLimit):
        super().__init__(theName, theacNum, thebalance, thecardNum, thecardExp)
        self.overdraft = theoverdraft
        self.overdraftLimit = float(theoverdraftLimit)
        print("A new Premium Member has been created: Hello {self.name}!".format(self=self))

    def getAvailableBalance(self):
        if self.overdraft:
            self.availableBalance = self.balance + self.overdraftLimit
            print("Your available balance is £", self.availableBalance)
        else:
            print("Your balance is £", self.balance)

    def getBalance(self):
        """
        Returns the balance of the account as a float.
        """
        print("Your balance is £", self.balance)
        print("Your overdraft limit is", self.overdraftLimit)

    def withdraw(self, thewithdrawal):
        """
        Withdraws amount to the balance
        """
        self.availableBalance = self.balance + self.overdraftLimit
        self.withdrawal = float(thewithdrawal)
        if self.overdraft:
            if thewithdrawal <= self.availableBalance:
                print(self.name, "has withdrew £",thewithdrawal)
                self.balance = self.balance - thewithdrawal
                print("New balance is £", self.balance)
            else:
                print("You do not have that amount in your available balance")
        else:
            if thewithdrawal <= self.balance:
                print(self.name, "has withdrew £",thewithdrawal)
                self.balance = self.balance - thewithdrawal
                print("New balance is £", self.balance)
            else:
                print("You do not have that amount in your available balance")

    def setOverdraftLimit(self, theoverdraftLimit):
        if -self.balance >= theoverdraftLimit:
            print("You must pay back £", -self.balance - theoverdraftLimit, "before you can change your limit to this amount" )
        else:
            self.overdraftLimit = theoverdraftLimit
            print("New overdraft limit is £", self.overdraftLimit)


    def closeAccount(self):
        if self.balance <= 0:
            print("Can not close account due to customer being overdrawn by £", -self.balance)
        else:
            return self.withdraw(self.balance)

#Create some people
p1 = PremiumAccount("Alice", 21, 65.0, 165.0, (30,30), 1, 1000)

p1.getAvailableBalance()
p1.deposit(100)
p1.withdraw(500)
p1.issueNewCard()
p1.closeAccount()