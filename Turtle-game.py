
import turtle
import random
import time
import sqlite3

class Game:
    
    def __init__(self):
                
        #Game status variable
        self.game_status = True

        #heading variable (stores the current direction of the player)
        self.current_heading = "right"
        
        #The Variable that is used to toggle the pause the game
        self.is_paused = False
        self.pause_message = turtle.Turtle()
        self.pause_message.hideturtle()
        self.pause_on_screen = False
        self.pause_time = 0
        self.pause_current_heading = "right"
        
        #Wait Variables to hold the movement checks and updates
        self.is_waiting = False
        self.is_waiting_after_game = False
        
        #Timer Variables
        self.previous_time = 0

        ### FOOD DETAILS ###
        #The variable that stores the number of food on the field
        self.food_count = 0
        self.max_food_count = 5
        self.food_data = []
        
        #Variables that govern Speed of the turtle
        self.player_speed = 2
        self.max_player_speed = 8
        self.speed_variable = 0
        
        #Variable that stores game score
        self.game_score = 0
        
        #Variable that stores lives
        self.turtle_lives = 1

        #Fonts
        self.score_font = ("Courier", 20, "")
        self.screen_font = ("Courier", 30, "bold")
        
        #Double Points Variables (Violet Pellet)
        self.double_points = False
        self.double_points_time = 0
        self.points_multiplier = 1
        
        #Speed Bost Variables (Blue Pellet)
        self.speed_boost = False
        self.speed_boost_time = 0
        self.speed_multiplier = 1
        
        #Speed Bost Variables (Purple Pellet)
        self.invincibility = False
        self.invincibility_time = 0

        #Game Reset Variables
        self.reset = False
        
        #player details
        self.player_name = ""
    
    # Function to Spawn A food pellet     
    def spawn_food(self):
        
        #Creating a new pellet
        food_turtle = turtle.Turtle()
        food_turtle.shape("circle")
        food_turtle.color("lime")
        food_turtle.type = "lime"
        food_turtle.time = 0
        food_turtle.timeout = random.randint(5,10)
        food_turtle.speed(0)
        food_turtle.penup()
        
        # Spawning pellet at random position
        position_x = random.randint(-220,200)
        position_y = random.randint(-210,170)
        food_turtle.goto(position_x,position_y)
        
        #Storing pellet in a list to be used later
        self.food_data.append(food_turtle)
        
    #function to check food timeout
    def food_timeout(self):
        
        #checking timeout for all food turtles
        for food in self.food_data:
            
            #checking if the food is timed out
            if food.time > food.timeout:
                
                #respawning food if timed out
                self.respawn(food)

    # Function that moves the food to random loaction
    def respawn(self,food_turtle):
        
        #Getting Random Chance Variable
        random_chance = int(random.random()*100)
        
        if food_turtle.type == "white":
            self.lives_increase(1)
        
        #If the value of chance variable is 0 then spawn extra life food pellet
        if random_chance < 1:
            
            # Making the life Turtle pellet
            food_turtle.shape("turtle")
            food_turtle.color("white")
            food_turtle.type = "white"
            
            #respawning the turtle
            position_x = random.randint(-220,200)
            position_y = random.randint(-210,170)
            food_turtle.goto(position_x,position_y)
            
        #If the value of chance variable is 5 or lower but above 0 then spawn ability food pellet
        elif random_chance < 6:
            
            ability_chance = int(random.random()*100)

            if ability_chance < 26:
                
                # Making the gold Turtle (50 pointer)
                food_turtle.shape("circle")
                food_turtle.color("yellow")
                food_turtle.type = "gold"
            
            elif ability_chance < 51:
                
                # Making the violet Turtle (points boost)
                food_turtle.shape("square")
                food_turtle.color("violet")
                food_turtle.type = "violet"
            
            elif ability_chance < 76:
                
                # Making the blue Turtle (speed boost)
                food_turtle.shape("square")
                food_turtle.color("blue")
                food_turtle.type = "blue"
            
            else:
                
                # Making the purple Turtle (invincibility)
                food_turtle.shape("triangle")
                food_turtle.color("purple")
                food_turtle.type = "purple"
            
            position_x = random.randint(-220,220)
            position_y = random.randint(-220,220)
            food_turtle.goto(position_x,position_y)
            
        else:    
            
            ability_chance = int(random.random()*100)

            if ability_chance <=10:
                #making the red pellets
                food_turtle.shape("circle")
                food_turtle.color("red")
                food_turtle.type = "red"

            else:
                #making the regular food
                food_turtle.shape("circle")
                food_turtle.color("lime")
                food_turtle.type = "lime"

            #repositioning 
            position_x = random.randint(-220,220)
            position_y = random.randint(-220,220)
            food_turtle.goto(position_x,position_y)

        food_turtle.time = 0
        food_turtle.timeout = random.randint(5,10)

    #Function to increase Game score and Game speed Variable
    def score_increase(self, points):

        self.game_score += points
        self.speed_variable += points
        self.scoreboard.clear()
        self.scoreboard.write("Score:{}".format(self.game_score) , align="left", font=self.score_font)
      
    #function to check for border collisions  
    def check_border(self):
        
        if self.player.xcor() > 250 or self.player.ycor() > 250 or self.player.ycor() < -250 or self.player.xcor() < -250:
            self.lives_increase(-1)
        
    #Function to increase Game score and Game speed Variable
    def lives_increase(self, points):
        
        self.turtle_lives += points

        #Ending the game if necessary
        if self.turtle_lives <= 0:
            self.game_over()

        #Checking a life has been lost
        if self.turtle_lives > 0:
            self.is_waiting = True
            if points < 0:
                self.player.goto(0,0)
                for i in range(3,0,-1):
                    self.pause_message.color("red")
                    self.pause_message.write("{}!".format(i), align="center", font=self.screen_font)
                    time.sleep(0.5)
                    self.pause_message.clear()
                    time.sleep(0.35)
            self.is_waiting = False
            self.go_up()
            
        self.lives.clear()
        self.lives.write("Lives:{}".format(self.turtle_lives) , align="right", font=self.score_font)
        
    #Function to add score to database
    def insert_into_db(self):
        self.c.execute("insert into game_scores(player_name,player_score) values(\"{}\",{})".format(self.player_name,self.game_score))
        self.conn.commit()
    
    #function to get top 3 score from database
    def get_from_db(self):
        data = self.c.execute("select * from game_scores order by player_score desc limit 5")
        return data
    
    #end's the game
    def game_over(self):

        #inserting score into the db
        self.insert_into_db()
        
        #getting the top 3 score
        data = self.get_from_db()
        
        #printing the Game over sign
        self.is_waiting = True
        for i in range(3):
                self.pause_message.color("red")
                self.pause_message.write("{}!".format("Game Over"), align="center", font=self.screen_font)
                time.sleep(0.5)
                self.pause_message.clear()
                time.sleep(0.35)
        self.is_waiting = False
        self.go_up()
        
        #printing the Highscores
        name_x,name_y = -100,100
        score_x,score_y = 100,100
        
        #write on screen
        self.scoreboard.pu()
        self.scoreboard.goto(name_x,name_y)
        self.scoreboard.write("Player", align="center", font=self.score_font)
        
        self.lives.pu()
        self.lives.goto(score_x,score_y)
        self.lives.write("Score", align="center", font=self.score_font)
        
        #printing the scorebord
        for i in data:
            name_y -= 30
            self.scoreboard.goto(name_x,name_y)
            self.scoreboard.write("{}".format(i[0]), align="center", font=self.score_font)
            
            score_y -= 30
            self.lives.goto(score_x,score_y)
            self.lives.write("{}".format(i[1]), align="center", font=self.score_font)
        
        time.sleep(5)
        
        #Terminate's main game loop
        self.game_status = False
    
    #function that incresases player speed
    def speed_increase(self,amount):
        
        if self.player_speed < self.max_player_speed:
            self.player_speed += amount
        
    # Function that checks if a food pellet has been eaten
    def has_consumed(self):
        
        for food in self.food_data:
            
            if food.distance(self.player) < 25:
                
                #Increase Game Score
                if food.type == "lime":
                    self.score_increase(10*self.points_multiplier)
                elif food.type == "gold":
                    self.score_increase(50*self.points_multiplier)
                elif food.type == "red":
                    self.score_increase(-20)
                else:
                    self.score_increase(20*self.points_multiplier)
                
                if food.type == "violet":
                    
                    if not self.double_points:
                        self.double_points = True
                        self.points_multiplier = 2
                        self.score_increase(20)
                        self.double_points_time = int(time.time())
                        
                if food.type == "blue":
                    
                    if not self.speed_boost:
                        self.speed_boost = True
                        self.speed_multiplier = 1.25
                        self.speed_boost_time = int(time.time())

                if food.type == "purple":
                    
                    if not self.invincibility:
                        self.invincibility = True
                        self.invincibility_time = int(time.time())
                
                if food.type == "red":

                    #Respawn Food
                    self.respawn(food)
                    self.lives_increase(-1)
                    
                #Respawn Food
                self.respawn(food)
                    
                #Increase speed
                if self.speed_variable >= 100:
                    self.speed_increase(1)
                    self.speed_variable = 0

    #Function to check for all the power-ups
    def check_ups(self):
        
        # When the violet power up is active
        if self.double_points:
            
            # If the 10 second timer is done then disable the powerup
            if self.double_points_time >= 10:
                self.double_points = False
                self.points_multiplier = 1
                self.double_points_time = 0 
                
        if self.speed_boost:
            
            # If the 10 second timer is done then disable the powerup
            if self.speed_boost_time >= 10:
                self.speed_boost = False
                self.speed_multiplier = 1
                self.speed_boost_time = 0 
                
        if self.invincibility:
            
            # If the 10 second timer is done then disable the powerup
            if self.invincibility_time >= 10:
                self.invincibility = False
                self.invincibility_time = 0 
               
        
    # function that starts the game loop
    def start(self):
        
        #larger turtle polygon
        turtle_x2=((0,32), (-4,28), (-2,20), (-8,14),(-14,18), (-18,16),
                    (-12,10), (-14,2), (-10,-6), (-16,-12),
                    (-12,-16), (-8,-5), (0,-14), (8,-10), (12,-16), (16,-12),
                    (10,-6), (14,2), (12,10), (18,16), (14,18), (8,14), (2,20),(4,28))
        
        #setting up the canvas
        self.wn  = turtle.Screen()
        self.wn.cv._rootwindow.resizable(False, False)
        self.wn.title("Turtle Game")
        self.wn.setup(500,500)
        self.wn.bgpic("assets/background.gif")
        
        #getting player name from the user
        self.player_name = turtle.textinput("Who's Playing","Player Name")
        if self.player_name == "":
            self.player_name = "Guest"
            
        #creating database if there is no database or table
        self.conn = sqlite3.connect("Score.db")
        self.c = self.conn.cursor()
        self.c.execute("create table if not exists game_scores(player_name varchar(50) not null, player_score integer not null)")
        
        #Points Scoreboard 
        self.scoreboard = turtle.Turtle()
        self.scoreboard.hideturtle()
        self.scoreboard.color("white")
        self.scoreboard.up()
        self.scoreboard.goto(-240,220)
        self.scoreboard.write("Score:{}".format(self.game_score), align="left", font=self.score_font) 
        
        #Life Scoreboard
        self.lives = turtle.Turtle()
        self.lives.hideturtle()
        self.lives.up()
        self.lives.color("white")
        self.lives.goto(240,220)
        self.lives.write("Lives:{}".format(self.turtle_lives), align="right", font=self.score_font)
        
        #setting up the player character
        self.player = turtle.Turtle()
        turtle.register_shape("assets/turtle/turtle-up.gif")
        turtle.register_shape("assets/turtle/turtle-down.gif")
        turtle.register_shape("assets/turtle/turtle-left.gif")
        turtle.register_shape("assets/turtle/turtle-right.gif")
        self.player.shape("assets/turtle/turtle-right.gif")
        self.player.color("white")
        self.player.penup()
        self.player.speed(0)
        
        #binding the player charter movement to w,a,s and d
        self.wn.onkey(self.go_up, "w")
        self.wn.onkey(self.go_left, "a")
        self.wn.onkey(self.go_down, "s")
        self.wn.onkey(self.go_right, "d")
        self.wn.onkey(self.pause, "p")
        
        self.previous_time = time.time()

        #main loop which keeps the player alive
        while self.game_status:
            
            try:
                #updating turtle
                turtle.update()
                
                #pushing the player forward if game is not paused
                if not self.is_paused:
                    self.player.forward(self.player_speed*self.speed_multiplier)
                
                if not self.is_paused:
                    self.food_timer()

                #spawning food on the field if there are none
                if self.max_food_count > self.food_count:
                    self.spawn_food()
                    self.food_count += 1

                #Checking if a food pellet has been consumed
                self.has_consumed()
                
                #chechink for border Collision
                self.check_border()
                
                # Checking for power ups and time outs
                self.check_ups()
                
                #checking if food timesout
                self.food_timeout()

                # Listening for key contrls and updating 
                self.wn.listen()
                self.wn.update()
            except:
                break

        turtle.bye()

    #function to update the timer of the food per second
    def food_timer(self):

        #checking if one second has passed 
        if int(time.time() - self.previous_time) >=1:

            #updating the time for each elements
            for food in self.food_data:
                food.time += 1

            #Updating the time variable for the power up
            self.double_points_time += 1 
            self.speed_boost_time += 1
            self.invincibility_time += 1

            #updating the previous time for
            self.previous_time = time.time()


    #Function that changes the player character's heading to up
    def go_up(self):

        #Checking if the game is paused
        if not self.is_paused and not self.is_waiting:
            
            #setting the current turtle image
            self.player.shape("assets/turtle/turtle-up.gif")
            
            #setting up the movement of the player based on current heading
            if self.current_heading == "right":
                self.player.left(90)
            elif self.current_heading == "left":
                self.player.left(-90)
            elif self.current_heading == "down":
                self.player.left(180)
            
            #updating the universal heading variable
            self.current_heading = "up"

    #Function that changes the player character's heading to left
    def go_left(self):

        #Checking if the game is paused
        if not self.is_paused and not self.is_waiting:
            
            #setting the current turtle image
            self.player.shape("assets/turtle/turtle-left.gif")
            
            #setting up the movement of the player based on current heading
            if self.current_heading == "right":
                self.player.left(180)
            elif self.current_heading == "up":
                self.player.left(90)
            elif self.current_heading == "down":
                self.player.left(-90)
            
            #updating the universal heading variable
            self.current_heading = "left"

    #Function that changes the player character's heading to right
    def go_right(self):

        #Checking if the game is paused
        if not self.is_paused and not self.is_waiting:
            
            #setting the current turtle image
            self.player.shape("assets/turtle/turtle-right.gif")
            
            #setting up the movement of the player based on current heading
            if self.current_heading == "left":
                self.player.left(180)
            elif self.current_heading == "down":
                self.player.left(90)
            elif self.current_heading == "up":
                self.player.left(-90)
            
            #updating the universal heading variable
            self.current_heading = "right"

    #Function that changes the player character's heading to down
    def go_down(self):

        #Checking if the game is paused
        if not self.is_paused and not self.is_waiting:
            
            #setting the current turtle image
            self.player.shape("assets/turtle/turtle-down.gif")
            
            #setting up the movement of the player based on current heading
            if self.current_heading == "left":
                self.player.left(90)
            elif self.current_heading == "right":
                self.player.left(-90)
            elif self.current_heading == "up":
                self.player.left(180)

            #updating the universal heading variable
            self.current_heading = "down"

    #function to toggle the game from being paused
    def pause(self):
        
        # Changing Pause Variable
        self.is_paused = not self.is_paused

        #storing current heading of the turtle
        if self.is_paused:
            self.pause_current_heading = self.current_heading
            self.pause_time = time.time()
        
        #when the game is resumed changing heading to the right heading
        if not self.is_paused:

            if self.pause_current_heading == "right":
                self.go_right()
            elif self.pause_current_heading == "left":
                self.go_left()
            elif self.pause_current_heading == "up":
                self.go_up()
            elif self.pause_current_heading == "down":
                self.go_down()

        # Displaying Paused Text on screen
        if self.pause_on_screen:
            self.pause_message.clear()
            self.pause_on_screen = False
        else:
            self.pause_message.write("Paused!", align="center", font=self.screen_font)
            self.pause_on_screen = True

        
#initial startup 
if __name__ == '__main__':
    obj = Game()
    obj.start()
