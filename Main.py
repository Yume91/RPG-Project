import functools, random, re, Attacks, RandomEvents,json
from Character import Mage, Paladin, Helper
from Enemy import Dragon, Goblin, Armor, Spider

run = True      #variable for keepink the game loop; closed with quit()
party = []      #player's characters added here
enemies = []    #enemies added here - resets per each fight
novalerr = True     #check for validity of answer; False triggers a retry of question
enemiesmet = []    #list of descriptions for the encountered ones
prevenc = 0

calcchance = lambda x: float(random.randint(0,int(float(x)*100)))/100

def title(name):
    def separator(func):
        @functools.wraps(func)
        def wrap(*args):
            print("\n☰☰☰☰☰☰☰☰☰☰ "+name.upper()+" ☰☰☰☰☰☰☰☰☰☰")
            return func(*args)
        return wrap
    return separator

def countinggenerator(maxi):
    for x in range(1,maxi):
        yield x

#ADD CHARACTER ========================================
def hire(character):
    if len(party)<3:        #maximum party size
        party.append(character)
        for p in party:
            Attacks.checkattacks(p)
        character.hired()
    else:
        print("[!!!]Maximum party size reached, remove"
              "\none character in order to add a new one!")

#MENUS ==================================================
@title("main menu")
def mainmenu():
    print("1 - Party Members ["+str(len(party))+"]"
          "\n2 - Manage Party"
          "\n3 - Recorded Monsters ["+str(len(enemiesmet))+"/"+str(4)+"]"
          "\n4 - Explore"
          "\n5 - Duel"
          "\n6 - Load/Save Progress"
          "\n7 - Exit")
    answer = questionrequiresint(7)
    return answer

@title("party members")
def partymembers():
    if len(party)==0:
        print("[!!!]You have no party members!")
    else:
        for character in party:
            print(character.__repr__())
    print("1 - Back to Main Menu")
    answer = questionrequiresint(1)
    return answer

@title("manage party")
def manageparty():
    print("Current party consists of "+str(len(party))+" characters"
          "\n1 - Add Member"
          "\n2 - Remove Member"
          "\n3 - Back to Main Menu")
    answer = questionrequiresint(3)
    return answer

def addcharacter():
    while novalerr:
        print("\nWhat class do you want the character to be?"
              "\n1 - Paladin - attacks with their sword, heals allies"
              "\n2 - Mage - casts dangerous spells"
              "\n3 - Helper - supports party, weakens enemies")
        chclass = questionrequiresint(3)
        print("\nAnd what should they be called?")
        answer = questionrequiresstring()
        check = False
        for p in party:
            if p.name==answer:
                check = True
        if check:
            print("[!!!]You already have a character with that name in the party!")
            addcharacter()
            return None
        match chclass:
            case 1:
                hire(Paladin(answer))
            case 2:
                hire(Mage(answer))
            case 3:
                hire(Helper(answer))
        break
    return None

def removecharacter():
    print("\nCurrent party:")
    if len(party)==0:
        print("[!!!]Party is empty, there is no character"
              "\nthat can be removed!")
        return None
    else:
        for p in countinggenerator(len(party)+1):
            print(p.__str__() +" - " + party[p-1].__str__())
        print("Who do you want to remove?")
        answer = questionrequiresint(len(party))
        match answer:
            case _:
                party[answer-1].removed()   #displays a message
                party.pop(answer-1)         #deletes character
        return None

@title("recorded monsters")
def monsterrecords():
    if len(enemiesmet) == 0:
        print("[!!!]You haven't encountered any enemies yet!")
    else:
        for enm in enemiesmet:
            print(enm.__repr__())
    print("1 - Back to Main Menu")
    answer = questionrequiresint(1)
    return answer

@title("duel")
def duel():
    counter = 1
    if len(party) < 2:
        print("[!!!]You don't have enough characters yet!")
    else:
        print("Choose your fighter:")
        for chrc in party:
            print(counter.__str__()+" - "+chrc.__str__())
            counter+=1
    print(counter.__str__()+" - Back to Main Menu")
    chr1 = questionrequiresint(counter)
    if not chr1==counter:
        counter=1
        print("\nWho will they battle against?")
        for chrc in party:
            print(counter.__str__() + " - " + chrc.__str__())
            counter += 1
        chr2 = questionrequiresint(counter-1)
        if chr1==chr2:
            print("[!!!]A character can't duel themselves!")
            duel()
            return None
        else:
            battle([party[chr1-1]], [party[chr2-1]])
    return None

@title("manage progress")
def savemanager():
    print("What do you want to do?"
          "\n1 - Load an Existing Save"
          "\n2 - Save Current Progress"
          "\n3 - Back to Main Menu")
    return questionrequiresint(3)

#SAVES/LOADS ==================================================
# game's progress and difficulty rise is dynamically calculated on party level,
# so the only crucial data to save is the party itself, and the met monsters
def save():
    # crucial Character parameters - clas name level modifier maxhp hp
    # crucial Enemy parameters - clas level
    print("\nHow do you want to name this save?")
    filename = questionrequiresstring()+".json"
    tosave = []
    for i in party:
        tosave.append([i.clas, i.name, i.level, i.modifier, i.maxhp, i.hp])
    for i in enemiesmet:
        tosave.append([i.clas, i.level])
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(tosave, file, ensure_ascii=False, indent=2)
    print("[★]Your progress has been saved! - "+filename)
    pass

def load():
    print("\nWhich save do you want to restore?")
    filename = questionrequiresstring()+".json"
    with open(filename, 'r', encoding='utf-8') as file:
        loaded = json.load(file)
    print("[☆]Save has been loaded!")
    for i in loaded:
        match i[0]:
            case "Paladin":
                hiring = Paladin(i[1])
                hiring.level = i[2]
                hiring.modifier = i[3]
                hiring.maxhp = i[4]
                hiring.hp = i[5]
                hire(hiring)
            case "Mage":
                hiring = Mage(i[1])
                hiring.level = i[2]
                hiring.modifier = i[3]
                hiring.maxhp = i[4]
                hiring.hp = i[5]
                hire(hiring)
            case "Helper":
                hiring = Helper(i[1])
                hiring.level = i[2]
                hiring.modifier = i[3]
                hiring.maxhp = i[4]
                hiring.hp = i[5]
                hire(hiring)
            case "Dragon":
                enemiesmet.append(Dragon(i[1]))
            case "Armor":
                enemiesmet.append(Armor(i[1]))
            case "Goblin":
                enemiesmet.append(Goblin(i[1]))
            case "Spider":
                enemiesmet.append(Spider(i[1]))
    pass

#ENCOUNTER ==================================================
def explore():
    global prevenc
    if len(party)==0:
        print("[!!!]You don't have a single character yet!")
        return None
    enc = generate()
    trigger(enc,party,enemies)
    if not run:
        quit()
    print(enc.afterword)
    print("1 - Continue"
          "\n2 - Back to Main Menu")
    prevenc = enc
    answer = questionrequiresint(2)
    match answer:
        case 1:
            explore()
        case 2:
            return None
    return None

def trigger(event, prt, enm):
    print(event.__repr__())
    if event.enctype== "B":
        print("\nInput any number to continue")
        questionrequiresint(9,0)
        avglvl = 0
        for p in prt:
            avglvl+=p.level
        avglvl=int(avglvl / len(prt))
        for ec in event.enms:
            if ec=="Dragon":
                for i in range(0, event.enms[ec]):
                    enm.append(Dragon(avglvl))
            if ec=="Goblin":
                for i in range(0, event.enms[ec]):
                    enm.append(Goblin(avglvl))
            if ec=="Armor":
                for i in range(0, event.enms[ec]):
                    enm.append(Armor(avglvl))
            if ec=="Spider":
                for i in range(0, event.enms[ec]):
                    enm.append(Spider(avglvl))
            if ec=="Double":
                    pt = []
                    for p in prt:
                        pt.append(p)
                    if event.enms[ec]>len(party):
                        event.enms[ec]=len(party)
                    for i in range(0, event.enms[ec]):
                        num=random.randint(1,len(pt))
                        enm.append(pt[num-1])
                        pt.remove(pt[num-1])
            for e in enm:
                Attacks.checkattacks(e)
            battle(prt, enm)
            return None
    elif event.enctype=="R" or event.enctype=="T":
        if event.multi:
            for p in prt:
                p.hp += int(p.maxhp*event.effect)
                if p.hp>p.maxhp:
                    p.hp=p.maxhp
                if p.hp<0:
                    p.hp=0
        else:
            counter=1
            print("Choose the character")
            for i in prt:
                print(counter.__str__()+" - "+i.__str__())
                counter+=1
            answer = questionrequiresint(counter-1)
            prt[answer-1].hp += int(prt[answer-1].maxhp*event.effect)
            if prt[answer-1].hp>prt[answer-1].maxhp:
                prt[answer-1].hp=prt[answer-1].maxhp
            if prt[answer-1].hp<0:
                prt[answer-1].hp=0
        return None
    elif event.enctype== "F":
        if event.multi:
            for p in prt:
                if p.effect==1:
                    p.effect = event.effect
                else:
                    p.effect = (p.effect+event.effect)/2
        else:
            counter=1
            for i in prt:
                print(counter.__str__()+" - "+i.__str__())
                counter+=1
            print("Choose the character")
            answer = questionrequiresint(counter-1)
            if prt[answer-1].effect == 1:
                prt[answer-1].effect = event.effect
            else:
                prt[answer-1].effect = (prt[answer-1].effect+event.effect)/2
        return None
    return None

def generate():
    collectivechance = 0
    ret=0           #chosen event to be returned
    avg = 0         #current average party level
    for p in party:
        avg+=p.level
    avg=int(float(avg)/float(len(party)))
    for j in RandomEvents.allencounters:
        if j.lvl<=avg:
            collectivechance += j.chance
    chosen = calcchance(collectivechance)
    for enc in RandomEvents.allencounters:
        if enc.lvl<=avg:
            if chosen<=enc.chance:
                ret = enc
                break
            else:
                chosen -= enc.chance
    if ret==prevenc:
        ret=generate()
    return ret

#BATTLE ==================================================
@title("battle")
def battle(pcs,enm):    #pcs - list of characters | enm - list of opponents
    if len(party) <=0:
        print("[!!!]You don't have enough characters yet!")
        return None
    print("Enemies:")
    for e in enm:
        print(e.__str__())
    ongoing = True
    record()
    while ongoing:
        print("\n============== YOUR TURN ==============")
        for p in pcs:
            if p.hp>0:
                direct(p,pcs,enm)
                if not finishcheck(enm):
                    ongoing = False
                    break
                else:
                    ongoing = downedcheck()
                    if not ongoing:
                        break
                print("Input any number to continue")
                questionrequiresint(9,0)
                print()
            else:
                print(">>> "+p.name+" is currently incapacitated!")
            for j in enm:
                if j.hp==0: enm.remove(j)
            print()
        if not ongoing:
            break
        print("\n============= ENEMY TURN ==============")
        for e in enm:
            enmdirect(e,pcs)
            ongoing = downedcheck()
            if not ongoing:
                break
        print("\nInput any number to continue")
        questionrequiresint(9,0)
    if not downedcheck():
        print("\nYour entire party has been downed!"
              "\n============== GAME OVER ==============")
        quit()
    else:
        print("\n============= BATTLE WON ==============")
        for j in enm:
            if j.hp == 0: enm.remove(j)
        for p in pcs:
            p.lvlup()
            Attacks.checkattacks(p)
        return None

def direct(char,pcs,enm):   #combines methods below into a single call
    atk=char.attacks[atkchoice(char)-1]
    if not atk.multi:
        if atk.target=="P":
            dirct=pcs[prtlist(pcs)-1]
        else:
            dirct=enm[enmlist(enm)-1]
    else:
        if atk.target=="P":
            dirct=pcs
        else:
            for e in enm:
                print(e.__str__())
            dirct=enm
    print("\n[🗡]"+char.name+" "+ atk.description)
    Attacks.action(char,atk,dirct)

def enmdirect(mon,pcs):    #combined full system for the enemy's turn
    atk = enmatkchoice(mon)
    if atk.target=="P":
        dirct=Attacks.enmaim(atk,pcs)
        if dirct==-1:
            enmdirect(mon,pcs)
            return None
    else:
        dirct=mon   #enemies only use boosting effects on themselves
    print("\n>>> " + mon.name + "'s turn,"
          "\n[🗡]it " + atk.description)
    Attacks.action(mon,atk,dirct)
    return None

def enmatkchoice(mon):
    return mon.attacks[random.randint(0,len(mon.attacks)-1)]

def atkchoice(char):
    print(">>> "+char.name+"'s turn,"
          "\nchoose an attack:")
    counter = 0
    for a in char.attacks:
        counter+=1
        print(counter.__str__()+" - "+a.__str__())
    chattk = questionrequiresint(counter)
    return chattk   #returns [i+1] of the chosen attack at attacks[i]

def enmlist(enm):      #target from enemies
    print("\nChoose your target:")
    counter=0
    for e in enm:
        counter+=1
        print(counter.__str__()+" "+e.__str__())
    chtarget = questionrequiresint(counter)
    return chtarget #returns [i+1] of the chosen target at enemies[i]

def prtlist(pcs):      #target from party
    print("\nYour adventuring party:")
    counter=1
    for p in pcs:
        print(counter.__str__()+" "+p.__str__())
        counter+=1
    chtarget = questionrequiresint(counter-1)
    return chtarget #returns [i+1] of the chosen target at party[i]

def finishcheck(team):  #checker for win/lose for both sides of battle
    counter = 0
    for t in team:
        if t.hp <= 0:
            counter += 1
    if counter == len(team):
        return False
    else:
        return True

def downedcheck():  #True if not all are downed | False if game lost
    counter=0
    for j in party:
        if j.hp<=0:
            counter+=1
    if counter==len(party):
        return False
    else:
        return True

def record():   #updates the enemiesmet list
    for enm in enemies:
        for p in party:
            if enm.name==p.name:
                return None
            counter = 0
            new = True
            for met in enemiesmet:
                if enm.name==met.name:
                    if enm.level>met.level:
                        print("Monster records entry on {"+enm.name+"} has been updated!")
                        enemiesmet[counter]=enm
                    new = False
                counter+=1
            if new:
                print("{"+enm.name+"}'s entry has been added to the monster records!")
                enemiesmet.append(enm)
    return None

#ANSWER TYPES ========================================
def questionrequiresint(*args):
    if len(args)==1:
        maxi=args[0]
        answer = input("Enter the chosen number: ")
        if answer is not None:
            try:
                if not (1 <= int(answer) <= int(maxi)):
                    raise OutOfRange
                return int(answer)
            except OutOfRange:  #custom exception type for separate print() outputs
                print("[!!!]Answer out of range, please input a viable one!")
                return questionrequiresint(maxi)
            except ValueError:
                print("[!!!]Wrong answer type, please input an integer!")
                return questionrequiresint(maxi)
        return None
    elif len(args)==2:
        maxi = args[0]
        mini = args[1]
        answer = input("Enter the chosen number: ")
        if answer is not None:
            try:
                if not (int(mini) <= int(answer) <= int(maxi)):
                    raise OutOfRange
                return int(answer)
            except OutOfRange:  # custom exception type for separate print() outputs
                print("[!!!]Answer out of range, please input a viable one!")
                return questionrequiresint(maxi,mini)
            except ValueError:
                print("[!!!]Wrong answer type, please input an integer!")
                return questionrequiresint(maxi,mini)
        return None
    else: return None

def questionrequiresstring():
    answer= input("Enter the name: ")
    try:
        match = re.match("^\\w+$",answer)
        if not match:
            raise OutOfRange
        return str(answer)
    except OutOfRange:  # custom exception type for separate print() outputs
        print("[!!!]Answer out of range, name must be a single word!")
        answer = questionrequiresstring()
        return answer
    except ValueError:
        print("[!!!]Wrong answer type, please input a string!")
        answer = questionrequiresstring()
        return answer

#VALIDITY ANSWER CHECK ===============================
class OutOfRange(ValueError):
    pass

#Methods
#=================================================================================================
#=================================================================================================
#Main Framework

while run:
    match mainmenu():
        case 1:     #list party members
            match partymembers():
                case 1:     #to main menu
                    pass
        case 2:     #manage the party
            match manageparty():
                case 1:     #add a new character
                    addcharacter()
                    pass
                case 2:     #remove a character
                    removecharacter()
                    pass
                case 3:
                    pass    #to main menu
            pass
        case 3:     #monster records
            match monsterrecords():
                case 1:
                    pass    #to main menu
        case 4:     #exploration - random encounters
            explore()
            pass
        case 5:     #duel two characters
            duel()
            pass
        case 6:
            match savemanager():
                case 1:
                    load()
                    pass
                case 2:
                    save()
                    pass
                case 3: #to main menu
                    pass
        case 7:     #exit program
            print ("\nGoodbye!")
            quit()