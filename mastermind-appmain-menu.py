#-------------------- mastermind game -------------------------
#απαραίτητες βιβλιοθήκες 
import tkinter as tk
from random import sample
from itertools import permutations
from random import randint
import os

#δημιουργία αρχικού παραθύρου για το menu του παιχνιδιού
app= tk.Tk()
app.title('Παιχνίδι Mastermind')
app.geometry('1850x781+0+0')
#φωτογραφια backround
ima= os.path.expanduser('~')+'\\Desktop\\ΑΡΧΕΙΟ 27\\MASTERMIND\\wood.gif'

wood= tk.PhotoImage(file=ima)
#ορισμός καμβά αρχικού μενού
can= tk.Canvas(app, width= 2000, height=1100)
can.grid(row=0, column=0)
can.create_image(0, 0,anchor= 'nw', image= wood)
can.create_text(750, 100, text='ΚΑΛΩΣΗΡΘΕΣ ΣΤΟ MASTERMIND', \
              fill= 'white', font= 'Forte 30 ')

#δημιουργία συναρτήσεων

def rules(): #άνοιγμα παραθύρου κανόνων
    global wood
    r= tk.Toplevel()
    r.geometry('1850x781+0+0')
    r.title('ΚΑΝΟΝΕΣ ΠΑΙΧΝΙΔΙΟΥ')
    c1= tk.Canvas(r, width= 2000, height=1000)
    c1.grid(row=0, column=0)
    c1.create_image(0,0,anchor='nw', image=wood)
    c1.create_text(800,400,text='''
                                                 ΚΑΝΟΝΕΣ ΠΑΙΧΝΙΔΙΟΥ

CODEBREAKER
- Σκοπός σου είναι να βρεις τον μυστικό συνδυασμό του υπολογιστή μέσα σε 8 προσπάθειες το πολύ
- Ο συνδυασμός περιέχει 4 χρώματα από μια φορά το καθένα
- Μπορείς να βάλεις δύο ή περισσότερες φορές το ίδιο χρώμα γνωρίζοντας ότι θα εμφανίζονται παραπάνω
  λευκά ή μαύρα κουτιά ανάλογα με το αν εμπεριέχεται το επαναλμβανόμενο χρώμα στον σωστό συνδυασμό 
- Κάνοντας κλικ σε κάθε χρώμα επιλέγεις έναν πιθανό συνδυασμό
- Για να αλλάξεις κάποιο χρώμα κάνεις κλικ στο αντίστοιχο τετράγωνο για να αποχρωματιστεί
  (κάθε φορά που αποχρωματίζει ένα κουτί, ο παίκτης πρέπει να το χρωματίζει αμέσως μετά)
- Όταν είσαι έτοιμος πατάς check για να ελεγχθεί ο συνδυασμός χρωμάτων που επέλεξες
- Ο υπολογιστής θα σου απαντήσει με μία ακολουθία άσπρων ή/και μαύρων κουτιών
- Μαύρο κουτί = ένα από τα χρώματα της μαντεψιάς σου έχει τοποθετηθεί σωστά
- Άσπρο κουτί = ένα από τα χρώματα βρίσκεται στον κώδικα, αλλά σε διαφορετική θέση 



CODEMAKER
-Σκοπός σου είναι ο υπολογιστής να μην μαντέψει τον μυστικό συνδυασμό που επιλέγεις
-Κάνεις κλικ στα 4 χρώματα που θες να έχει ο συνδυασμός σου και έπειτα πατάς: start
-Κάθε φορά που ο υπολογιστής εμφανίζει ένα συνδυασμό, πατάς το μαύρο ή/και το άσπρο κουμπί
 όσες φορές χρειάζεται και όταν τελειώσεις κλικάρεις το κουμπί ΟΚ
-Μαύρο κουτί = ένα από τα χρώματα της μαντεψιάς του έχει τοποθετηθεί σωστά
-Άσπρο κουτί = ένα από τα χρώματα βρίσκεται στον κώδικα, αλλά σε διαφορετική θέση
-Άν θες να αφαιρέσεις άσπρο ή μαύρο κουτί, το πατάς και εξαφανίζεται
''', font='Arial 15', fill='white')
    
#--------------------------------
c=0 #το c συμβολίζει τον αρθμό ενός κουτιού-κουμπιού (πχ για το box11(γραμμή 1 στήλη 1) c=0)
guesslist=[] #η λίστα που θα εμπεριέχει τη μαντεψιά του παίκτη 

#----------συναρτήσεις στο κομμάτι του codebreaker----------
#ορίζω συναρτήσεις αφαίρεσης χρώματος κουτιού
def exit_game(): #καταστρέφει το παράθυρο 
    root.destroy()
def restart_game(): #ανοίγει καινούριο παράθυρο για να παίξει ο παίκτης ως codebreaker
    exit_game()
    play_codebreaker()
def removecolor11():
    global c
    if c<4 :#για να μη γίνονται αλλαγές έπειτα από την επόμενη γραμμή (που το πρώτο κουτί έχει c=5)
        c=0 #ο χρωματισμός κουτιού που έπεται να αφορά το κουτί bbox11
        bbox11.config(bg='#C9824B')
        bbox11['state']='disabled'
        guesslist.remove(guesslist[0]) #αφαιρεί από τη λίστα (guesslist) του παίκτη το στοιχείο που αφορά το χρώμα του bbox11
def removecolor12():
    global c
    if c<5:
        c=1
        bbox12.config(bg='#C9824B')
        bbox12['state']='disabled'
        guesslist.remove(guesslist[1])
def removecolor13():
    global c
    if c<5:
        c=2
        bbox13.config(bg='#C9824B')
        bbox13['state']='disabled'
        guesslist.remove(guesslist[2])
def removecolor14():
    global c
    if c<5:
        c=3
        bbox14.config(bg='#C9824B')
        bbox14['state']='disabled'
        guesslist.remove(guesslist[3])
def removecolor21():
    global c
    if c<9:
        bbox21.config(bg='#C9824B')
        bbox21['state']='disabled'
        c=4
        guesslist.remove(guesslist[0])
def removecolor22():
    global c
    if c<9:
        bbox22.config(bg='#C9824B')
        bbox22['state']='disabled'
        c=5
        guesslist.remove(guesslist[1])
def removecolor23():
    global c
    if c<9:
        bbox23.config(bg='#C9824B')
        bbox23['state']='disabled'
        c=6
        guesslist.remove(guesslist[2])
def removecolor24():
    global c
    if c<9:
        bbox24.config(bg='#C9824B')
        bbox24['state']='disabled'
        c=7
        guesslist.remove(guesslist[3])
def removecolor31():
    global c
    if c<13:
        bbox31.config(bg='#C9824B')
        bbox31['state']='disabled'
        c=8
        guesslist.remove(guesslist[0])
def removecolor32():
    global c
    if c<13:
        bbox32.config(bg='#C9824B')
        bbox32['state']='disabled'
        c=9
        guesslist.remove(guesslist[1])
def removecolor33():
    global c
    if c<13:
        bbox33.config(bg='#C9824B')
        bbox33['state']='disabled'
        c=10
        guesslist.remove(guesslist[2])
def removecolor34():
    global c
    if c<13:
        bbox34.config(bg='#C9824B')
        bbox34['state']='disabled'
        c=11
        guesslist.remove(guesslist[3])
def removecolor41():
    global c
    if c<17:
        bbox41.config(bg='#C9824B')
        bbox41['state']='disabled'
        c=12
        guesslist.remove(guesslist[0])
def removecolor42():
    global c
    if c<17:
        bbox42.config(bg='#C9824B')
        bbox42['state']='disabled'
        c=13
        guesslist.remove(guesslist[1])
def removecolor43():
    global c
    if c<17:
        bbox43.config(bg='#C9824B')
        bbox43['state']='disabled'
        c=14
        guesslist.remove(guesslist[2])
def removecolor44():
    global c
    if c<17:
        bbox44.config(bg='#C9824B')
        bbox44['state']='disabled'
        c=15
        guesslist.remove(guesslist[3])
def removecolor51():
    global c
    if c<21:
        bbox51.config(bg='#C9824B')
        bbox51['state']='disabled'
        c=16
        guesslist.remove(guesslist[0])
def removecolor52():
    global c
    if c<21:
        bbox52.config(bg='#C9824B')
        bbox52['state']='disabled'
        c=17
        guesslist.remove(guesslist[1])
def removecolor53():
    global c
    if c<21:
        bbox53.config(bg='#C9824B')
        bbox53['state']='disabled'
        c=18
        guesslist.remove(guesslist[2])
def removecolor54():
    global c
    if c<21:
        bbox54.config(bg='#C9824B')
        bbox54['state']='disabled'
        c=19
        guesslist.remove(guesslist[3])
def removecolor61():
    global c
    if c<25:
        bbox61.config(bg='#C9824B')
        bbox61['state']='disabled'
        c=20
        guesslist.remove(guesslist[0])
def removecolor62():
    global c
    if c<25:
        bbox62.config(bg='#C9824B')
        bbox62['state']='disabled'
        c=21
        guesslist.remove(guesslist[1])
def removecolor63():
    global c
    if c<25:
        bbox63.config(bg='#C9824B')
        bbox63['state']='disabled'
        c=22
        guesslist.remove(guesslist[2])
def removecolor64():
    global c
    if c<25:
        bbox64.config(bg='#C9824B')
        bbox64['state']='disabled'
        c=23
        guesslist.remove(guesslist[3])
def removecolor71():
    global c
    if c<29:
        bbox71.config(bg='#C9824B')
        bbox71['state']='disabled'
        c=24
        guesslist.remove(guesslist[0])
def removecolor72():
    global c
    if c<29:
        bbox72.config(bg='#C9824B')
        bbox72['state']='disabled'
        c=25
        guesslist.remove(guesslist[1])
def removecolor73():
    global c
    if c<29:
        bbox73.config(bg='#C9824B')
        bbox73['state']='disabled'
        c=26
        guesslist.remove(guesslist[2])
def removecolor74():
    global c
    if c<29:
        bbox74.config(bg='#C9824B')
        bbox74['state']='disabled'
        c=27
        guesslist.remove(guesslist[3])
def removecolor81():
    global c
    if c<33:
        bbox81.config(bg='#C9824B')
        bbox81['state']='disabled'
        c=28
        guesslist.remove(guesslist[0])
def removecolor82():
    global c
    if c<33:
        bbox82.config(bg='#C9824B')
        bbox82['state']='disabled'
        c=29
        guesslist.remove(guesslist[1])
def removecolor83():
    global c
    if c<33:
        bbox83.config(bg='#C9824B')
        bbox83['state']='disabled'
        c=30
        guesslist.remove(guesslist[2])
def removecolor84():
    global c
    if c<33:
        bbox84.config(bg='#C9824B')
        bbox84['state']='disabled'
        c=31
        guesslist.remove(guesslist[3])

def greenit(): #ορίζω command του κουμπιού που χρωματίζει πράσινο το κουτί στο παράθυρο του codebreaker
               #αντίστοιχα και για τα υπόλοιπα χρώματα
    global c
    if c==31:
        bbox84.config(bg='#A6E345')
        bbox84['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==30:
        bbox83.config(bg='#A6E345')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#A6E345')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#A6E345')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#A6E345')
        bbox74['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==26:
        bbox73.config(bg='#A6E345')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#A6E345')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#A6E345')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#A6E345')
        bbox64['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==22:
        bbox63.config(bg='#A6E345')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#A6E345')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#A6E345')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#A6E345')
        bbox54['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==18:
        bbox53.config(bg='#A6E345')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#A6E345')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#A6E345')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#A6E345')
        bbox44['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==14:
        bbox43.config(bg='#A6E345')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#A6E345')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#A6E345')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#A6E345')
        bbox34['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==10:
        bbox33.config(bg='#A6E345')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#A6E345')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#A6E345')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#A6E345')
        bbox24['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==6:
        bbox23.config(bg='#A6E345')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#A6E345')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#A6E345')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#A6E345')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#A6E345')
        bbox14['state']='normal'
        guesslist.insert(3,'#A6E345')
    if c==2:
        bbox13.config(bg='#A6E345')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#A6E345')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#A6E345')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#A6E345')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0: #αναφέρεται στο 1ο κουτί
        bbox11.config(bg='#A6E345')#αλλάζει το χρώμα του από καφέ σε πράσινο
        bbox11['state']='normal'
        c+=1 #προχωράει στο επόμενο κουτί
        guesslist.insert(0,'#A6E345') #εισάγει στη λίστα ως 1ο στοιχείο το αντίστοιχο χρώμα(εδώ πράσινο)
        if bbox12['bg']!='#C9824B': #αν το επόμενο κουτί είναι χρωματισμένο, προχωρά στο επόμενο
            c+=1
            if bbox13['bg']!='#C9824B': #αν το επόμενο κουτί είναι χρωματισμένο, προχωρά στο επόμενο
                c+=1
                if bbox14['bg']!='#C9824B':#αν το επόμενο κουτί είναι χρωματισμένο, προχωρά στο επόμενο
                    c+=1
def redit():
    global c
    if c==31:
        bbox84.config(bg='#D43D40')
        bbox84['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==30:
        bbox83.config(bg='#D43D40')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#D43D40')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#D43D40')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#D43D40')
        bbox74['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==26:
        bbox73.config(bg='#D43D40')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#D43D40')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#D43D40')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#D43D40')
        bbox64['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==22:
        bbox63.config(bg='#D43D40')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#D43D40')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#D43D40')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#D43D40')
        bbox54['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==18:
        bbox53.config(bg='#D43D40')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#D43D40')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#D43D40')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#D43D40')
        bbox44['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==14:
        bbox43.config(bg='#D43D40')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#D43D40')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#D43D40')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#D43D40')
        bbox34['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==10:
        bbox33.config(bg='#D43D40')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#D43D40')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#D43D40')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#D43D40')
        bbox24['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==6:
        bbox23.config(bg='#D43D40')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#D43D40')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#D43D40')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#D43D40')
        bbox14['state']='normal'
        guesslist.insert(3,'#D43D40')
    if c==2:
        bbox13.config(bg='#D43D40')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#D43D40')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#D43D40')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#D43D40')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0:
        bbox11.config(bg='#D43D40')
        bbox11['state']='normal'
        c+=1
        guesslist.insert(0,'#D43D40')
        if bbox12['bg']!='#C9824B':
            c+=1
            if bbox13['bg']!='#C9824B':
                c+=1
                if bbox14['bg']!='#C9824B':
                    c+=1
def blueit():
    global c
    if c==31:
        bbox84.config(bg='#2EEAEB')
        bbox84['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==30:
        bbox83.config(bg='#2EEAEB')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#2EEAEB')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#2EEAEB')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#2EEAEB')
        bbox74['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==26:
        bbox73.config(bg='#2EEAEB')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#2EEAEB')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#2EEAEB')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#2EEAEB')
        bbox64['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==22:
        bbox63.config(bg='#2EEAEB')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#2EEAEB')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#2EEAEB')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#2EEAEB')
        bbox54['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==18:
        bbox53.config(bg='#2EEAEB')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#2EEAEB')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#2EEAEB')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#2EEAEB')
        bbox44['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==14:
        bbox43.config(bg='#2EEAEB')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#2EEAEB')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#2EEAEB')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#2EEAEB')
        bbox34['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==10:
        bbox33.config(bg='#2EEAEB')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#2EEAEB')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#2EEAEB')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#2EEAEB')
        bbox24['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==6:
        bbox23.config(bg='#2EEAEB')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#2EEAEB')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#2EEAEB')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#2EEAEB')
        bbox14['state']='normal'
        guesslist.insert(3,'#2EEAEB')
    if c==2:
        bbox13.config(bg='#2EEAEB')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#2EEAEB')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#2EEAEB')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#2EEAEB')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0:
        bbox11.config(bg='#2EEAEB')
        bbox11['state']='normal'
        c+=1
        guesslist.insert(0,'#2EEAEB')
        if bbox12['bg']!='#C9824B':
            c+=1
            if bbox13['bg']!='#C9824B':
                c+=1
                if bbox14['bg']!='#C9824B':
                    c+=1
#FFFC47
def yellowit():
    global c
    if c==31:
        bbox84.config(bg='#FFFC47')
        bbox84['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==30:
        bbox83.config(bg='#FFFC47')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#FFFC47')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#FFFC47')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#FFFC47')
        bbox74['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==26:
        bbox73.config(bg='#FFFC47')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#FFFC47')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#FFFC47')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#FFFC47')
        bbox64['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==22:
        bbox63.config(bg='#FFFC47')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#FFFC47')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#FFFC47')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#FFFC47')
        bbox54['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==18:
        bbox53.config(bg='#FFFC47')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#FFFC47')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#FFFC47')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#FFFC47')
        bbox44['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==14:
        bbox43.config(bg='#FFFC47')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#FFFC47')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#FFFC47')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#FFFC47')
        bbox34['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==10:
        bbox33.config(bg='#FFFC47')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#FFFC47')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#FFFC47')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#FFFC47')
        bbox24['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==6:
        bbox23.config(bg='#FFFC47')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#FFFC47')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#FFFC47')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#FFFC47')
        bbox14['state']='normal'
        guesslist.insert(3,'#FFFC47')
    if c==2:
        bbox13.config(bg='#FFFC47')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#FFFC47')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#FFFC47')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#FFFC47')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0:
        bbox11.config(bg='#FFFC47')
        bbox11['state']='normal'
        c+=1
        guesslist.insert(0,'#FFFC47')
        if bbox12['bg']!='#C9824B':
            c+=1
            if bbox13['bg']!='#C9824B':
                c+=1
                if bbox14['bg']!='#C9824B':
                    c+=1
#FA8EDC
def pinkit():
    global c
    if c==31:
        bbox84.config(bg='#FA8EDC')
        bbox84['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==30:
        bbox83.config(bg='#FA8EDC')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#FA8EDC')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#FA8EDC')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#FA8EDC')
        bbox74['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==26:
        bbox73.config(bg='#FA8EDC')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#FA8EDC')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#FA8EDC')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#FA8EDC')
        bbox64['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==22:
        bbox63.config(bg='#FA8EDC')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#FA8EDC')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#FA8EDC')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#FA8EDC')
        bbox54['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==18:
        bbox53.config(bg='#FA8EDC')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#FA8EDC')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#FA8EDC')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#FA8EDC')
        bbox44['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==14:
        bbox43.config(bg='#FA8EDC')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#FA8EDC')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#FA8EDC')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#FA8EDC')
        bbox34['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==10:
        bbox33.config(bg='#FA8EDC')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#FA8EDC')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#FA8EDC')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#FA8EDC')
        bbox24['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==6:
        bbox23.config(bg='#FA8EDC')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#FA8EDC')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#FA8EDC')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#FA8EDC')
        bbox14['state']='normal'
        guesslist.insert(3,'#FA8EDC')
    if c==2:
        bbox13.config(bg='#FA8EDC')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#FA8EDC')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#FA8EDC')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#FA8EDC')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0:
        bbox11.config(bg='#FA8EDC')
        bbox11['state']='normal'
        c+=1
        guesslist.insert(0,'#FA8EDC')
        if bbox12['bg']!='#C9824B':
            c+=1
            if bbox13['bg']!='#C9824B':
                c+=1
                if bbox14['bg']!='#C9824B':
                    c+=1
#9D2AA6    
def purpleit():
    global c
    if c==31:
        bbox84.config(bg='#9D2AA6')
        bbox84['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==30:
        bbox83.config(bg='#9D2AA6')
        bbox83['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox84['bg']!='#C9824B':
            c+=1
    if c==29:
        bbox82.config(bg='#9D2AA6')
        bbox82['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox83['bg']!='#C9824B':
            c+=1
            if bbox84['bg']!='#C9824B':
                c+=1
    if c==28:
        bbox81.config(bg='#9D2AA6')
        bbox81['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox82['bg']!='#C9824B':
            c+=1
            if bbox83['bg']!='#C9824B':
                c+=1
                if bbox84['bg']!='#C9824B':
                    c+=1
    if c==27:
        bbox74.config(bg='#9D2AA6')
        bbox74['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==26:
        bbox73.config(bg='#9D2AA6')
        bbox73['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox74['bg']!='#C9824B':
            c+=1
    if c==25:
        bbox72.config(bg='#9D2AA6')
        bbox72['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox73['bg']!='#C9824B':
            c+=1
            if bbox74['bg']!='#C9824B':
                c+=1
    if c==24:
        bbox71.config(bg='#9D2AA6')
        bbox71['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox72['bg']!='#C9824B':
            c+=1
            if bbox73['bg']!='#C9824B':
                c+=1
                if bbox74['bg']!='#C9824B':
                    c+=1
    if c==23:
        bbox64.config(bg='#9D2AA6')
        bbox64['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==22:
        bbox63.config(bg='#9D2AA6')
        bbox63['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox64['bg']!='#C9824B':
            c+=1
    if c==21:
        bbox62.config(bg='#9D2AA6')
        bbox62['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox63['bg']!='#C9824B':
            c+=1
            if bbox64['bg']!='#C9824B':
                c+=1
    if c==20:
        bbox61.config(bg='#9D2AA6')
        bbox61['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox62['bg']!='#C9824B':
            c+=1
            if bbox63['bg']!='#C9824B':
                c+=1
                if bbox64['bg']!='#C9824B':
                    c+=1
    if c==19:
        bbox54.config(bg='#9D2AA6')
        bbox54['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==18:
        bbox53.config(bg='#9D2AA6')
        bbox53['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox54['bg']!='#C9824B':
            c+=1
    if c==17:
        bbox52.config(bg='#9D2AA6')
        bbox52['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox53['bg']!='#C9824B':
            c+=1
            if bbox54['bg']!='#C9824B':
                c+=1
    if c==16:
        bbox51.config(bg='#9D2AA6')
        bbox51['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox52['bg']!='#C9824B':
            c+=1
            if bbox53['bg']!='#C9824B':
                c+=1
                if bbox54['bg']!='#C9824B':
                    c+=1
    if c==15:
        bbox44.config(bg='#9D2AA6')
        bbox44['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==14:
        bbox43.config(bg='#9D2AA6')
        bbox43['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox44['bg']!='#C9824B':
            c+=1
    if c==13:
        bbox42.config(bg='#9D2AA6')
        bbox42['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox43['bg']!='#C9824B':
            c+=1
            if bbox44['bg']!='#C9824B':
                c+=1
    if c==12:
        bbox41.config(bg='#9D2AA6')
        bbox41['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox42['bg']!='#C9824B':
            c+=1
            if bbox43['bg']!='#C9824B':
                c+=1
                if bbox44['bg']!='#C9824B':
                    c+=1
    if c==11:
        bbox34.config(bg='#9D2AA6')
        bbox34['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==10:
        bbox33.config(bg='#9D2AA6')
        bbox33['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox34['bg']!='#C9824B':
            c+=1
    if c==9:
        bbox32.config(bg='#9D2AA6')
        bbox32['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox33['bg']!='#C9824B':
            c+=1
            if bbox34['bg']!='#C9824B':
                c+=1
    if c==8:
        bbox31.config(bg='#9D2AA6')
        bbox31['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox32['bg']!='#C9824B':
            c+=1
            if bbox33['bg']!='#C9824B':
                c+=1
                if bbox34['bg']!='#C9824B':
                    c+=1
    if c==7:
        bbox24.config(bg='#9D2AA6')
        bbox24['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==6:
        bbox23.config(bg='#9D2AA6')
        bbox23['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox24['bg']!='#C9824B':
            c+=1
    if c==5:
        bbox22.config(bg='#9D2AA6')
        bbox22['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox23['bg']!='#C9824B':
            c+=1
            if bbox24['bg']!='#C9824B':
                c+=1
    if c==4:
        bbox21.config(bg='#9D2AA6')
        bbox21['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox22['bg']!='#C9824B':
            c+=1
            if bbox23['bg']!='#C9824B':
                c+=1
                if bbox24['bg']!='#C9824B':
                    c+=1
    if c==3:
        bbox14.config(bg='#9D2AA6')
        bbox14['state']='normal'
        guesslist.insert(3,'#9D2AA6')
    if c==2:
        bbox13.config(bg='#9D2AA6')
        bbox13['state']='normal'
        c+=1
        guesslist.insert(2,'#9D2AA6')
        if bbox14['bg']!='#C9824B':
            c+=1
    if c==1:
        bbox12.config(bg='#9D2AA6')
        bbox12['state']='normal'
        c+=1
        guesslist.insert(1,'#9D2AA6')
        if bbox13['bg']!='#C9824B':
            c+=1
            if bbox14['bg']!='#C9824B':
                c+=1
    if c==0:
        bbox11.config(bg='#9D2AA6')
        bbox11['state']='normal'
        c+=1
        guesslist.insert(0,'#9D2AA6')
        if bbox12['bg']!='#C9824B':
            c+=1
            if bbox13['bg']!='#C9824B':
                c+=1
                if bbox14['bg']!='#C9824B':
                    c+=1
            

#ορίζω command των checkbutton ώστε να εμφανίζουν μαύρα κουτιά (σωστή απάντηση σε σωστή θέση)
#και λευκά κουτιά (σωστή απάντηση σε λάθος θέση)
def checkrow1():
    global c
    global guesslist
    if bbox11['bg']=='#C9824B' or bbox12['bg']=='#C9824B' or bbox13['bg']=='#C9824B' or bbox14['bg']=='#C9824B':
        messagebox=tk.Toplevel()#αν πατήσει check χωρίς να έχουν όλα τα κουτιά χρώμα, εμφανίζει παράθυρο με μήνυμα
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:    
        rightanswers=0 #ορίζω μια μεταβλητή που θα δείχνει πόσα μαύρα κουτιά να εμφανίζονται
        difposanswers=0 #ορίζω μια μεταβλητή που θα δείχνει πόσα λευκά κουτιά να εμφανίζονται
        checkbuttonrow1.destroy()#καταστρέφεται το κουμπί check στην αντίστοιχη σειρά αφού πατηθεί
        checkbuttonrow2['state']=['normal']#ενεργοποιείται το check της επόμενης σειράς 
        bbox11['state']=['disabled']
        bbox12['state']=['disabled']
        bbox13['state']=['disabled']
        bbox14['state']=['disabled']
        for i in range(0,4): #έλεγχος για σωστά χρώματα στη σωστή θέση
            if code[i]==guesslist[i]:
                rightanswers+=1
        for s in range(0,rightanswers): #εμφάνιση μαύρων ενδείξεων για τη σωστά στη σωστή θέση
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=10,column=7+s,padx=1,pady=1)
        for a in range(0,4): #έλεγχος για σωστά χρώματα στη λάθος θέση (υμπεριλαμβάνονται και τα σωστά χρώματα
                             #στη σωστή θέση, που έπειτα αφαιρούνται)
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for m in range(0,difposanswers-rightanswers): #εμφάνιση λευκών ενδείξεων για τη σωστά στη λάθος θέση
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=10,column=12+m,padx=1,pady=1)
        guesslist=[] #αδειάζει τη λίστα guesslist  οποία θα ξαναγεμίσει με τα επόμενα χρώματα της επόμενης γραμμής
        c=4 #πρέπει το τέλος να μετακινείται στο κουτί bbox21 (πχ αν πάτησε διόρθωση χρώματος σε κάποιο ενδιάμεσο κουτί)
        if rightanswers==4: #ο παίκτης έχει βρει τον κώδικα 
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345') #εμφάνιση label που ενημερώνει τον παίκτη πως νίκησε
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled' #απενεργοποίηση κουμπιών ώστε να μην παίξει ο παίκτης ξανά
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow2['state']='disabled'
            checkbuttonrow3['state']='disabled'
            checkbuttonrow4['state']='disabled'
            checkbuttonrow5['state']='disabled'
            checkbuttonrow6['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow2():
    global guesslist
    global c
    if bbox21['bg']=='#C9824B' or bbox22['bg']=='#C9824B' or bbox23['bg']=='#C9824B' or bbox24['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow2.destroy()
        checkbuttonrow3['state']=['normal']
        bbox21['state']=['disabled']
        bbox22['state']=['disabled']
        bbox23['state']=['disabled']
        bbox24['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=9,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=9,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=8
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow3['state']='disabled'
            checkbuttonrow4['state']='disabled'
            checkbuttonrow5['state']='disabled'
            checkbuttonrow6['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow3():
    global guesslist
    global c
    if bbox31['bg']=='#C9824B' or bbox32['bg']=='#C9824B' or bbox33['bg']=='#C9824B' or bbox34['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow3.destroy()
        checkbuttonrow4['state']=['normal']
        bbox31['state']=['disabled']
        bbox32['state']=['disabled']
        bbox33['state']=['disabled']
        bbox34['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=8,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=8,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=12
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow4['state']='disabled'
            checkbuttonrow5['state']='disabled'
            checkbuttonrow6['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow4():
    global guesslist
    global c
    if bbox41['bg']=='#C9824B' or bbox42['bg']=='#C9824B' or bbox43['bg']=='#C9824B' or bbox44['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:    
        rightanswers=0
        difposanswers=0
        checkbuttonrow4.destroy()
        checkbuttonrow5['state']=['normal']
        bbox41['state']=['disabled']
        bbox42['state']=['disabled']
        bbox43['state']=['disabled']
        bbox44['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=7,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=7,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=16
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow5['state']='disabled'
            checkbuttonrow6['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow5():
    global guesslist
    global c
    if bbox51['bg']=='#C9824B' or bbox52['bg']=='#C9824B' or bbox53['bg']=='#C9824B' or bbox54['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow5.destroy()
        checkbuttonrow6['state']=['normal']
        bbox51['state']=['disabled']
        bbox52['state']=['disabled']
        bbox53['state']=['disabled']
        bbox54['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=6,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=6,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=20
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow6['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow6():
    global guesslist
    global c
    if bbox61['bg']=='#C9824B' or bbox62['bg']=='#C9824B' or bbox63['bg']=='#C9824B' or bbox64['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow6.destroy()
        checkbuttonrow7['state']=['normal']
        bbox61['state']=['disabled']
        bbox62['state']=['disabled']
        bbox63['state']=['disabled']
        bbox64['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=5,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=5,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=24
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow7['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow7():
    global guesslist
    global c
    if bbox71['bg']=='#C9824B' or bbox72['bg']=='#C9824B' or bbox73['bg']=='#C9824B' or bbox74['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow7.destroy()
        checkbuttonrow8['state']=['normal']
        bbox71['state']=['disabled']
        bbox72['state']=['disabled']
        bbox73['state']=['disabled']
        bbox74['state']=['disabled']
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=4,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=4,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=28
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345')
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
            checkbuttonrow8['state']='disabled'
def checkrow8():
    global c
    global guesslist
    if bbox81['bg']=='#C9824B' or bbox82['bg']=='#C9824B' or bbox83['bg']=='#C9824B' or bbox84['bg']=='#C9824B':
        messagebox=tk.Toplevel()
        forgotbutton=tk.Label(messagebox,bg='red',text='Ξέχασες να βάλεις κάποιο χρώμα',font='Arial 20')
        forgotbutton.grid(column=0,row=0,padx=5,pady=5)
    else:
        rightanswers=0
        difposanswers=0
        checkbuttonrow8.destroy()
        for i in range(0,4):
            if code[i]==guesslist[i]:
                rightanswers+=1
        for a in range(0,4):
            for b in range(0,4):
                if code[b]==guesslist[a]:
                    difposanswers+=1
        for s in range(0,rightanswers):
            rightanswer=tk.Label(root,bg='black')
            rightanswer.grid(row=3,column=7+s,padx=1,pady=1)
        for m in range(0,difposanswers-rightanswers):
            difposanswer=tk.Label(root,bg='white')
            difposanswer.grid(row=3,column=12+m,padx=1,pady=1)
        guesslist=[]
        c=32
        bbox81['state']=['disabled']
        bbox82['state']=['disabled']
        bbox83['state']=['disabled']
        bbox84['state']=['disabled']
        if rightanswers==4:
            win=tk.Label(root,text='Κέρδισες!!',bg='#A6E345', padx=30, pady=10)
            win.grid(row=0,column=0,padx=45,pady=45)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'
        if rightanswers!=4: #αν δεν έχει βρει το σωστό συνδυασμό έπειτα από 8 προσπάθειες τότε εμφανίζει gameover
            gameover=tk.Label(root,text='game over',bg='red', padx=30, pady=10)
            gameover.grid(row=0,column=0,padx=20,pady=20)
            right1.grid(row=2,column=2)#εμφανίζεται ο σωστός συνδυασμός
            right2.grid(row=2,column=3)
            right3.grid(row=2,column=4)
            right4.grid(row=2,column=5)
            bgreenbutton['state']='disabled'
            bredbutton['state']='disabled'
            byellowbutton['state']='disabled'
            bbluebutton['state']='disabled'
            bpinkbutton['state']='disabled'
            bpurplebutton['state']='disabled'





#------------------------------------------   
def play_codebreaker():
    global c,guesslist,root,code,colors,right1,right2,right3,right4,bbox11,bbox12,bbox13,bbox14,bbox21,bbox22,bbox23,bbox24,bbox31,bbox32,bbox33,bbox34,bbox41,bbox42,bbox43,bbox44,bbox51,bbox52,bbox53,bbox54,bbox61,bbox62,bbox63,bbox64,bbox71,bbox72,bbox73,bbox74,bbox81,bbox82,bbox83,bbox84,\
           checkbuttonrow1,checkbuttonrow2,checkbuttonrow3,checkbuttonrow4,checkbuttonrow5,checkbuttonrow6,checkbuttonrow7,checkbuttonrow8,\
           bgreenbutton,bredbutton,byellowbutton,bpinkbutton,bpurplebutton,bbluebutton
#------------------codebreaker code--------------------#
    c=0 #το c συμβολίζει τον αρθμό ενός κουτιού-κουμπιού (πχ για το bbox11(γραμμή 1 στήλη 1) c=0)
    root=tk.Toplevel() #ορίζουμε το παράθυρο του codebreaker 
    root.geometry('1850x781')
    root.title('Codebreaker')

    mainbg=tk.PhotoImage(file=ima)
    mylabel=tk.Label(root,image=mainbg)
    mylabel.place(x=0,y=0)

    colors=['#A6E345','#D43D40','#2EEAEB','#FFFC47','#FA8EDC','#9D2AA6'] #η λίστα των χρωμάτων που μπορεί να επιλέξει ο παίκτης
    code= sample(colors, k=4) #η λίστα που περιέχει τον σωστό συνδυασμό χρωμάτων (4 τυχαία χρώματα διαφορετικά μεταξύ τους)
    guesslist=[] #η λίστα που θα περιλαμβάνει κάθε φορά τον συνδυασμό που μαντεύει ο παίκτης
    #τα label με τον σωστό συνδυασμό που εμφανίζονται όταν χάνει ο παίκτης
    right1=tk.Label(root,bg=code[0],padx=9,pady=3)
    right2=tk.Label(root,bg=code[1],padx=9,pady=3)
    right3=tk.Label(root,bg=code[2],padx=9,pady=3)
    right4=tk.Label(root,bg=code[3],padx=9,pady=3)
     
    number1=tk.Label(root,text='1',bg='#C9824B') #δείχνει την προσπάθεια στην οποία είναι ο παίκτης
    number2=tk.Label(root,text='2',bg='#C9824B')
    number3=tk.Label(root,text='3',bg='#C9824B')
    number4=tk.Label(root,text='4',bg='#C9824B')
    number5=tk.Label(root,text='5',bg='#C9824B')
    number6=tk.Label(root,text='6',bg='#C9824B')
    number7=tk.Label(root,text='7',bg='#C9824B')
    number8=tk.Label(root,text='8',bg='#C9824B')
                     
    number1.grid(column=0,row=10,padx=(600,3))
    number2.grid(column=0,row=9,padx=(600,3))
    number3.grid(column=0,row=8,padx=(600,3))
    number4.grid(column=0,row=7,padx=(600,3))
    number5.grid(column=0,row=6,padx=(600,3))
    number6.grid(column=0,row=5,padx=(600,3))
    number7.grid(column=0,row=4,padx=(600,3))
    number8.grid(column=0,row=3,padx=(600,3))
    
    titlecb=tk.Label(root,text='Codebreaker',bg='#C9824B',font='Arial 15')
    titlecb.grid(column=1,row=0,columnspan=6,pady=100)
    
    # ορίζω τα κουτιά-κουμπιά για τον codebreaker(για κάθε κουτί bboxab το a συμβολίζει τη γραμμή
    # του κουτιού ξεκινώντας από κάτω και το b συμβολίζει τη στήλη του κουτιού
    bbox11=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor11, state='disabled')
    bbox12=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor12, state='disabled')
    bbox13=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor13, state='disabled')
    bbox14=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor14, state='disabled')

    bbox11.grid(column=2,row=10,padx=10,pady=2)
    bbox12.grid(column=3,row=10,padx=10,pady=2)
    bbox13.grid(column=4,row=10,padx=10,pady=2)
    bbox14.grid(column=5,row=10,padx=10,pady=2)

    bbox21=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor21, state='disabled')
    bbox22=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor22, state='disabled')
    bbox23=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor23, state='disabled')
    bbox24=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor24, state='disabled')

    bbox21.grid(column=2,row=9,padx=10,pady=2)
    bbox22.grid(column=3,row=9,padx=10,pady=2)
    bbox23.grid(column=4,row=9,padx=10,pady=2)
    bbox24.grid(column=5,row=9,padx=10,pady=2)

    bbox31=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor31, state='disabled')
    bbox32=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor32, state='disabled')
    bbox33=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor33, state='disabled')
    bbox34=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor34, state='disabled')

    bbox31.grid(column=2,row=8,padx=10,pady=2)
    bbox32.grid(column=3,row=8,padx=10,pady=2)
    bbox33.grid(column=4,row=8,padx=10,pady=2)
    bbox34.grid(column=5,row=8,padx=10,pady=2)

    bbox41=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor41, state='disabled')
    bbox42=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor42, state='disabled')
    bbox43=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor43, state='disabled')
    bbox44=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor44, state='disabled')

    bbox41.grid(column=2,row=7,padx=10,pady=2)
    bbox42.grid(column=3,row=7,padx=10,pady=2)
    bbox43.grid(column=4,row=7,padx=10,pady=2)
    bbox44.grid(column=5,row=7,padx=10,pady=2)

    bbox51=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor51, state='disabled')
    bbox52=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor52, state='disabled')
    bbox53=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor53, state='disabled')
    bbox54=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor54, state='disabled')

    bbox51.grid(column=2,row=6,padx=10,pady=2)
    bbox52.grid(column=3,row=6,padx=10,pady=2)
    bbox53.grid(column=4,row=6,padx=10,pady=2)
    bbox54.grid(column=5,row=6,padx=10,pady=2)

    bbox61=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor61, state='disabled')
    bbox62=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor62, state='disabled')
    bbox63=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor63, state='disabled')
    bbox64=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor64, state='disabled')

    bbox61.grid(column=2,row=5,padx=10,pady=2)
    bbox62.grid(column=3,row=5,padx=10,pady=2)
    bbox63.grid(column=4,row=5,padx=10,pady=2)
    bbox64.grid(column=5,row=5,padx=10,pady=2)

    bbox71=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor71, state='disabled')
    bbox72=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor72, state='disabled')
    bbox73=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor73, state='disabled')
    bbox74=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor74, state='disabled')

    bbox71.grid(column=2,row=4,padx=10,pady=2)
    bbox72.grid(column=3,row=4,padx=10,pady=2)
    bbox73.grid(column=4,row=4,padx=10,pady=2)
    bbox74.grid(column=5,row=4,padx=10,pady=2)

    bbox81=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor81, state='disabled')
    bbox82=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor82, state='disabled')
    bbox83=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor83, state='disabled')
    bbox84=tk.Button(root,bg='#C9824B',padx=9,pady=3,command=removecolor84, state='disabled')

    bbox81.grid(column=2,row=3,padx=10,pady=2)
    bbox82.grid(column=3,row=3,padx=10,pady=2)
    bbox83.grid(column=4,row=3,padx=10,pady=2)
    bbox84.grid(column=5,row=3,padx=10,pady=2)
    #ορίζω τα κουμπιά χρωματισμού των κουτιών για των codebreaker
    bgreenbutton=tk.Button(root,bg='#A6E345',padx=3,pady=1,command=greenit)
    bredbutton=tk.Button(root,bg='#D43D40',padx=3,pady=1,command=redit)
    bbluebutton=tk.Button(root,bg='#2EEAEB',padx=3,pady=1,command=blueit)
    byellowbutton=tk.Button(root,bg='#FFFC47',padx=3,pady=1,command=yellowit)
    bpinkbutton=tk.Button(root,bg='#FA8EDC',padx=3,pady=1,command=pinkit)
    bpurplebutton=tk.Button(root,bg='#9D2AA6',padx=3,pady=1,command=purpleit)

    bgreenbutton.grid(row=3,column=20,padx=10)
    bredbutton.grid(row=4,column=20,padx=10)
    bbluebutton.grid(row=5,column=20,padx=10)
    byellowbutton.grid(row=6,column=20,padx=10)
    bpinkbutton.grid(row=7,column=20,padx=10)
    bpurplebutton.grid(row=8,column=20,padx=10)

    #ορίζω τα checkbuttons που ελέγχουν κάθε προσπάθεια του παίκτη        
    checkbuttonrow1=tk.Button(root,bg='grey',text='Check',command=checkrow1)
    checkbuttonrow2=tk.Button(root,bg='grey',text='Check',command=checkrow2, state='disabled')
    checkbuttonrow3=tk.Button(root,bg='grey',text='Check',command=checkrow3, state='disabled')
    checkbuttonrow4=tk.Button(root,bg='grey',text='Check',command=checkrow4, state='disabled')
    checkbuttonrow5=tk.Button(root,bg='grey',text='Check',command=checkrow5, state='disabled')
    checkbuttonrow6=tk.Button(root,bg='grey',text='Check',command=checkrow6, state='disabled')
    checkbuttonrow7=tk.Button(root,bg='grey',text='Check',command=checkrow7, state='disabled')
    checkbuttonrow8=tk.Button(root,bg='grey',text='Check',command=checkrow8, state='disabled')

    checkbuttonrow1.grid(row=10,column=6)
    checkbuttonrow2.grid(row=9,column=6)
    checkbuttonrow3.grid(row=8,column=6)
    checkbuttonrow4.grid(row=7,column=6)
    checkbuttonrow5.grid(row=6,column=6)
    checkbuttonrow6.grid(row=5,column=6)
    checkbuttonrow7.grid(row=4,column=6)
    checkbuttonrow8.grid(row=3,column=6)
    #ορίζω κουμπί που επιστρέφει τον παίκτη στο αρχικό μενού
    exitbutton=tk.Button(root,text='Exit',fg='white',bg='red',font='Arial 8',command=exit_game,padx=10)
    exitbutton.grid(row=13,column=6)
    #ορίζω κουμπί που ανοίγει νέο παράθυρο codebreaker
    restartbutton=tk.Button(root,text='Restart',fg='white',bg='green',font='Arial 8',command=restart_game,)
    restartbutton.grid(row=12,column=6)
    root.mainloop()
#---------------------------
def mexit_game(): #καταστρέφει τα παράθυρα του codemaker 
    global messagebox2
    wind.destroy()
    wind2.destroy()
    try:
        messagebox2.destroy()
    except: NameError
def mrestart_game(): #ανοίγει καινούριο παράθυρο για να παίξει ο παίκτης ως codemaker
    mexit_game()
    play_codemaker()
def mgreenit(): #χρωματίζει τα κουτιά του συνδυασμού που επιλέγει ο παίκτης
    global c, code
    if c==3:
        code4['bg']=['#A6E345']
        greenbutton.destroy() #καταστρέφει τα χρώματα που απομένουν 
        redbutton.destroy()
        bluebutton.destroy()
        pinkbutton.destroy()
        purplebutton.destroy()
        yellowbutton.destroy()
        startbutton['state']='normal' #ενεργοποιεί το start που ξεκινά το παιχνίδι 
    if c==2:
        code3['bg']=['#A6E345']
        greenbutton.destroy() #καταστρέφει το κουμπί χρωματισμού ώστε να μη βάλει ο παίκτης
                              #δυο φορές το ίδιο χρώμα
        c+=1
    if c==1:
        code2['bg']=['#A6E345']
        greenbutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#A6E345']
        greenbutton.destroy()
        c+=1
    
    

def mredit():
    global c, code
    if c==3:
        code4['bg']=['#D43D40']
        redbutton.destroy()
        greenbutton.destroy()
        bluebutton.destroy()
        pinkbutton.destroy()
        purplebutton.destroy()
        yellowbutton.destroy()
        startbutton['state']='normal'
    if c==2:
        code3['bg']=['#D43D40']
        redbutton.destroy()
        c+=1
    if c==1:
        code2['bg']=['#D43D40']
        redbutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#D43D40']
        redbutton.destroy()
        c+=1
    

def mblueit():
    global c, code
    if c==3:
        code4['bg']=['#2EEAEB']
        bluebutton.destroy()
        greenbutton.destroy()
        redbutton.destroy()
        pinkbutton.destroy()
        purplebutton.destroy()
        yellowbutton.destroy()
        startbutton['state']='normal'
    if c==2:
        code3['bg']=['#2EEAEB']
        bluebutton.destroy()
        c+=1
    if c==1:
        code2['bg']=['#2EEAEB']
        bluebutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#2EEAEB']
        bluebutton.destroy()
        c+=1


def myellowit():
    global c, code
    if c==3:
        code4['bg']=['#FFFC47']
        yellowbutton.destroy()
        greenbutton.destroy()
        redbutton.destroy()
        bluebutton.destroy()
        pinkbutton.destroy()
        purplebutton.destroy()
        startbutton['state']='normal'
    if c==2:
        code3['bg']=['#FFFC47']
        yellowbutton.destroy()
        c+=1
    if c==1:
        code2['bg']=['#FFFC47']
        yellowbutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#FFFC47']
        yellowbutton.destroy()
        c+=1

def mpinkit():
    global c, code
    if c==3:
        code4['bg']=['#FA8EDC']
        pinkbutton.destroy()
        greenbutton.destroy()
        redbutton.destroy()
        bluebutton.destroy()
        purplebutton.destroy()
        yellowbutton.destroy()
        startbutton['state']='normal' 
    if c==2:
        code3['bg']=['#FA8EDC']
        pinkbutton.destroy()
        c+=1
    if c==1:
        code2['bg']=['#FA8EDC']
        pinkbutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#FA8EDC']
        pinkbutton.destroy()
        c+=1

def mpurpleit():
    global c, code
    if c==3:
        code4['bg']=['#9D2AA6']
        purplebutton.destroy()
        greenbutton.destroy()
        redbutton.destroy()
        bluebutton.destroy()
        pinkbutton.destroy()
        yellowbutton.destroy()
        startbutton['state']='normal'
    if c==2:
        code3['bg']=['#9D2AA6']
        purplebutton.destroy()
        c+=1
    if c==1:
        code2['bg']=['#9D2AA6']
        purplebutton.destroy()
        c+=1
    if c==0:
        code1['bg']=['#9D2AA6']
        purplebutton.destroy()
        c+=1


def black(): #καταστρέφει τη μαύρη ένδειξη σε περίπτωση λάθους 
    global b,co
    blackresponse.destroy()
    b-=1
    co-=1
def white(): #καταστρέφει τη λευκή ένδειξη σε περίπτωση λάθους
    global w,co
    whiteresponse.destroy()
    w-=1
    co-=1

def putblack(): #εμφανίζει μαύρη ένδειξη για σωστό σε σωστή θέση
    global b,i,co,blackresponse
    if b+w<4: #το σύνολο των ενδείξεων πρέπει να είναι μέχρι 4
        co+=1
        b+=1 
        blackresponse=tk.Button(wind,bg='black',command=black)
        blackresponse.grid(row=i,column=co,padx=5)
    
def putwhite(): #εμφανίζει λευκή ένδειξη για σωστό σε λάθος θέση
    global w,i,co,whiteresponse
    if b+w<4:
        w+=1
        co+=1
        whiteresponse=tk.Button(wind,bg='white',command=white)
        whiteresponse.grid(row=i,column=co,padx=5)
    

def ok1():
    global b,w,i,guess1,guess2,possible1,co,messagebox2
    okbutton1.destroy() 
    okbutton2['state']='normal'
    possible1=[] #λίστα που θα περιέχει τους πιθανούς συνδυασμούς που θα απομείνουν μετά την πρώτη προσπάθεια
    for item in possible: #έλεγχος κάθε πιθανού συνδυασμού(σύγκριση της μαντεψιάς με κάθε συνδυασμό)
        itemb=0 #θα δείχνει πόσα σωστά είναι σε σωστή θέση
        itemw=0 #θα δείχνει πόσα σωστά είναι σε λάθος θέση
        for t in range(0,4): 
            if item[t]==guess1[t]:
                itemb+=1
        for a in range(0,4):
            if item[0]==guess1[a]:
                itemw+=1
            if item[1]==guess1[a]:
                itemw+=1
            if item[2]==guess1[a]:
                itemw+=1
            if item[3]==guess1[a]:
                itemw+=1
        itemw-=itemb #διαφορά των itemw και itemb που αντιπροσωπεύει τα σωστά σε λάθος θέση
        if itemb==b and itemw==w: #κάθε συνδυασμός που ικανοποιεί την πληροφορία του παίκτη εισάγεται στην possible1 αλλιώς απορρίπτεται
            possible1.append(item)
    if b==4: #ο υπολογιστής βρήκε τον συνδυασμό του παίκτη
        winlabel=tk.Label(wind, bg='red', text='Ο υπολογιστής κέρδισε :(')
        winlabel.grid(row=0, column=0)
        okbutton2.destroy() #καταστρέφονται όλα τα υπόλοιπα okbuttons 
        okbutton3.destroy()
        okbutton4.destroy()
        okbutton5.destroy()
        blackbutton['state']='disabled' #απενεργοποίηση για να μην πατηθούν
        whitebutton['state']='disabled'
    else:
        i-=1 #πηγαίνει στην επόμενη σειρά
        co=7 #ξεκινά από την αρχική στήλη 
        b,w=0,0 #οι μεταβλητές b,w μηδενίζονται για την επόμενη μαντεψιά του υπολογιστή
        if len(possible1)!=0: #αν η λίστα δεν περιέχει στοιχεία τότε ο παίκτης κάνει λάθος
            guess2=possible1[randint(0,len(possible1)-1)] #ο υπολογιστής επιλέγει τυχαία μαντεψιά από τις υπόλοιπες
            box21['bg']=guess2[0] #χρωματίζονται τα κουτιά της επόμενης γραμμής
            box22['bg']=guess2[1]
            box23['bg']=guess2[2]
            box24['bg']=guess2[3]
        else:
            messagebox2=tk.Toplevel() #ανοίγει προειδοποιητικό παράθυρο για ύπαρξη λάθους
            wronglabel=tk.Label(messagebox2,bg='red',text='''Έκανες κάτι λάθος''',font='Arial 15')
            wronglabel.grid(row=0,column=0)
def ok2():
    global b,w,i,guess2,guess3,possible2,possible1,co,messagebox2
    okbutton2.destroy()
    okbutton3['state']='normal'
    possible2=[]
    for item in possible1:
        itemb=0
        itemw=0
        for t in range(0,4):
            if item[t]==guess2[t]:
                itemb+=1
        for a in range(0,4):
            if item[0]==guess2[a]:
                itemw+=1
            if item[1]==guess2[a]:
                itemw+=1
            if item[2]==guess2[a]:
                itemw+=1
            if item[3]==guess2[a]:
                itemw+=1
        itemw-=itemb
        if itemb==b and itemw==w:
            possible2.append(item)
    if b==4:
        winlabel=tk.Label(wind, bg='red', text='Ο υπολογιστής κέρδισε :(')
        winlabel.grid(row=0, column=0)
        okbutton3.destroy()
        okbutton4.destroy()
        okbutton5.destroy()
        blackbutton['state']='disabled'
        whitebutton['state']='disabled'
    else:
        i-=1
        co=7
        b,w=0,0
        if len(possible2)!=0:
            guess3=possible2[randint(0,len(possible2)-1)]
            box31['bg']=guess3[0]
            box32['bg']=guess3[1]
            box33['bg']=guess3[2]
            box34['bg']=guess3[3]
        else:
            messagebox2=tk.Toplevel()
            wronglabel=tk.Label(messagebox2,bg='red',text='''Έκανες κάτι λάθος''',font='Arial 15')
            wronglabel.grid(row=0,column=0)

def ok3():
    global b,w,i,guess3,guess4,possible2,possible3,co,messagebox2
    okbutton3.destroy()
    okbutton4['state']='normal'
    possible3=[]
    for item in possible2:
        itemb=0
        itemw=0
        for t in range(0,4):
            if item[t]==guess3[t]:
                itemb+=1
        for a in range(0,4):
            if item[0]==guess3[a]:
                itemw+=1
            if item[1]==guess3[a]:
                itemw+=1
            if item[2]==guess3[a]:
                itemw+=1
            if item[3]==guess3[a]:
                itemw+=1
        itemw-=itemb
        if itemb==b and itemw==w:
            possible3.append(item)
    if b==4:
        winlabel=tk.Label(wind, bg='red', text='Ο υπολογιστής κέρδισε :(')
        winlabel.grid(row=0, column=0)
        okbutton4.destroy()
        okbutton5.destroy()
        blackbutton['state']='disabled'
        whitebutton['state']='disabled'
    else:
        i-=1
        co=7
        b,w=0,0
        if len(possible3)!=0:
            guess4=possible3[randint(0,len(possible3)-1)]
            box41['bg']=guess4[0]
            box42['bg']=guess4[1]
            box43['bg']=guess4[2]
            box44['bg']=guess4[3]
        else:
            messagebox2=tk.Toplevel()
            wronglabel=tk.Label(messagebox2,bg='red',text='''Έκανες κάτι λάθος''',font='Arial 15')
            wronglabel.grid(row=0,column=0)

def ok4():
    global b,w,i,guess5,guess4,possible3,possible4,co,messagebox2
    okbutton4.destroy()
    okbutton5['state']='normal'
    possible4=[]
    for item in possible3:
        itemb=0
        itemw=0
        for t in range(0,4):
            if item[t]==guess4[t]:
                itemb+=1
        for a in range(0,4):
            if item[0]==guess4[a]:
                itemw+=1
            if item[1]==guess4[a]:
                itemw+=1
            if item[2]==guess4[a]:
                itemw+=1
            if item[3]==guess4[a]:
                itemw+=1
        itemw-=itemb
        if itemb==b and itemw==w:
            possible4.append(item)
    if b==4:
        winlabel=tk.Label(wind, bg='red', text='Ο υπολογιστής κέρδισε :(')
        winlabel.grid(row=0, column=0)
        okbutton5.destroy()
        blackbutton['state']='disabled'
        whitebutton['state']='disabled'
    else:
        i-=1
        co=7
        b,w=0,0
        if len(possible4)!=0:
            guess5=possible4[randint(0,len(possible4)-1)]
            box51['bg']=guess5[0]
            box52['bg']=guess5[1]
            box53['bg']=guess5[2]
            box54['bg']=guess5[3]
        else:
            messagebox2=tk.Toplevel()
            wronglabel=tk.Label(messagebox2,bg='red',text='''Έκανες κάτι λάθος''',font='Arial 15')
            wronglabel.grid(row=0,column=0)

def ok5():
    global b,w,i,possible4,messagebox2
    okbutton5.destroy()
    possible5=[]
    for item in possible3:
        itemb=0
        itemw=0
        for t in range(0,4):
            if item[t]==guess4[t]:
                itemb+=1
        for a in range(0,4):
            if item[0]==guess4[a]:
                itemw+=1
            if item[1]==guess4[a]:
                itemw+=1
            if item[2]==guess4[a]:
                itemw+=1
            if item[3]==guess4[a]:
                itemw+=1
        itemw-=itemb
        if itemb==b and itemw==w:
            possible5.append(item)
    if b!=4:
        if len(possible5)!=0:
            loselabel=tk.Label(wind, bg='green', text='Ο υπολογιστής έχασε :)')
            loselabel.grid(row=0, column=0)
        else:
            messagebox2=tk.Toplevel()
            wronglabel=tk.Label(messagebox2,bg='red',text='''Έκανες κάτι λάθος''',font='Arial 15')
            wronglabel.grid(row=0,column=0)
    if b==4:
        winlabel=tk.Label(wind, bg='red', text='Ο υπολογιστής κέρδισε :(')
        winlabel.grid(row=0, column=0)


def start(): #ξεκίνημα του παιχνιδιού μετά την επιλογή συνδυασμού 
    box11['bg']=guess1[0] #εμφάνιση πρώτης μαντεψιάς
    box12['bg']=guess1[1]
    box13['bg']=guess1[2]
    box14['bg']=guess1[3]
    startbutton.destroy()
    okbutton1['state']='normal'
    blackbutton['state']='normal'
    whitebutton['state']='normal'


def play_codemaker():
    global c,code1,code2,code3,code4,okbutton1,okbutton2,okbutton3,okbutton4,okbutton5,\
           startbutton,winlabel,loselbel,winbutton,wronglabel,possible,guess1,\
           greenbutton,b,w,i,co,wind,wind2,redbutton,purplebutton,pinkbutton,bluebutton,yellowbutton,blackbutton,\
           whitebutton,box11,box12,box13,box14,box21,box22,box23,box24,box31,box32,box33,box34,box41,box42,box43,box44,\
           box51,box52,box53,box54,box61,box62,box63,box64,\
           box71,box72,box73,box74,box81,box82,box83,box84,messagebox2
    wind2= tk.Toplevel() #παράθυρο που περιέχει τον συνδυασμό του παίκτη
    wind= tk.Toplevel() #παράθυρο codemaker
    wind.title('Codemaker')
    wind2.geometry('300x100+1000+100')
    wind2.title('Ο συνδυασμός μου')
    mainbg=tk.PhotoImage(file=ima)
    mylabel=tk.Label(wind,image=mainbg)
    mylabel.place(x=0,y=0)
    mylabel2=tk.Label(wind2, image=mainbg)
    mylabel2.place(x=0,y=0)
    wind.geometry('1000x1000+0+0')
    b=0 #θα δείχνει τα σωστά στη σωστή θέση 
    w=0 #θα δείχνει τα σωστά σε λάθος θέση
    i=10 
    co=7
    c=0
    #κουμπιά ελέγχου μαντεψιάς του υπολογιστή
    okbutton1=tk.Button(wind,text='OK',command=ok1, bg='grey',state= 'disabled')
    okbutton2=tk.Button(wind,text='OK',command=ok2, bg='grey',state= 'disabled')
    okbutton3=tk.Button(wind,text='OK',command=ok3, bg='grey',state= 'disabled')
    okbutton4=tk.Button(wind,text='OK',command=ok4, bg='grey',state= 'disabled')
    okbutton5=tk.Button(wind,text='OK',command=ok5, bg='grey',state= 'disabled')

    okbutton1.grid(column=6,row=10,padx=10,columnspan=2)
    okbutton2.grid(column=6,row=9,padx=10,columnspan=2)
    okbutton3.grid(column=6,row=8,padx=10,columnspan=2)
    okbutton4.grid(column=6,row=7,padx=10,columnspan=2)
    okbutton5.grid(column=6,row=6,padx=10,columnspan=2)

    startbutton = tk.Button(wind2, text='START', command= start, bg='green',state= 'disabled')
    startbutton.grid(row=2, column=1)
    # ορίζω τα κουτιά-κουμπιά για τον codemaker(για κάθε κουτί boxab το a συμβολίζει τη γραμμή
    # του κουτιού ξεκινώντας από κάτω και το b συμβολίζει τη στήλη του κουτιού
    box11=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box12=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box13=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box14=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')

    box11.grid(column=2,row=10,padx=10,pady=2)
    box12.grid(column=3,row=10,padx=10,pady=2)
    box13.grid(column=4,row=10,padx=10,pady=2)
    box14.grid(column=5,row=10,padx=10,pady=2)

    box21=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box22=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box23=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box24=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')

    box21.grid(column=2,row=9,padx=10,pady=2)
    box22.grid(column=3,row=9,padx=10,pady=2)
    box23.grid(column=4,row=9,padx=10,pady=2)
    box24.grid(column=5,row=9,padx=10,pady=2)

    box31=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box32=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box33=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box34=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')

    box31.grid(column=2,row=8,padx=10,pady=2)
    box32.grid(column=3,row=8,padx=10,pady=2)
    box33.grid(column=4,row=8,padx=10,pady=2)
    box34.grid(column=5,row=8,padx=10,pady=2)

    box41=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box42=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box43=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box44=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')

    box41.grid(column=2,row=7,padx=10,pady=2)
    box42.grid(column=3,row=7,padx=10,pady=2)
    box43.grid(column=4,row=7,padx=10,pady=2)
    box44.grid(column=5,row=7,padx=10,pady=2)

    box51=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box52=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box53=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')
    box54=tk.Button(wind,bg='#C9824B',padx=3,pady=1, state='disabled')

    box51.grid(column=2,row=6,padx=10,pady=2)
    box52.grid(column=3,row=6,padx=10,pady=2)
    box53.grid(column=4,row=6,padx=10,pady=2)
    box54.grid(column=5,row=6,padx=10,pady=2)

    mnumber1=tk.Label(wind, bg='#C9824B', text='1')
    mnumber2=tk.Label(wind, bg='#C9824B', text='2')
    mnumber3=tk.Label(wind, bg='#C9824B', text='3')
    mnumber4=tk.Label(wind, bg='#C9824B', text='4')
    mnumber5=tk.Label(wind, bg='#C9824B', text='5')
    
    mnumber1.grid(column=0,row=10,padx=(300,3))
    mnumber2.grid(column=0,row=9,padx=(300,3))
    mnumber3.grid(column=0,row=8,padx=(300,3))
    mnumber4.grid(column=0,row=7,padx=(300,3))
    mnumber5.grid(column=0,row=6,padx=(300,3))
    
    titlecm=tk.Label(wind, bg='#C9824B',text='Codemaker',font='Arial 15')
    titlecm.grid(column=1,row=0,columnspan=6,pady=100)
    #λίστα που περιέχει όλους τους πιθανούς συνδυασμούς με αυτά τα 6 χρώματα
    possible= list(permutations( ('#A6E345', '#D43D40', '#2EEAEB', '#FFFC47', '#FA8EDC', '#9D2AA6'), 4) )
    guess1=possible[randint(0,len(possible)-1)] #η πρώτη τυχαία μαντεψιά
    #κουμπιά χρωματισμού για τον συνδυασμό του παίκτη 
    greenbutton=tk.Button(wind2,bg='#A6E345',padx=3,pady=1,command=mgreenit)
    redbutton=tk.Button(wind2,bg='#D43D40',padx=3,pady=1,command=mredit)
    bluebutton=tk.Button(wind2,bg='#2EEAEB',padx=3,pady=1,command=mblueit)
    yellowbutton=tk.Button(wind2,bg='#FFFC47',padx=3,pady=1,command=myellowit)
    pinkbutton=tk.Button(wind2,bg='#FA8EDC',padx=3,pady=1,command=mpinkit)
    purplebutton=tk.Button(wind2,bg='#9D2AA6',padx=3,pady=1,command=mpurpleit)

    greenbutton.grid(row=11,column=7)
    redbutton.grid(row=11,column=8)
    bluebutton.grid(row=11,column=9)
    yellowbutton.grid(row=11,column=10)
    pinkbutton.grid(row=11,column=11)
    purplebutton.grid(row=11,column=12) 
    #κουμπιά που περιέχουν τον συνδυασμό του παίκτη
    code1=tk.Button(wind2, bg='#C9824B', padx=5, pady=5, state='disabled')
    code2=tk.Button(wind2, bg='#C9824B', padx=5, pady=5, state='disabled')
    code3=tk.Button(wind2, bg='#C9824B', padx=5, pady=5, state='disabled')
    code4=tk.Button(wind2, bg='#C9824B', padx=5, pady=5, state='disabled')

    code1.grid(column=2, row=11)
    code2.grid(column=3, row=11)
    code3.grid(column=4, row=11)
    code4.grid(column=5, row=11)
    #εμφάνιση μαύρων και άσπρων ενδείξεων
    blackbutton=tk.Button(wind,bg='black',command=putblack, state='disabled')
    whitebutton=tk.Button(wind,bg='white',command=putwhite, state='disabled')

    blackbutton.grid(column=6,row=11,padx=7)
    whitebutton.grid(column=7,row=11,padx=7)
    
    mexitbutton=tk.Button(wind,text='Exit',font='Arial 8',fg='white',bg='red',padx=8,command=mexit_game)
    mrestartbutton=tk.Button(wind,text='Restart',font='Arial 8',fg='white',bg='green',padx=8,command=mrestart_game)

    mexitbutton.grid(row=13,column=6,columnspan=2)
    mrestartbutton.grid(row=12,column=6,columnspan=2)

    wind.mainloop()

#κουμπιά του αρχικού μενού
#κουμπί που εμφανίζει τους κανόνες
b_rules= tk.Button(app, text= 'Κανόνες παιχνιδιού', \
                   command= rules, padx= 50, pady=8, bg= '#7b440c',font=('Helvetica', '16'))

#κουμπί που εμφανίζει τον codemaker
b_maker= tk.Button(app, text= 'Παίξε ως Codemaker', \
                   command= play_codemaker,padx= 45, pady=8, bg='#7b440c',font=('Helvetica', '16'))
#κουμπί που εμφανίζει τον codebreaker
b_breaker= tk.Button(app, text= 'Παίξε ως Codebreaker', \
                     command= play_codebreaker,padx= 38, pady=8, bg= '#7b440c',font=('Helvetica', '16'))

#εισαγωγή κουμπιών στον καμβά
set_rules= can.create_window(640, 200, anchor='nw', window= b_rules)
set_maker= can.create_window(640, 260, anchor='nw',  window= b_maker)
set_breaker= can.create_window(640, 320, anchor='nw',  window= b_breaker)

app.mainloop()

