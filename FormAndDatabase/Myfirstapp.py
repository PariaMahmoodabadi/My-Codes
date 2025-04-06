from tkinter import *
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageDraw, ImageFont,ImageTk
import random
import pygame
import mysql.connector as mc

def Paria():
    db1 = mc.connect(
    host ="localhost",
    user ="root",
    passwd ="1234",
    database='formParia'
    )
    return db1



def Shahrad():
    db2 = mc.connect(
    host ="localhost",
    user ="root",
    passwd ="1234",
    database='formShahrad'
    )
    return db2

MyProgram = Tk()
MyProgram.geometry("800x750")
MyProgram.configure(background="#f4f3d2")
MyProgram.title("Test")
bg_image= PhotoImage(file="test.png")
back=Label(MyProgram,image=bg_image).place(relwidth=1,relheight=1)

def audio1():
    pygame.mixer.init()
    pygame.mixer.music.load("DiceRoll.mp3")
    pygame.mixer.music.play()

def audio2():
    pygame.mixer.init()
    pygame.mixer.music.load("GameOver.mp3")
    pygame.mixer.music.play()

def audio3():
    pygame.mixer.init()
    pygame.mixer.music.load("success.mp3")
    pygame.mixer.music.play()
    

def dicegame():
    # Create game window
    dice = Toplevel(MyProgram)
    dice.geometry("800x600")
    dice.configure(background="#f4f3d2")
    dice.title("Dice game")

    attempts = 0  # Track number of attempts
    max_attempts = 3  # Maximum allowed attempts

    def roll_dice():
        nonlocal attempts  # Modify the outer variable
        attempts += 1  # Increment attempt counter
        
        # Roll two dice
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        
        # Winning condition (matching dice)
        if dice1 == dice2:
            messagebox.showinfo("Well done!", f"Yay, pass!\nDice 1: {dice1}, Dice 2: {dice2}")
            audio3()  # Play success sound
            dice.destroy()  # Close game window
            formShahrad()  # Open Shahrad's form
            return
        
        # Final attempt condition
        elif attempts >= max_attempts:
            messagebox.showinfo("Game Over", 
                f"Final attempt!\nDice 1: {dice1}, Dice 2: {dice2}\nBut let's go in!")
            audio2()  # Play game over sound
            dice.destroy()
            formShahrad()  # Open form even after losing
            return
        
        # Intermediate attempt (ask to continue)
        else:
            retry = messagebox.askyesno(
                "Try Again", 
                f"Attempt {attempts}/{max_attempts}\nDice 1: {dice1}, Dice 2: {dice2}\nOh no! Try again?"
            )
            if retry:
                audio1()  # Play dice roll sound
            else:
                dice.destroy()  # Close game if user declines

    # Game UI
    Label(dice, 
        text="Welcome to the game!!", 
        bg="white", 
        fg="black", 
        font="Arial 30 bold"
    ).place(x=180, y=250)
    
    Button(dice, 
        text="Let's roll it!", 
        command=roll_dice,  # Trigger dice roll
        font="Arial 10 bold"
    ).place(x=300, y=350)
    
    Button(dice, 
        text="Exit", 
        command=dice.destroy,  # Close window
        font="Arial 10 bold"
    ).place(x=400, y=350)
    

def check_credentials(username, password):
    try:
        with open("filetamrin.txt", "r") as openfile:
            for line in openfile:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    stored_username, stored_password = parts
                    if stored_username == username and stored_password == password:
                        return True
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
    return False

def password():
    form1 = Toplevel(MyProgram)
    form1.geometry("500x400")
    form1.configure(background="#f4f3d2")
    form1.title("Enter")
    
    l=Label(form1, text="Enter your username: ").place(x=200, y=150)
    tx = StringVar()
    e=Entry(form1, textvariable=tx).place(x=200, y=170)
    
    l1=Label(form1, text="Enter your password: ").place(x=200, y=200)
    tx1 = StringVar()
    e1=Entry(form1, textvariable=tx1, show='*').place(x=200, y=220)
    
    def getting():
        user = tx.get()
        passwordesh = tx1.get()
        if check_credentials(user, passwordesh):
            messagebox.showinfo("Entrance", "Login Successful Welcome "+str(user))
            form1.destroy()
            if user=="Paria" and passwordesh=="12345678":
                formParia()
            else:
                dicegame()

        else:
            m3 = messagebox.askyesno("Error", "Do you want to exit?!")
            if m3:
                form1.destroy()
            else:
                messagebox.showinfo("Back", "Back to previous page!")

    b=Button(form1, text="submit", command=getting).place(x=200, y=250)
    b1=Button(form1, text="exit form", command=form1.destroy).place(x=250, y=250)

#creating forms
class UserForm:
    def __init__(self, master, db_name, table_name):
        
        self.master = master  # Parent window
        self.db_name = db_name  # Database name (e.g., 'formParia')
        self.table_name = table_name  # Table name (e.g., 'resultParia')
        self.create_form()  # Build the form UI
    
    def create_form(self):
       
        # Form window setup
        self.form = Toplevel(self.master)
        self.form.geometry("700x700")
        self.form.configure(background="#f4f3d2")
        self.form.title("Form")

        # Labels
        Label(self.form, text=" Form ", font="Arial 20 bold").place(x=300, y=10)
        Label(self.form, text="Enter your first name: ").place(x=120, y=70)
        Label(self.form, text="Enter your last name: ").place(x=120, y=110)
        Label(self.form, text="Enter your phone num.: ").place(x=120, y=150)
        Label(self.form, text="Preferences", font="Arial 20").place(x=180, y=400)
        Label(self.form, text="Gender", font="Arial 20").place(x=180, y=200)
        Label(self.form, text="Status", font="Arial 20").place(x=190, y=300)

        # Image
        global imagecor
        imagecor = PhotoImage(file="test2.png")
        Label(self.form, image=imagecor).place(x=450, y=450)

        # Form variables
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.phone_num = StringVar()
        self.gender = StringVar(value="null")
        self.marital_status = StringVar(value="null")
        self.fav = IntVar()  # Sports
        self.fav1 = IntVar()  # Music
        self.fav2 = IntVar()  # Cooking
        self.fav3 = IntVar()  # Books

        # Entry fields
        Entry(self.form, textvariable=self.first_name).place(x=250, y=70)
        Entry(self.form, textvariable=self.last_name).place(x=250, y=110)
        Entry(self.form, textvariable=self.phone_num).place(x=250, y=150)

        # Radio buttons
        Radiobutton(self.form, text="Male", variable=self.gender, value="Male").place(x=200, y=230)
        Radiobutton(self.form, text="Female", variable=self.gender, value="Female").place(x=200, y=250)
        Radiobutton(self.form, text="Single", variable=self.marital_status, value="Single").place(x=200, y=330)
        Radiobutton(self.form, text="Married", variable=self.marital_status, value="Married").place(x=200, y=350)

        # Checkboxes
        Checkbutton(self.form, text="Sports", variable=self.fav).place(x=200, y=430)
        Checkbutton(self.form, text="Music", variable=self.fav1).place(x=200, y=450)
        Checkbutton(self.form, text="Cooking", variable=self.fav2).place(x=200, y=470)
        Checkbutton(self.form, text="Books", variable=self.fav3).place(x=200, y=490)

        # Action buttons
        Button(self.form, text="Submit", command=self.submit_form).place(x=250, y=540)
        Button(self.form, text="exit form", command=self.form.destroy).place(x=300, y=540)
    
    #submitting data into database
    def submit_form(self):
        
        try:
            # Database connection
            db = mc.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database=self.db_name
            )
            cursor = db.cursor()
            
            # Process checkbox selections
            favorites = []
            if self.fav.get(): favorites.append('Sports')
            if self.fav1.get(): favorites.append('Music')
            if self.fav2.get(): favorites.append('Cooking')
            if self.fav3.get(): favorites.append('Books')
            
            favorites_str = ', '.join(favorites)
            
            # Database insertion
            query = f"""
            INSERT INTO {self.table_name} 
            (first_name, last_name, phone_num, gender, marital_status, favorites) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                self.first_name.get(),
                self.last_name.get(),
                self.phone_num.get(),
                self.gender.get(),
                self.marital_status.get(),
                favorites_str
            )
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Data inserted successfully")
            
            # Generate output image
            self.generate_output_image()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
        finally:
            # Clean up resources
            if 'cursor' in locals(): cursor.close()
            if 'db' in locals() and db.is_connected(): db.close()
    
    def generate_output_image(self):
        """Generate a summary image of the form data"""
        info = (
            f"First Name: {self.first_name.get()}\n"
            f"Last Name: {self.last_name.get()}\n"
            f"Phone Number: {self.phone_num.get()}\n"
            f"Gender: {self.gender.get()}\n"
            f"Marital Status: {self.marital_status.get()}\n"
            f"Preferences:\n"
            f"  - Sports: {'Yes' if self.fav.get() else 'No'}\n"
            f"  - Music: {'Yes' if self.fav1.get() else 'No'}\n"
            f"  - Cooking: {'Yes' if self.fav2.get() else 'No'}\n"
            f"  - Books: {'Yes' if self.fav3.get() else 'No'}"
        )
        
        # Image processing
        backgr = Image.open("back.png")
        backgr = backgr.convert('RGBA')  
        layer = Image.new('RGBA', backgr.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)
        
        # Text positioning
        font = ImageFont.truetype("arial.ttf", 250)
        bbox = draw.textbbox((0,0), info, font=font)
        textwidth = bbox[2] - bbox[0]
        texthight = bbox[3] - bbox[1]
        width, hight = backgr.size
    
        x = (width - textwidth) // 2
        y = (hight - texthight) // 2
        
        # Draw text and save
        draw.text((x, y), info, fill=(0, 0, 0, 255), font=font)
        composite = Image.alpha_composite(backgr, layer)
        composite = composite.convert('RGB')
        composite.show()
        composite.save("form_output.png")
Label(MyProgram, text="Welcome to my App", bg="white", fg="black", font="Arial 30 bold").place(x=180, y=250)
Button(MyProgram, text="Enter", command=password, font="Arial 15 bold").place(x=350, y=350)

def formParia():
    """Create form for Paria"""
    UserForm(MyProgram, "formParia", "resultParia")

def formShahrad():
    """Create form for Shahrad"""
    UserForm(MyProgram, "formShahrad", "resultShahrad")


MyProgram.mainloop()
