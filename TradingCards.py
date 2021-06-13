#Adam Kent Trading Cards Student Number 201443064
import openpyxl

class Card():
    def __init__(self, theName, theType, theHP, theMoves, isShiny):
        self.name = theName
        self.type = theType
        self.HP= int(theHP)
        self.moves= tuple(theMoves)
        self.shiny = isShiny

    def __str__(self):
        return f'Card name: {self.name}. Card type: {self.type}. Card HP: {self.HP}. Card moves {self.moves}. Card shiny: {self.shiny}'

class Deck():
    def __init__(self):
        self.deck = []

    def __str__(self):
        output = "["
        for element in self.deck:
            output += str(element)
            output += "\n\n"
        output += "]"
        return output 

    def inputFromFile(self, fileName):
        self.file = fileName
        totalNumCards = 0
        sheet = book.active
        for row in sheet.iter_rows(min_row = 2):
            features = []
            for cell in row:
                if cell.value != None:
                    features.append(cell.value)
                else:
                    return
            #Popping the moves stuff as an other tuple
            theMoves = []
            for i in range (0,10):
                x = features.pop()
                theMoves.append(x)
                i+=1
            theMoves.reverse()
            #Trying to assign these to a new card, then insert that into a stack deck
            name = features[0]
            cardtype = features[1]
            hitpoints = features[2]
            shininess = features[3]
            NewCard = Card(name, cardtype, hitpoints, theMoves, shininess)
            self.deck.insert(0, NewCard)

    def addCard(self, theCard):
        self.deck.insert(0, theCard)
        print("Added " ,theCard.name, " to the deck of cards.")

    def rmCard(self, theCard):
        for item in range (0, (len(self.deck)-1)):
            if self.deck[item].name == theCard.name:
                removed = self.deck.pop(item)
                print("The card, " ,removed.name, "has been removed")
            item+=1
    
    def getMostPowerful(self):
        points = {}
        for element in self.deck:
            theName = element.name
            order = list(element.moves)
            numbers = []
            for element in range(1,len(order), 2):
                okay = order[element]
                numbers.append(okay)
            numbers.sort()
            highest = numbers.pop()
            points[theName] = highest
        bestest = max(points, key=points.get)
        print(bestest, "Is the most powerful card with a move of", points[bestest])


    def getAverageDamage(self):
        averages = []
        for element in self.deck:
            theName = element.name
            order = list(element.moves)
            numbers = []
            for element in range(1,len(order), 2):
                okay = order[element]
                numbers.append(okay)
            total = sum(numbers)
            total/=5
            averages.append(total)
        total1 = (sum(averages))/len(self.deck)
        print(total1)

    def viewAllCards(self):
        print(self)

    def viewAllShinyCards(self):
        print("Viewing cards by shininess being a Truth")
        for element in self.deck:
            if element.shiny == True:
                print(element)

    def viewAllByType(self,theType):
        print("Viewing cards by type ", theType)
        for element in self.deck:
            if element.type == theType:
                print(element)

    def getCards(self):
        return self.deck

    def saveToFile(self, fileName):
        book.save(fileName)
        print("File has been saved successfully")
        return

book = openpyxl.load_workbook('sampleDeck.xlsx')
Winkle = Card("Winkle", "egg", 89, ["lol","lol","lol","lol","lol"], 1)
New = Deck()
New.inputFromFile('sampleDeck.xlsx')
New.addCard(Winkle)
print(New)
New.rmCard(Winkle)
New.getMostPowerful()
New.getAverageDamage()
New.viewAllCards()
New.saveToFile("sampleDeck1.xlsx")
New.viewAllShinyCards()
New.viewAllByType("Magi")