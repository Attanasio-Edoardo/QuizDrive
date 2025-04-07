import tkinter as tk
from tkinter import messagebox
import random
import json
from PIL import Image, ImageTk


def carica_domande(num_domande=30):
    try:
        with open('domande.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            tutte_domande = []
            for categoria in data.values():
                tutte_domande.extend(categoria)

            random.shuffle(tutte_domande)
            domande_selezionate = tutte_domande[:num_domande]
    except FileNotFoundError:
        print("File non trovato")
        return []
    return domande_selezionate

def carica_domande_sezione(titolo, num_domande=30):
    try:
        with open('domande.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            tutte_domande = []
            for domanda in data[titolo]:
                tutte_domande.append(domanda)

            random.shuffle(tutte_domande)
            domande_selezionate = tutte_domande[:num_domande]
    except FileNotFoundError:
        print("File non trovato")
        return []
    return domande_selezionate

class HomePage(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('Quiz patente B')
        self.master.geometry('1920x1080')
        self.crea_oggetti_pagina()

    def crea_oggetti_pagina(self):
        self.nav = tk.Label(self.master, bg="#252850", width=200, height=100)
        self.nav.place(x=940, y=0)
        self.label_title()
        self.crea_label_esercitazioni('SEGNALI DI PERICOLO',0.15, 0.3)
        self.crea_label_esercitazioni('PRECEDENZA',0.35,0.3)
        self.crea_label_esercitazioni('SEGNALI DI INDICAZIONE',0.15,0.4)
        self.crea_label_esercitazioni('DIVIETO',0.35,0.4)
        self.crea_label_esercitazioni('OBBLIGO',0.15,0.5)
        self.crea_label_esercitazioni('AUTOSTRADE',0.35, 0.5)
        self.start_quiz_btn()
        self.exit_button()

    def label_title(self):
        label_title = tk.Label(self.master, text="ESERCITAZIONI", font=("Garamond", 40, "bold"),  fg='#252850')
        label_title.place(relx=0.13, rely=0.1, anchor="nw")
        label_title2 = tk.Label(self.master, text="ESAME B", font=("Garamond", 40, "bold"),  fg='#ffffff', bg='#252850')
        label_title2.place(relx=0.7, rely=0.1, anchor="nw")


    def crea_label_esercitazioni(self, titolo, relx, relyp):
        btn = tk.Button(self.master, text=titolo, font=("Garamond", 13, "bold"), bg="#ffffff",fg="#252850", command= lambda: ese_scheda(titolo.lower()))        
        btn.place(relx=relx, rely=relyp, anchor="center")
        btn.config(width=35, height=5)

    def start_quiz_btn(self):
        start = tk.Button(self.master, text="Inizia il test", font=("Garamond", 13, "bold"),bg="lightblue",fg="black", command= main_scheda)        
        start.place(relx=0.75, rely=0.4, anchor="center")
        start.config(width=35, height=5)

    def exit_button(self):
        exit = tk.Button(self.master, text='Esci', bg="lightblue", command= self.master.quit)
        exit.place(x = 1700, y= 890)



class QuizApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.idx = 0
        self.domande = carica_domande()
        if not self.domande:
            self.destroy()
            return
            
        self.title('Scheda Quiz')
        self.geometry('1920x1080')
        self.resizable(0, 0)
        self.risposte_utente = [tk.IntVar(value=2) for _ in range(30)]
        self.punti = 0
        self.secondi = 20 * 60 

        self.crea_oggetti_pagina()
        self.mostra_domanda()
        self.aggiorna()

    def crea_oggetti_pagina(self):
        bg = tk.Label(self, bg="#ffffff", width=1920, height=1080)
        bg.place(x=0, y=0)
        
        nav = tk.Label(self, bg="#252850", width=400, height=7)
        nav.place(x=0, y=0)
        snav = tk.Label(self, bg="#C0C0C0", width=400, height=3)
        snav.place(x=0, y=120)
        
        label_title = tk.Label(self, text="Quiz Patente 2025", font=("Garamond", 40, "bold"), fg="#ffffff", bg='#252850')
        label_title.place(x = 30 , y = 30)

        self.btns = []
        for i in range(30):
            self.btn_n_domanda = tk.Button(self, text=f'{i + 1}', command=lambda i = i : self.vai_alla_domanda(i), width=3, padx=3)
            self.btn_n_domanda.place(x = i*35 + 630 , y = 900)
            self.btns.append(self.btn_n_domanda)

        self.contatore = tk.Label(
            self, 
            text="", 
            bg="lightblue",
            fg="#000080", 
            font=('Garamond', 12, 'bold'),
            width=15,
            padx=5,
            pady=5
        )
        self.contatore.place(x=1600, y=130)
        
        self.label_num_domanda = tk.Label(
            self,
            text="",
            font=('Garamond', 20, 'bold'), 
            bg="#ffffff"
        )
        self.label_num_domanda.place(x=350, y=300)

        self.label_domande = tk.Label(
            self, 
            text="", 
            font=('Garamond', 15), 
            bg="#ffffff",
            wraplength=1000, 
            justify="left"
        )
        self.label_domande.place(x=700, y=450, width=1000)
        
        self.label_immagine = tk.Label(self, bg='white')
        self.label_immagine.place(x=300, y=350, width=400, height=300)
        
        self.btn_vero = tk.Radiobutton(
            self, 
            text="Vero",
            variable=self.risposte_utente[self.idx], 
            value=1,
            font=('Garamond', 14),
            width=10
        )
        self.btn_vero.place(x=1300, y=800)
        
        self.btn_falso = tk.Radiobutton(
            self, 
            text="Falso", 
            variable=self.risposte_utente[self.idx],
            value=0, 
            font=('Garamond', 14),
            width=10
        )
        self.btn_falso.place(x=1500, y=800)
        
        self.btn_indietro = tk.Button(
            self, 
            text="← Indietro", 
            command=self.domanda_precedente,
            state=tk.DISABLED
        )
        self.btn_indietro.place(x=400, y=900)
        
        self.btn_avanti = tk.Button(
            self, 
            text="Avanti →", 
            command=self.domanda_successiva
        )
        self.btn_avanti.place(x=500, y=900)
        
        self.label_timer = tk.Label(
            self,
            text="",
            font=("Garamond", 12, "bold"),
            fg="#b62a38",
            bg="#e8a2b7",
            width=15,
            padx=5,
            pady=5,
        )
        self.label_timer.place(x=1760, y=130)

        self.btn_verifica = tk.Button(
            self, 
            text="Consegna", 
            command=self.verifica_risposte,
            bg="lightblue"
        )
        self.btn_verifica.place(x=450, y=800)

    def aggiorna_contatore_risposte(self):
        self.risposte_date = sum(1 for risposta in self.risposte_utente if risposta.get() != 2)
        self.contatore.config(text=f"Risposto a {self.risposte_date} di {len(self.domande)}")

    def vai_alla_domanda(self, indice):
        self.idx = indice   
        self.mostra_domanda()  

    def aggiorna(self):
        if self.secondi > 0:
            self.min_restanti = self.secondi // 60
            self.sec_restanti = self.secondi % 60
            self.label_timer.config(text=f'{self.min_restanti:02d}:{self.sec_restanti:02d}')
            self.secondi -= 1
            self.after(1000, self.aggiorna)
        else:
            messagebox.showinfo("TEMPO SCADUTO", "test consegnato")
            self.verifica_risposte()

    def mostra_domanda(self):
        if self.idx < len(self.domande):
            domanda = self.domande[self.idx]

            self.label_num_domanda.config(text=f"Domanda n° {self.idx + 1}")
            self.aggiorna_contatore_risposte()
            self.btn_vero.config(variable=self.risposte_utente[self.idx])
            self.btn_falso.config(variable=self.risposte_utente[self.idx])
            # Mostra testo domanda
            self.label_domande.config(text=domanda['domanda'])
            # Mostra immagine se presente
            try:
                img = Image.open(domanda['immagine'])
                self.idxmg_tk = ImageTk.PhotoImage(img)
                self.label_immagine.config(image=self.idxmg_tk)
            except:
                self.label_immagine.config(image='', text="Immagine non disponibile")
                        
            # Disabilita pulsante indietro se siamo alla prima domanda
            self.btn_indietro.config(state=tk.DISABLED if self.idx == 0 else tk.NORMAL)
            
            # Disabilita pulsante avanti se siamo all'ultima domanda
            self.btn_avanti.config(state=tk.DISABLED if self.idx == len(self.domande)-1 else tk.NORMAL)

    def domanda_successiva(self):
        if self.idx < len(self.domande) - 1:
            self.idx += 1
            self.mostra_domanda()

    def domanda_precedente(self):
        if self.idx > 0:
            self.idx -= 1
            self.mostra_domanda()

    def verifica_risposte(self):
        risposte_utente_values = [self.risposte_utente[i].get() for i in range(len(self.domande))]
        for i in range(len(self.domande)):
            if risposte_utente_values[i] == 1 and self.domande[i]['risposta'] == 'vero' or risposte_utente_values[i] == 0 and self.domande[i]['risposta'] == 'falso':
                self.punti += 1
            
        messagebox.showinfo( title='TEST FINITO',message=f"""\
IL QUIZ È TERMINATO !
    Punteggio: {self.punti}
    {'Hai risposto a tutte le domande' if 2 not in risposte_utente_values else f'Hai risposto a {self.risposte_date} su 30'}
""")
        self.destroy()

class Esercitazione(QuizApp):
    def __init__(self, titolo):
        super().__init__()

        self.title("Scheda di esercitazione")
        self.domande = carica_domande_sezione(titolo)
    def mostra_domanda(self):
        if self.idx < len(self.domande):
            domanda = self.domande[self.idx]

            # Aggiorna contatore
            self.label_num_domanda.config(text=f"Domanda n° {self.idx + 1}")
            self.aggiorna_contatore_risposte()            
            self.btn_vero.config(variable=self.risposte_utente[self.idx])
            self.btn_falso.config(variable=self.risposte_utente[self.idx])
            # Mostra testo domanda
            self.label_domande.config(text=domanda['domanda'])
            # Mostra immagine se presente
            try:
                img = Image.open(domanda['immagine'])
                self.idxmg_tk = ImageTk.PhotoImage(img)
                self.label_immagine.config(image=self.idxmg_tk)
            except:
                self.label_immagine.config(image='', text="Immagine non disponibile")
            
            # Resetta selezione risposta
            
            # Disabilita pulsante indietro se siamo alla prima domanda
            self.btn_indietro.config(state=tk.DISABLED if self.idx == 0 else tk.NORMAL)
            
            # Disabilita pulsante avanti se siamo all'ultima domanda
            self.btn_avanti.config(state=tk.DISABLED if self.idx == len(self.domande)-1 else tk.NORMAL)

def ese_scheda(titolo):
    ese = Esercitazione(titolo)
    ese.geometry('1920x1080')
    ese.resizable(0, 0)
    ese.mainloop()

def main_scheda():
    f = QuizApp()
    f.title('Scheda d\'esame')
    f.geometry('1920x1080')
    f.resizable(0, 0)
    f.mainloop()

def chiama_esercitazione(arg):
    print(arg)
    
def main():
    f = HomePage()
    f.master.title('Quiz patente B')
    f.master.geometry('1920x1080')
    f.master.resizable(0, 0)
    f.mainloop()

main()