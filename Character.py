import random

#CHARACTER BASE CLASS ========================================
class Character:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.modifier = random.randint(1,3)
        self.effect = 1
        self.maxhp = 0  #/placeholders for
        self.hp = 0     #\__repr__ to work
        self.attacks = []
        self.target = 1 #chance to be targeted by enemies, depending on class

    def __repr__(self):
        return (self.name+" -> lvl: "+self.level.__str__()+
                " hp: "+str(self.hp)+"/"+str(self.maxhp)+
                "\n> Attacks:\n"+self.atklist())

    def __str__(self):
        return (self.name + "(lvl " + self.level.__str__() + " "
                +self.hp.__str__() + "/" + self.maxhp.__str__() + ")")

    def hired(self):
        return print("\n[+]"+self.name+" has been added to the party!")

    def removed(self):
        return print("\n[-]"+self.name+" has been removed from the party!")

    def find(self, name):
        if name in self.name: return self
        else: return None

    def atklist(self):
        result = ""
        for i in self.attacks:
            result += i.__repr__() + "\n"
        return result

#MAGE EXTENSION CLASS ========================================
class Mage(Character):
    def __init__(self, name):
        super().__init__(name)
        self.maxhp = random.randint(1,6)*2+int(self.modifier / 2)
        self.hp = self.maxhp
        self.target = 0.6
        self.clas = "Mage"

    def __repr__(self):
        return ">> {MAGE}\t\t"+super().__repr__()

    def lvlup(self):
        if self.level<10:
            print("[↑]"+self.__str__()+" has leveled up!")
            self.level+=1
            addedhp=random.randint(1,6)*2
            self.maxhp+=addedhp
            self.hp+=addedhp
            print("And now they are "+self.__str__())
            if self.level==5:
                print(self.name + " has learned a new attack!"
                                  "You can read more info on the Party page")
        else:
            print(self.name+" is already level 10!")

#PALADIN EXTENSION CLASS ========================================
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name)
        self.maxhp = random.randint(1,10)*2+self.modifier
        self.hp = self.maxhp
        self.target = 1.2
        self.clas = "Paladin"

    def __repr__(self):
        return ">> {PALADIN}\t"+super().__repr__()

    def lvlup(self):
        if self.level<10:
            print("[↑]"+self.__str__()+" has leveled up!")
            self.level+=1
            addedhp=random.randint(1,10)*2+self.modifier
            self.maxhp+=addedhp
            self.hp+=addedhp
            print("And now they are "+self.__str__())
            if self.level==5:
                print(self.name + " has learned a new attack!"
                                  "You can read more info on the Party page")
        else:
            print(self.name+" is already level 10!")

#HELPER EXTENSION CLASS ========================================
class Helper(Character):
    def __init__(self, name):
        super().__init__(name)
        self.maxhp = random.randint(1,8)*2+int(self.modifier / 2)
        self.hp = self.maxhp
        self.target = 0.9
        self.clas = "Helper"

    def __repr__(self):
        return ">> {HELPER}\t"+super().__repr__()

    def lvlup(self):
        if self.level<10:
            print("[↑]"+self.__str__()+" has leveled up!")
            self.level+=1
            addedhp=random.randint(1,8)*2
            self.maxhp+=addedhp
            self.hp+=addedhp
            print("And now they are "+self.__str__())
            if self.level==5:
                print(self.name+" has learned a new attack!"
                      "You can read more info on the Party page")
        else:
            print(self.name+" is already level 10!")