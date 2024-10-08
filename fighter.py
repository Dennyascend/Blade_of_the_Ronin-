import pygame 
class Fighter():
    def __init__(self,player, x, y, flip,data, sprite_sheet, animation_steps,sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  #0;attack1 #1;attack2 #2;attack3 3;death #4;idle #5;run #6;jump #7;take hit #8;fall
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]  
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80,180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown =1000
        self.attack_sound = sound 
        self.hit = False
        self.last_attack =0 
        self.health = 100
        self.alive = True 
        

    def load_images(self, sprite_sheet, animation_steps):
    # extract images from spritesheet
     animation_list = []
     num_rows = sprite_sheet.get_height() // self.size
     row_num = 0
     x_offset = 0
     for animation in animation_steps:
        temp_img_list = []
        for x in range(animation):
            temp_img = sprite_sheet.subsurface(x_offset * self.size, row_num * self.size, self.size, self.size)
            temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            x_offset += 1
            if x_offset >= sprite_sheet.get_width() // self.size:
                x_offset = 0
                row_num += 1
                if row_num >= num_rows:
                    row_num = 0
        animation_list.append(temp_img_list)
        
     return animation_list

    def move(self, screen_width,screen_height,surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0 
        #get keypresses
        key = pygame.key.get_pressed()
    
        if self.alive == True and round_over == False :
        #check player 1 controls
         if self.player == 1:
            
            #movements
        
            if key[pygame.K_a]:
                dx =-SPEED
                self.running = True
            if key[pygame.K_d]:
                dx = SPEED  
                self.running = True  
            #jump
            if key[pygame.K_w]  and self.jump == False:
                self.vel_y= -30
                self.jump = True

            #attack
            if self.attacking == False:
             if key[pygame.K_e] or key[pygame.K_q]:
                self.attack(surface, target)
                #determine which attack is used
                if key[pygame.K_e]:
                    self.attack_type = 1
                if key[pygame.K_q]:
                    self.attack_type = 2
            
        #check player 2 controls
        if self.player == 2:
            
            #movements
        
            if key[pygame.K_LEFT]:
                dx =-SPEED
                self.running = True
            if key[pygame.K_RIGHT]:
                dx = SPEED  
                self.running = True  
            #jump
            if key[pygame.K_UP]  and self.jump == False:
                self.vel_y= -30
                self.jump = True

        #attack
            if self.attacking == False:
             if key[pygame.K_KP1] or key[pygame.K_KP2]:
               self.attack(surface, target)
            #determine which attack is used
            if key[pygame.K_KP1]:
                self.attack_type = 1
            if key[pygame.K_KP2]:
                self.attack_type = 2
           
        
        #apply gravity
        self.vel_y +=GRAVITY
        dy += self.vel_y   


        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width -self.rect.right   
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #ensure player face each
        if self.alive == True:
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True
            #update player postion
            self.rect.x += dx
            self.rect.y += dy
  
    #handle animation updates
    def update(self):
             
       #check what action , player is performing 
       if self.health <=0:
          self.health = 0
          self.update_action(6)
          self.alive = False
       elif self.hit == True:
        self.update_action(4)
       elif self.attacking ==True:
          if self.attack_type == 1 :
            self.update_action(1)
          elif self.attack_type == 2 :
            self.update_action(2)  
            
       elif self.jump == True:
          self.update_action(5)

       elif self.running == True:
          self.update_action(3)
       else:
          self.update_action(0) #0 idle , #1 attack2 , #2 attack3 , #3 run , #4 hit , #5 jump , #6 jump
          
        #for attacking and stopping attack animation 
       animation_cooldown = 80
       self.image = self.animation_list[self.action][self.frame_index % len(self.animation_list[self.action])]
       
       #check if enough time is passed since the last update
       if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
        self.frame_index += 1
        self.update_time = pygame.time.get_ticks()

        if self.action == 6:  # Death animation
          if self.frame_index >= len(self.animation_list[self.action]):
            # Remove fighter from game
            self.alive = False
            self.frame_index = len(self.animation_list[self.action])-1
        
         #check if attack is executed 
        if self.attacking == True:
           if self.frame_index >= len(self.animation_list[self.action]):
              self.attacking = False
              self.frame_index =0 
    
        if self.action == 4:
           if self.frame_index >= len(self.animation_list[self.action]):
              self.hit = False
              #if player is in middle of attack then attack is stopped
              self.attacking = False
              self.attack_cooldown = 1000
              self.frame_index =0 

        
                         
         #check if animation has finished 
        if self.frame_index >= len(self.animation_list[self.action]):
         self.frame_index = 0
        self.update_time = pygame.time.get_ticks()  
 
        

    def attack(self, surface, target):
     current_time = pygame.time.get_ticks()
     if current_time - self.last_attack >= self.attack_cooldown:  # 1000 milliseconds = 1 second
         self.attacking = True
         self.attack_sound.play()
         self.last_attack = current_time
         attacking_rect = pygame.Rect(self.rect.centerx - (3*self.rect.width * self.flip), self.rect.y, 3*self.rect.width, self.rect.height)
         if attacking_rect.colliderect(target.rect):
          target.health -= 10
          target.hit = True
         

        
    def update_action(self, new_action):
       #check if new action is different to previous one 
       if new_action != self.action:
         self.action = new_action
       #update animation setting 
         self.frame_index = 0
         self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
      img = pygame.transform.flip(self.image, self.flip, False)
     
      surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale) , self.rect.y - (self.offset[1] * self.image_scale)))
    