class UserLevels():

    def __init__(self):
        self.users = []

    def getUser(self, id):
        return next((x for x in self.users if x.id == id), False)

    def addUser(self,id):
        self.users.append(User(id,0,0,0))

    def __str__(self):
        pass


class User():

    def __init__(self, theId, theExp, theCoins, theLevel):
        self.id = theId
        self.exp = theExp
        self.coins = theCoins
        self.level = theLevel
        self.expRate = 1
        self.badges = []

    def onMessage(self, boost = 0):
        self.exp += 1
        if self.level < 5 and self.exp == ((2**(self.level + 1))*100):
            self.level+= 1
            self.exp = 0
            return True
        else:
            return False
