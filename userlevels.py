class UserLevels():

    def __init__(self):
        self.users = []

    def getUser(self, id):
        return next((x for x in self.users if x.id == id), False)

    def addUser(self,id):
        theUser = User(id,0,0,0)
        self.users.append(theUser)
        return theUser

    def outputUsers(self):
        out = []
        for aUser in self.users:
            out.append(aUser.__dict__)
        out.sort(key=lambda r: r["exp"],reverse=True)
        out.sort(key=lambda r: r["level"],reverse=True)
        return out

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
        self.guilds = []

    def onMessage(self, boost = 0):
        self.exp += 1
        if self.level < 5 and self.exp >= (self.level + 1)*1000:
            self.level += 1
            self.exp = self.exp - (self.level*1000)
            self.coins += 10
            return True
        else:
            return False

    def __str__(self):
        pass
