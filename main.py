from classes.game import person
from classes.game import bcolors
from classes.magic import spell
from classes.inventory import item
import random


print("\n\n")

#make black magic
fire = spell("fire", 25, 600, "black")
thunder = spell("Thunder", 25, 600, "black")
blizzard = spell("Blizzard", 25, 600, "black")
meteor = spell("Meteor", 40, 1200, "black")
quake = spell("Quake", 14, 140, "black")


#white magic 
cure= spell("Cure", 25, 650, "white")
cura = spell("cura", 32, 1500, "white")


#creating items
potion = item("potion", "potion", "heals 50 HP", 50)
hipotion = item("Hi-potion", "potion", "heals 100 HP", 100)
superpotion = item("super potion", "potion", "heals 1000 HP", 1000)
elixer = item("elixer", "elixer", "fully restores HP/MP of one party member", 9999)
hielixer = item("MegaElixer", "elixer", "fully restores party's HP/MP", 9999)

grenade = item("grenade", "attack", "deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire,meteor, cure]
player_items = [{"item":potion,"quantity": 15}, {"item":hipotion, "quantity": 5},
                 {"item":superpotion, "quantity":5}, {"item":elixer, "quantity":5},
                 {"item":hielixer, "quantity":2}, {"item":grenade, "quantity":5}]

#instantiate person 
player1 = person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = person("Robot:", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = person("imp  ", 3260, 132, 300, 34, enemy_spells, player_items)
enemy2 = person("magus", 11200, 701, 525, 25, enemy_spells, player_items)
enemy3 = person("Rob  ", 3260, 132, 300, 34, enemy_spells, player_items)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "ENEMY ATTACKS!!!" + bcolors.ENDC)

while running:
    print("===============")

    print("\n")
    print("NAME                HP                                         MP")
    for player in players:
        player.get_stats()
        print("\n")

    for enemy in enemies:
            enemy.get_enemy_stats()

    for player in players:
        player.choose_action() 
        choice = input("    Choose action:")
        index = int(choice) -1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("\nYou attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage to " + enemies[enemy].name)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + "has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue
                    
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL+ "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals "+ enemy.name +"for", str(magic_dmg), "HP." + bcolors.ENDC )
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + "    "+ spell.name.replace(" ", "")+  + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item:")) - 1

            if item_choice == 0:
                continue

            item = player.item[item_choice] ["item"]

            if player.item[item_choice] ["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "none left" + bcolors.ENDC)
                continue

            player.item[item_choice] ["quantity"] -= 1
            
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " Fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_action(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to "+ enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
            
       #check if player won     
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win" + bcolors.ENDC)
        running = False
    
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you" + bcolors.ENDC)
        running = False

        #enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            #choose attack
            enemy_dmg = enemies[0].generate_damage()
            target = random.randrange(0,3)

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ","")+" for", enemy_dmg)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell(enemy)
            enemy.reduce_mp(spell.cost)
            print("Enemy chose ", spell, " damage is", magic_dmg)


