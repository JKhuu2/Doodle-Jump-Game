#Jennifer Khuu jtk2eh
#Stephen Krepich spk5mr

#we made a platformer game where the character has to jump on top of continuous platforms moving in a vertical direction without missing a platform or lagging behind the camera
#goal - collect the most coins before the game is over

#required features:
#user input - use the UP arrow key to jump and the LEFT and RIGHT arrow kids to move horizontally
#graphics/images - used the protagonist from the popular platformer game Hollow Knight as our playable character
#platforms were displayed as colored blocks and coins were yellow squares
#start screen - it's the first thing displayed once you run the code
#small enough window - it's not larger than gamebox.Camera(800, 600)

#optional requirements:
#collectibles - collect yellow coins to increase your score
#scrolling level - platforms are continously drawn upwards until the game is over
#timer - used to know when to transition to the next level
#multiple levels - with each level, the camera moves faster and faster

import pygame
import gamebox
import random

camera=gamebox.Camera(800,600)

platforms = [
    gamebox.from_color(150, 300, 'blue', 100, 30),
    gamebox.from_color(100, 100, 'blue', 100, 30),
    gamebox.from_color(500, 0, 'blue', 100, 30),
    gamebox.from_color(300, 200, 'pink', 100, 30),
    gamebox.from_color(400, 100, 'pink', 100, 30),
    gamebox.from_color(200, 0, 'pink', 100, 30),
    gamebox.from_color(600, -100, 'pink', 100, 30),
    gamebox.from_color(300, -100, 'blue', 100, 30)]

#white platforms are pseudo-platforms that the character can't jump on and will fall right through
white_platforms=[gamebox.from_color(500, 250, 'white', 100, 30),
    gamebox.from_color(600, 100, 'white', 100, 30),
    gamebox.from_color(100, -100, 'white', 100, 30)]

character = gamebox.from_image(150, 200, "hollow-knight-image.png")
character.width=75
character.facing = 'right'
score=0
time=0

coins=[gamebox.from_color(200,200,'yellow',10,10),
       gamebox.from_color(300,100,'yellow',10,10),
       gamebox.from_color(100,0,'yellow',10,10)]

startscreen=[gamebox.from_text(400,camera.top+100,'Hollow Knight Jump',50,'white',False),
             gamebox.from_text(400,camera.top+150,'By: Jennifer Khuu (jtk2eh) and Stephen Krepich (spk5mr)',25,'white'),
             gamebox.from_text(400,camera.top+200,'The objective of the game is to get the highest score by ',25,'white',False),
             gamebox.from_text(400,camera.top+250,'collecting the most coins without falling down or getting behind.',25,'white',False),
             gamebox.from_text(400,camera.top+300,'Use the UP arrow to jump and the RIGHT and LEFT arrow keys to move side-to-side',25,"white",False), #added what keys to use
             gamebox.from_text(400,camera.top+350,'There are three levels with increasing speeds.',25,"white",False),
             gamebox.from_text(400,camera.top+400,"DON'T jump on the white platforms.",25,'white'),
             gamebox.from_text(400,camera.top+450,'Tap SPACE to start',40,'white')]

game_on=False

def every_frame(keys):
    global score
    global time
    global game_on
    camera.clear('dark blue')
    if game_on==False:
        for text in startscreen:
            camera.draw(text)
        camera.display()
        if pygame.K_SPACE in keys:
            game_on=True
    if game_on==True:
        camera.move(0, -2)
        for thing in platforms:
            if thing.top > camera.bottom + 100:
                platforms.remove(thing)
        for thing in white_platforms:
            if thing.top > camera.bottom+100:
                white_platforms.remove(thing)
        for coin in coins:
            if coin.top>camera.bottom+100:
                coins.remove(coin)
        if coins[-1].bottom>camera.top:
            new_coin=gamebox.from_color(
                random.randrange(100, 700), camera.top - 100,
                'yellow', 10, 10)
            coins.append(new_coin)
        if platforms[-1].bottom > camera.top:
            new_platform = [
                gamebox.from_color(200, camera.top - 100,'blue', 100, 30),
                gamebox.from_color(500, camera.top - 100,'pink', 100, 30),
                gamebox.from_color(300, camera.top - 200, 'pink', 100, 30),
                gamebox.from_color(600, camera.top - 200, 'blue', 100, 30),
                gamebox.from_color(400, camera.top - 300, 'blue', 100, 30),
                gamebox.from_color(600, camera.top - 300, 'pink', 100, 30),
                gamebox.from_color(300, camera.top - 400, 'pink', 100, 30),
                gamebox.from_color(600, camera.top - 400, 'blue', 100, 30),
            ]
            platforms.extend(new_platform)
        if white_platforms[-1].bottom>camera.top:
            new_white_platform = [gamebox.from_color(200, camera.top - 300, 'white', 100, 30),
                                  gamebox.from_color(100, camera.top - 200, 'white', 100, 30),
                                  gamebox.from_color(100, camera.top - 1000, 'white', 100, 30),
                                  gamebox.from_color(200, camera.top - 1100, 'white', 100, 30),
                                  gamebox.from_color(100, camera.top - 1200, 'white', 100, 30),
                                  ]
            white_platforms.extend(new_white_platform)

        # motion
        if pygame.K_LEFT in keys:
            character.x -= 6
            if character.facing == 'right':
                character.flip()
                character.facing = 'left'
        if pygame.K_RIGHT in keys:
            character.x += 6
            if character.facing == 'left':
                character.flip()
                character.facing = 'right'

        # jump
        if pygame.K_UP in keys:
            for thing in platforms:
                if character.bottom_touches(thing):
                    # if in contact with platform
                    character.speedy = -35

        #gravity
        character.speedy += 3
        character.move_speed()

        # bump into platform
        for thing in platforms:
            character.move_to_stop_overlapping(thing)

        camera.draw(character)
        for thing in platforms:
            camera.draw(thing)
        for thing in white_platforms:
            camera.draw(thing)
        for coin in coins:
            camera.draw(coin)
            if coin.touches(character):
                coins.remove(coin)
                score+=1
        score_label=gamebox.from_text(400,camera.top+20,'Score: '+str(score),30,'yellow')
        score_label.move_speed()
        time += 0.1
        time_label = gamebox.from_text(750, camera.top + 20, 'Time: ' + str(int(time)), 30, 'white')
        time_label.move_speed()
        if time>=30 and time<60:
            camera.move(0,-3)
        if time>=30 and time<33:
            level_2=gamebox.from_text(camera.x,camera.y,'Level 2',100,'white')
            camera.draw(level_2)
        if time>=60:
            camera.move(0,-4)
        if time>=60 and time<63:
            level_3 = gamebox.from_text(camera.x, camera.y, 'Level 3', 100, 'white')
            camera.draw(level_3)
        camera.draw(time_label)
        camera.draw(score_label)
        if character.top > camera.bottom:
            camera.draw("GAME OVER!", 100, "white", 400, 200)
            camera.draw('Score: '+str(score),50,'yellow',400,300)
            gamebox.pause()
        camera.display()

gamebox.timer_loop(30, every_frame)
