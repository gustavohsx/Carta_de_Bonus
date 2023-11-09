from tkinter import Tk
from Tela import Tela

a = Tk()
a.title('Carta de Bônus')
aa = Tela(a)
larguraTela = a.winfo_screenwidth()
alturaTela = a.winfo_screenheight()
a.geometry(f'{larguraTela}x{alturaTela}+-10+0')

a.mainloop()
