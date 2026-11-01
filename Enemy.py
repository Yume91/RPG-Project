import random
import Attacks

#ENEMY BASE CLASS ========================================
class Enemy:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.modifier = random.randint(1, 3)
        self.attacks = []
        self.effect = 1
        self.maxhp = 0
        self.hp = 0
        #look into garbage collector for downed enemies who aren't registered!!!!!
        #ALSO implement private variables where it would be good to with __

    def __repr__(self):
        return ">> {"+self.name+"}"

    @staticmethod
    def atklist(self):
        result = ""
        for i in Attacks.allattacks:
            if i.usngclass == self.clas and i.lvl <= self.level:
                result += i.__repr__() + "\n"
        return result

#DRAGON EXTENSION CLASS ========================================
class Dragon(Enemy):
    def __init__(self, level):
        super().__init__("DRAGON", level)
        self.description = ("| a gargantuan winged lizard, dangerous foe"
                            "\n| with durable red scales, as well as sharp"
                            "\n| metal claws and a lethal breath of fire")
        self.maxhp = int(self.level*(30+random.randint(2,4)/2.5))+random.randint(1,3)
        if self.level < 5: self.maxhp = int(self.maxhp*0.85)
        self.hp = self.maxhp
        self.clas = "Dragon"

    def __repr__(self):
        return (super().__repr__()+
                "\n"+self.description+
                "\n> Attacks:\n"+self.atklist(self).__str__())

    def __str__(self):
        return (super().__repr__()+
                "\thp: "+self.hp.__str__()+"/"+self.maxhp.__str__()+
                " lvl: "+self.level.__str__())

#GOBLIN EXTENSION CLASS ========================================
class Goblin(Enemy):
    def __init__(self, level):
        super().__init__("GOBLIN", level)
        self.description = ("| short creature, often living and hunting"
                            "\n| in packs, can be easily angered, and can"
                            "\n| use rudimentary tools and weapons")
        self.maxhp = int(self.level*(10+random.randint(2,4)/2.5))+random.randint(1,3)
        if self.level < 5: self.maxhp = int(self.maxhp*0.85)
        self.hp = self.maxhp
        self.clas = "Goblin"

    def __repr__(self):
        return (super().__repr__()+
                "\n"+self.description+
                "\n> Attacks:\n"+self.atklist(self).__str__())

    def __str__(self):
        return (super().__repr__()+
                "\thp: "+self.hp.__str__()+"/"+self.maxhp.__str__()+
                " lvl: "+self.level.__str__())

# ARMOR EXTENSION CLASS ========================================
class Armor(Enemy):
    def __init__(self, level):
        super().__init__("ARMOR", level)
        self.description = ("| tall warrior completely covered in dark"
                            "\n| plate armor with a set of decorative horns,"
                            "\n| wields an enormous double-edged greatsword")
        self.maxhp = int(self.level * (20 + random.randint(2, 4) / 2.5)) + random.randint(1, 3)
        if self.level < 5: self.maxhp = int(self.maxhp * 0.85)
        self.hp = self.maxhp
        self.clas = "Armor"

    def __repr__(self):
        return (super().__repr__() +
                "\n" + self.description +
                "\n> Attacks:\n" + self.atklist(self).__str__())

    def __str__(self):
        return (super().__repr__() +
                "\thp: " + self.hp.__str__() + "/" + self.maxhp.__str__() +
                " lvl: " + self.level.__str__())

# SPIDER EXTENSION CLASS ========================================
class Spider(Enemy):
    def __init__(self, level):
        super().__init__("SPIDER", level)
        self.description = ("| a tall arachnid with long legs, usually"
                            "\n| found only in its den, waiting for worthy"
                            "\n| prey to come by unaware of its near end")
        self.maxhp = int(self.level * (16 + random.randint(2, 4) / 2.5)) + random.randint(1, 3)
        if self.level < 5: self.maxhp = int(self.maxhp * 0.85)
        self.hp = self.maxhp
        self.clas = "Spider"

    def __repr__(self):
        return (super().__repr__() +
                "\n" + self.description +
                "\n> Attacks:\n" + self.atklist(self).__str__())

    def __str__(self):
        return (super().__repr__() +
                "\thp: " + self.hp.__str__() + "/" + self.maxhp.__str__() +
                " lvl: " + self.level.__str__())