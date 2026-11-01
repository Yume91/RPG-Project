import random

class Attack:
    def __init__(self, usingclass, name, description, odds, minimum, maximum, lvl, attacktype, target, multi):
        self.usngclass = usingclass
        self.name = name
        self.description = description
        self.odds = odds
        self.minimum = minimum
        self.maximum = maximum
        self.lvl = lvl
        self.attacktype = attacktype    #types => D=damage E=effect H=heal
        self.target = target            #P=party E=enemies
        self.multi = multi              #True if attack hits multiple enemies

    def __repr__(self):
        return (self.__str__()+
                "\n"+self.description)

    def __str__(self):
        if self.multi:
            return self.name+" || "+self.odds.__str__()+"% to hit || multiple targets"
        else:
            return self.name + " || " + self.odds.__str__() + "% to hit || single target"

allattacks = [Attack(usingclass,name,description,odds,minimum,maximum,lvl,attacktype, target, multi)
              for usingclass,name,description,odds,minimum,maximum,lvl,attacktype, target, multi in [
#CHARACTERS ========================================
        #MAGE ATTACKS
                  ("Mage","Fireball",
                    "launches a big ball of fire,\ndamaging nearby enemies",
                    50,4,24,1,"D","E", True),
                  ("Mage","Bolt(??)",
                    "sends a bolt of energy at an\nattacking enemy",
                    100,4,12,1,"D","E", False),
                  ("Mage","Lightning",
                    "summons a bolt of electricity,\nstriking one opponent",
                   75,6,36,5,"D","E", False),
        #PALADIN ATTACKS
                  ("Paladin","Smite",
                    "imbues their sword with power,\nslashing at their opponent",
                    85,2,16,1,"D","E", False),
                  ("Paladin","Shield",
                    "blocks one of incoming enemy\nattacks, shielding the team",
                    100,0.8,0.3,1,"E","E", False),
                  ("Paladin","Heal",
                   "recovers some amount of health,\nfor themself, or an ally",
                   100,2,16,5,"H","P", False),
        #HELPER ATTACKS
                  ("Helper","Support",
                   "boosts the damage dealt by one\nof their allies",
                   100,1.2,1.6,1,"E","P", False),
                  ("Helper","First aid",
                    "helps an ally get up after a hit,\npatching up some of their injuries",
                    100,2,10,1,"H","P", False),
                  ("Helper","Weaken",
                   "reduces the damage dealt by one\nof their opponents",
                   100,0.9,0.6,5,"E","E", False),
#MONSTERS ========================================
        #DRAGON ATTACKS
                  ("Dragon","Claws",
                   "slashes one character with a swipe\nof its sharp claws",
                   75,4,16,1,"D","P", False),
                  ("Dragon","Glare",
                   "s piercing gaze intimidates\none attacking party member",
                   80,0.9,0.75,1,"E","P", False),
                  ("Dragon","Breath",
                   "breathes a blast of flame onto\nthe attacking party",
                   50,4,22,5,"D","P", True),
        #GOBLIN ATTACKS
                  ("Goblin","Club",
                   "tries to hit one of the characters\nwith its wooden club",
                   75,4,10,1,"D","P", False),
                  ("Goblin","War Cry",
                   "tries to motivate itself more\nwith an energizing shout",
                   100,1.4,1.75,1,"E","E", False),
                  ("Goblin","Arrow",
                   "fires off an arrow from its bow\nat a character",
                   50,6,18,5,"D","P", False),
        #ARMOR ATTACKS
                  ("Armor","Greatsword",
                   "slashes at one character with its\ndouble-handed sword",
                   80,3,9,1,"D","P", False),
                  ("Armor","Guard",
                   "prepares itself to block the next\nincoming attack",
                   90,0.85,0.7,1,"E","P", False),
                  ("Armor","Blades",
                   "sends a hail of small blades flying\nat the attacking party",
                   60,5,17,5,"D","P", True),
        #SPIDER ATTACKS
                  ("Spider","Web",
                   "covers the party in it's webs, slowing\ndown possible attacks",
                   75,0.9,0.65,1,"E","P", True),
                  ("Spider","Pincers",
                   "bites down at one of the characters,\ntrying to eat them",
                   85,5,12,1,"D","P", False),
                  ("Spider","Venom",
                   "injects venom into the bloodstream\nof a party member",
                   60,6,22,5,"D","P", False),
              ]]

#UPDATES CHARACTERS' AND ENEMIES' ATK LISTS
def checkattacks(caller):
    attackslst = [x for x in allattacks
                    if caller.clas==x.usngclass
                    and x.lvl <= caller.level]
    for atk in attackslst:
        if atk not in caller.attacks:
            caller.attacks.append(atk)

#SORT ATTACKS INTO THE RIGHT TYPES
def action(caller,self,recipient):
    if not self.multi:
        result=0
        if aim(self,recipient):
            match self.attacktype:
                case "D":
                    result=damage(self,caller,recipient)
                    recipient.hp-=result
                    if recipient.hp<0:
                        recipient.hp=0
                    print("[✴]"+recipient.name+" took "+result.__str__()+" damage! "+
                          "("+recipient.hp.__str__()+"/"+recipient.maxhp.__str__()+")")
                case "E":
                    result=effect(self,caller,recipient)
                case "H":
                    result=heal(self,caller,recipient)
            if recipient.hp==0:
                print("[☠]"+recipient.name + " has been defeated!")
        else:
            print("[ᯓ]"+recipient.name+" has dodged the incoming attack!")
        return result
    else:       #recursive for multiple enemies
        self.multi=False
        for i in recipient:
            action(caller,self,i)
        self.multi=True
        return None

#CHECK IF ATTACK HITS
def aim(self,recipient):
    if self.usngclass == "Helper":
        result=(random.randint(1,100)<=self.odds+recipient.modifier)
    else:
        result=(random.randint(1,100)<=self.odds)
    return result

#SYSTEM FOR ENEMIES TO TARGET CHARACTERS
def enmaim(self, party):    #returns the character to target
    ret = 0
    if self.multi:
        ret = party
    else:
        collectivechance = 0
        for i in party:
            collectivechance+=i.target
        chosen = float(random.randint(0,int(collectivechance*100)))/100
        targeted = 0
        for i in party:
            if chosen>i.target:
                chosen-=i.target
                targeted+=1
            else:
                ret = party[targeted]
                if ret.hp<=0:
                    ret=enmaim(self,party)
                break
        return ret
    return ret

#CALCULATE THE ATTACK'S DAMAGE
def damage(self,caller,recipient):
    result=random.randint(self.minimum,self.maximum)
    if self.usngclass == "Mage":
        result+=recipient.modifier
    if caller.effect!=1:
        result=int(caller.effect*result)
        caller.effect=1
    return result

#CALCULATING APPLYING EFFECTS
def effect(self,caller,recipient):
    minm=int(self.minimum*100)
    maxm=int(self.maximum*100)
    if  maxm>minm:                          #/calcchance lambda can not be applied
        result=random.randint(minm,maxm)    #\as there are two possible scenarios
    else:
        result=random.randint(maxm,minm)
    result=float(result)/100
    if caller.effect!=1:
        result = int(1+((result-1)*caller.effect))
        caller.effect=1
    if recipient.effect != 1:
        result = (recipient.effect + result)/2
    recipient.effect = result
    print("[🗲]"+recipient.name + "'s next attack will deal " + result.__str__() +
          "\ntimes it's regular damage!")
    return result

#HALCULATING HEALED AMOUNT
def heal(self,caller,recipient):
    result=random.randint(self.minimum,self.maximum)
    if caller.effect != 1:
        result = int(result*caller.effect)
        caller.effect = 1
    recipient.hp+=result
    if recipient.hp>recipient.maxhp:
        recipient.hp=recipient.maxhp
    print("[⛨]"+recipient.name + " has been healed for " + result.__str__() + " health points! " +
          "(" + recipient.hp.__str__() + "/" + recipient.maxhp.__str__() + ")")
    return result