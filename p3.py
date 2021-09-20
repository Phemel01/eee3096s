# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
GPIO.setmode(GPIO.BOARD)
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
DC1 = 0
DC2 =0
buzzer = None
eeprom = ES2EEPROMUtils.ES2EEPROM()
user_guess = 0
rnum=0;# set it up in the main function
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    #testing eeprom
    eeprom.clear(2048)
    eeprom.populate_mock_scores()     
    
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    for i  in range(3):
              x=raw_data[i]
              
              print("%d-%s took %d guesses"%(i+1,x[0],x[1]))
    # print out the scores in the required format



# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(11, GPIO.OUT)
    
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    print("2.2")
    # Setup PWM channels
   
    GPIO.setup(32, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT) 
    myled = GPIO.PWM(32,100)
    myBuz = GPIO.PWM(33,100)
    print("2")
    myled.start(0)
    myBuz.start(0)
    print("5")
    # Setup debouncing and callbacks
    GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback1, bouncetime=200)
    GPIO.add_event_detect(18, GPIO.FALLING, callback=my_callback2, bouncetime=200)
    print("7")


# Load high scores
def my_callback1():
    user_guess+=1
    
def my_callback2():
    user=1

def fetch_scores():
    # get however many scores there are
    score_count = 0
    ndata=eeprom.read_block(0,4)
    print(ndata[0])
    rd= eeprom.read_block(0,ndata[0]*4+4)
    print(rd)
    scores=[]
    i=0
    while True:
          f=[]
          wd=(chr(rd[i])+chr(rd[i+1])+chr(rd[i+2]))

          f.append(wd)
          f.append(rd[i+3])
          if i+4>=len(rd):
              break
          if  rd[i+4]==0 and  f[1]==0 :
              break
          elif f[1]!=0 :
              score_count+=1
              scores.append(f)
          i+=4

    # Get the scores
    score_count = ndata[0]
    # convert the codes back to ascii
    print(scores)
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    s_count, ss = fetch_scores() 
    name=input("Enter 3 letter name")
    eeprom.clear(2048)
    eeprom.write_block(0, [s_count])
    ws=[]
    tb=1
    for char in name:
             if tb>=3:
                break
             else:
                ws.append(ord(char))
    ss.append(ws+[user_guess])
    ss.sort(key=lambda x: x[1])
    for i, sc in enumerate(ss):
              dwrite=[]
              for ch in sc[0]:
                      dwrite.append(ord(ch))
              dwrite.append(sc[1])
              eeprom.write_block(i+1,dwrite)
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    if GPIO.output(15) == LOW:
        if GPIO.output(13)== LOW:
            if GPIO.output(11)== LOW:
                GPIO.output(11, GPIO.HIGH)
            else:
                GPIO.output(11, GPIO.LOW)
                GPIO.output(13, GPIO.HIGH)
        else:
            if GPIO.output(11)==LOW:
                GPIO.output(11, GPIO.HIGH)
            else:
                GPIO.output(11, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)
                GPIO.output(15, GPIO.HIGH)
    else:
        if GPIO.output(13)==LOW:
            if GPIO.output(11)==LOW:
                GPIO.output(11, GPIO.HIGH)
            else:
                GPIO.output(11, GPIO.LOW)
                GPIO.output(13, GPIO.HIGH)
        else:
            if GPIO.output(11)==LOW:
                GPIO.output(11, GPIO.HIGH)
            else:
                GPIO.output(11, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)
                GPIO.output(15, GPIO.HIGH)
                     
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    
    #converts led count to number  
    user_guess=0;
    if GPIO.output(11)==HIGH:
        user_guess+=1
    if GPIO.output(13)==HIGH:
        user_guess+=2
    if GPIO.output(15)==HIGH:
        user_guess+=4
    # Compare the actual value with the user value displayed on the LEDs   
    if user_guess==rnum:
         pass
    else:
        accuracy_leds()
        trigger_buzzer()
    
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    
    if user_guess>rnum:
        brightness=100*(8-user_guess)/(8-rnum)
    else:
        brightness= 100*(user_guess/rnum)
      
    myled.changeDutyCycle(brightness)
    
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    mybuz.changeDutyCycle(50)
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    if abs(rnum-user_guess)>=3:
        mybuz.changeFrequency(1)
    
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    if abs(rnum-user_guess)==2:
        mybuz.changeFrequency(2)
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    if abs(rnum-user_guess)==1:
        mybuz.changeFrequency(4)
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        print("here")
        setup()
        print("1")
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
