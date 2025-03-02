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
    dice = Toplevel(MyProgram)
    dice.geometry("800x600")
    dice.configure(background="#f4f3d2")
    dice.title("Dice game")

    def click():
        for i in range (4):
            dice1=random.randint(1,6)
            dice2=random.randint(1,6)
            if  dice1==dice2:
                messagebox.showinfo("well done!","Yay, pass!")
                formShahrad()
                dice.destroy()
                audio3()
                break
            elif not dice1==dice2 and i==3:
                 
                 messagebox.showinfo("not passed!","But let's go in!")
                 
                 formShahrad()
                 dice.destroy()
                 audio2()
                 break
            else:
                messagebox.showinfo("Result","dice 1 is : "+str(dice1)+" dice 2 is : "+str(dice2)+" Oh no! "+"Do it again!")
                audio1()

    Label(dice, text="Welcome to the game!!", bg="white", fg="black", font="Arial 30 bold").place(x=180, y=250)
    Button(dice,text="Let's roll it!",command=click,font="Arial 10 bold").place(x=300, y=350)
    Button(dice, text="exit form", command=dice.destroy,font="Arial 10 bold").place(x=400, y=350)

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

def formParia():
    formP = Toplevel(MyProgram)
    formP.geometry("700x700")
    formP.configure(background="#f4f3d2")
    formP.title("Form")

    l=Label(formP, text=" Form ", font="Arial 20 bold").place(x=300, y=10)
    l1=Label(formP, text="Enter your first name: ").place(x=120, y=70)
    l2=Label(formP, text="Enter your last name: ").place(x=120, y=110)
    l3=Label(formP, text="Enter your phone num.: ").place(x=120, y=150)
    l4=Label(formP, text="Preferences", font="Arial 20").place(x=180, y=400)
    l5=Label(formP, text="Gender", font="Arial 20").place(x=180, y=200)
    l6=Label(formP, text="Status", font="Arial 20").place(x=190, y=300)
    global imagecor

    imagecor=PhotoImage(file="test2.png")
    corner=Label(formP,image=imagecor).place(x=450,y=450)
    first_name = StringVar()
    last_name = StringVar()
    phone_num = StringVar()

    e1=Entry(formP, textvariable=first_name).place(x=250, y=70)
    e2=Entry(formP, textvariable=last_name).place(x=250, y=110)
    e3=Entry(formP, textvariable=phone_num).place(x=250, y=150)

    gender = StringVar(value="null")
    marital_status = StringVar(value="null")
    fav = IntVar()
    fav1 = IntVar()
    fav2 = IntVar()
    fav3 = IntVar()

    Radiobutton(formP, text="Male", variable=gender, value="Male").place(x=200, y=230)
    Radiobutton(formP, text="Female", variable=gender, value="Female").place(x=200, y=250)
    Radiobutton(formP, text="Single", variable=marital_status, value="Single").place(x=200, y=330)
    Radiobutton(formP, text="Married", variable=marital_status, value="Married").place(x=200, y=350)
    Checkbutton(formP, text="varzesh", variable=fav).place(x=200, y=430)
    Checkbutton(formP, text="moosighi", variable=fav1).place(x=200, y=450)
    Checkbutton(formP, text="ashpazi", variable=fav2).place(x=200, y=470)
    Checkbutton(formP, text="ketab", variable=fav3).place(x=200, y=490)

    def submit_formP():

        try:
            db3=Paria()
            cursor5 = db3.cursor()
            favorites = []
            if fav.get():
                favorites.append('varzesh')
            if fav1.get():
                favorites.append('moosighi')
            if fav2.get():
                favorites.append('ashpazi')
            if fav3.get():
                favorites.append('ketab')
            
            favorites_str = ', '.join(favorites)
            
            query = "INSERT INTO resultParia (first_name, last_name, phone_num, gender, marital_status, favorites) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name.get(), last_name.get(), phone_num.get(), gender.get(), marital_status.get(), favorites_str)
            cursor5.execute(query, values)
            db3.commit() 
            messagebox.showinfo("Success", "Data inserted successfully")
        except:
            messagebox.showinfo("Error", f"Error occurred: '{str(e)}'")
        finally:
            cursor5.close()
            db3.close()

        info = (
            f"First Name: {first_name.get()}\n"
            f"Last Name: {last_name.get()}\n"
            f"Phone Number: {phone_num.get()}\n"
            f"Gender: {gender.get()}\n"
            f"Marital Status: {marital_status.get()}\n"
            f"Preferences:\n"
            f"  - Varzesh: {'Yes' if fav.get() else 'No'}\n"
            f"  - Moosighi: {'Yes' if fav1.get() else 'No'}\n"
            f"  - Ashpazi: {'Yes' if fav2.get() else 'No'}\n"
            f"  - Ketab: {'Yes' if fav3.get() else 'No'}"
        )
        
        backgr = Image.open("back.png")
        backgr = backgr.convert('RGBA')  
        layer = Image.new('RGBA', backgr.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)
        font = ImageFont.truetype("arial.ttf", 250)
        bbox=draw.textbbox((0,0),info, font=font)
        textwidth=bbox[2]-bbox[0]
        texthight=bbox[3]-bbox[1]
        width , hight= backgr.size
    
        x=(width-textwidth)//2
        y=(hight-texthight)//2
        draw.text((x, y), info, fill=(0, 0, 0, 255), font=font)

        composite = Image.alpha_composite(backgr, layer)
        composite = composite.convert('RGB')
        composite.show()
        composite.save("form_output.png")
    
    Button(formP, text="Submit", command=submit_formP).place(x=250, y=540)
    Button(formP, text="exit form", command=formP.destroy).place(x=300, y=540)

def formShahrad():
    formShahrad = Toplevel(MyProgram)
    formShahrad.geometry("700x700")
    formShahrad.configure(background="#f4f3d2")
    formShahrad.title("Form")

    l=Label(formShahrad, text=" Form ", font="Arial 20 bold").place(x=300, y=10)
    Label(formShahrad, text="Enter your first name: ").place(x=120, y=70)
    Label(formShahrad, text="Enter your last name: ").place(x=120, y=110)
    Label(formShahrad, text="Enter your phone num.: ").place(x=120, y=150)
    Label(formShahrad, text="Preferences", font="Arial 20").place(x=180, y=400)
    Label(formShahrad, text="Gender", font="Arial 20").place(x=180, y=200)
    Label(formShahrad, text="Status", font="Arial 20").place(x=190, y=300)
    global imagecor

    imagecor=PhotoImage(file="test2.png")
    corner=Label(formShahrad,image=imagecor).place(x=450,y=450)
    first_name = StringVar()
    last_name = StringVar()
    phone_num = StringVar()

    Entry(formShahrad, textvariable=first_name).place(x=250, y=70)
    Entry(formShahrad, textvariable=last_name).place(x=250, y=110)
    Entry(formShahrad, textvariable=phone_num).place(x=250, y=150)

    gender = StringVar(value="null")
    marital_status = StringVar(value="null")
    fav = IntVar()
    fav1 = IntVar()
    fav2 = IntVar()
    fav3 = IntVar()

    Radiobutton(formShahrad, text="Male", variable=gender, value="Male").place(x=200, y=230)
    Radiobutton(formShahrad, text="Female", variable=gender, value="Female").place(x=200, y=250)
    Radiobutton(formShahrad, text="Single", variable=marital_status, value="Single").place(x=200, y=330)
    Radiobutton(formShahrad, text="Married", variable=marital_status, value="Married").place(x=200, y=350)
    Checkbutton(formShahrad, text="varzesh", variable=fav).place(x=200, y=430)
    Checkbutton(formShahrad, text="moosighi", variable=fav1).place(x=200, y=450)
    Checkbutton(formShahrad, text="ashpazi", variable=fav2).place(x=200, y=470)
    Checkbutton(formShahrad, text="ketab", variable=fav3).place(x=200, y=490)

    def submit_formS():
        
        try:
            db4=Shahrad()
            cursor4 = db4.cursor()
            favorites = []
            if fav.get():
                favorites.append('varzesh')
            if fav1.get():
                favorites.append('moosighi')
            if fav2.get():
                favorites.append('ashpazi')
            if fav3.get():
                favorites.append('ketab')
            
            favorites_str = ', '.join(favorites)
            
            query = "INSERT INTO resultShahrad (first_name, last_name, phone_num, gender, marital_status, favorites) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (first_name.get(), last_name.get(), phone_num.get(), gender.get(), marital_status.get(), favorites_str)
            cursor4.execute(query, values)
            db4.commit() 
            messagebox.showinfo("Success", "Data inserted successfully")
        except mc.Error as e:
            messagebox.showinfo("Error", f"Error occurred: '{str(e)}'")
        finally:
            cursor4.close()
            db4.close()

        info = (
            f"First Name: {first_name.get()}\n"
            f"Last Name: {last_name.get()}\n"
            f"Phone Number: {phone_num.get()}\n"
            f"Gender: {gender.get()}\n"
            f"Marital Status: {marital_status.get()}\n"
            f"Preferences:\n"
            f"  - Varzesh: {'Yes' if fav.get() else 'No'}\n"
            f"  - Moosighi: {'Yes' if fav1.get() else 'No'}\n"
            f"  - Ashpazi: {'Yes' if fav2.get() else 'No'}\n"
            f"  - Ketab: {'Yes' if fav3.get() else 'No'}"
        )
        
        backgr = Image.open("back.png")
        backgr = backgr.convert('RGBA')  
        layer = Image.new('RGBA', backgr.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)
        font = ImageFont.truetype("arial.ttf", 250)
        bbox=draw.textbbox((0,0),info, font=font)
        textwidth=bbox[2]-bbox[0]
        texthight=bbox[3]-bbox[1]
        width , hight= backgr.size
    
        x=(width-textwidth)//2
        y=(hight-texthight)//2
        draw.text((x, y), info, fill=(0, 0, 0, 255), font=font)

        composite = Image.alpha_composite(backgr, layer)
        composite = composite.convert('RGB')
        composite.show()
        composite.save("form_output.png")
    
    Button(formShahrad, text="Submit", command=submit_formS).place(x=250, y=540)
    Button(formShahrad, text="exit form", command=formShahrad.destroy).place(x=300, y=540)

Label(MyProgram, text="Welcome to my App", bg="white", fg="black", font="Arial 30 bold").place(x=180, y=250)
Button(MyProgram, text="Enter", command=password, font="Arial 15 bold").place(x=350, y=350)

MyProgram.mainloop()
