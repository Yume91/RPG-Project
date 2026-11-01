class Encounter:
    def __init__(self,name, description, afterword, enctype, chance, lvl, multi, enms, effect):
        self.name = name
        self.description = description
        self.afterword = afterword
        self.enctype = enctype  #F-find(boost) B-battle(fight) R-respite(heal) T-trap(damage)
        self.chance = chance    #chance of happening
        self.lvl = lvl   #minimum average level of the party for this event to be able to happen
        self.multi = multi  #True if affects the entire team
        self.enms = enms    #dictionary of enemies to be generated for a battle with their amount
        self.effect = effect    #effect to apply in F types; and % of health to gain/lose in R/T types

    def __repr__(self):
        return ("\n☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰"
                "\n|"+self.name+"|"
                "\n"+self.description)

allencounters = [Encounter(name,description,afterword,enctype,chance,lvl,multi,enms,effect)
                 for name,description,afterword,enctype,chance,lvl,multi,enms,effect in [
        #BATTLE ENCOUNTERS
                     ("Ambush",
                      "While walking through a forest,"
                      "\nnearby bushes start to shake. A"
                      "\ngroup of goblins jumps out.",
                      "\nAfter scaring away the remaining"
                      "\nenemies, the route is once again"
                      "\nsafe to traverse.",
                      "B",0.5,1,True,{"Goblin":4},0),
                     ("Grand Hall",
                      "The party enters a seemingly empty"
                      "\nchamber. The suits of armor along"
                      "\nthe walls begin to move.",
                      "\nMetal plates clutter to the ground,"
                      "\nloudly echoing off the walls. All"
                      "\nof the guards have been defeated.",
                      "B",0.3,2,True,{"Armor":3},0),
                     ("Forest of Webs",
                      "All around is a dense forest, barely"
                      "\nany light filters inside. The giant"
                      "\ncobwebs begin to shake.",
                      "\nWith three spiders less, this dark"
                      "\nhabitat has become a slightly"
                      "\nsafer place.",
                      "B",0.5,3,True,{"Spider":3},0),
                     ("Dragon's Lair",
                      "The mountain tunnel opens up into"
                      "\na large cavern. Dragons guarding"
                      "\ntheir lair notice the party.",
                      "\nWith it's two guardians defeated,"
                      "\nthe treasure accumulated by the"
                      "\nbeasts is up for taking.",
                      "B",0.3,2,True,{"Dragon":2},0),
                     ("Mirror Hall",
                      "The party walks through a narrow"
                      "\ncorridor filled with mirrors."
                      "\nTheir reflections begin to move.",
                      "\nThe mirrors shatter, and the"
                      "\ndoubles are gone with them."
                      "\nOnly the originals remain.",
                      "B",0.2,2,True,{"Double":3},0),
                     ("Enemy Camp",
                      "The warm light of a fire along with"
                      "\na smell of stew turn out to be from"
                      "\nan enemy campsite, not allies'.",
                      "\nAs the sounds of battle die out,"
                      "\nthe light of nearby campfires starts"
                      "\nto dim, and a new day begins.",
                      "B",0.1,4,True,{"Goblin":5,"Spider":2},0),
        #FIND ENCOUNTERS
                     ("Dragon Hoard",
                      "The dragon nest is thankfully not"
                      "\nguarded. With the creatures gone"
                      "\ntheir treasure is easily taken.",
                      "\nThe party manages to find some"
                      "\nuseful strength artifacts for their"
                      "\nnext battle.",
                      "F",0.3,1,True,{},2),
                     ("Sword in Stone",
                      "A sword is embedded in a big rock"
                      "\non top of an elaborate altar."
                      "\nWho shall pull it out?",
                      "\nThe sword's edge is gleaming"
                      "\nin sunlight. The character feels"
                      "\nempowered by this event.",
                      "F",0.1,3,False,{},4),
        #RESPITE ENCOUNTERS
                     ("Hot Spring",
                      "The calm after the storm is a"
                      "\nperfect time for respite. Even"
                      "\nmore so with a relaxing bath.",
                      "\nThe party feels refreshed, and"
                      "\neveryone's ready for the coming"
                      "\nfuture challenges.",
                      "R",0.3,3,True,{},1),
                     ("Found Potion",
                      "An unmarked potion is laying on"
                      "\nthe side of the road. Who should"
                      "\nit go to?",
                      "\nThis potion has turned out to be"
                      "\nhealing. The chosen character gained"
                      "\na good portion of their hp.",
                      "R",0.3,1,False,{},0.5),
        #TRAP ENCOUNTERS
                     ("Found Potion",
                      "An unmarked potion is laying on"
                      "\nthe side of the road. Who should"
                      "\nit go to?",
                      "\nThis potion has turned out to be"
                      "\npoison. The chosen character lost"
                      "\na good portion of their hp.",
                      "T",0.2,1,False,{},-0.5),
                     ("Hunting Traps",
                      "While walking through a dense"
                      "\nforest the party steps into an"
                      "\nunmarked field of hunting traps.",
                      "\nThe wounds will heal with time,"
                      "\nbut they may prove to be dangerous"
                      "\nin coming conflicts.",
                      "T",0.2,2,True,{},-0.35),
                 ]]