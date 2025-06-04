import tkinter as tk


def on_close():
    root.destroy()


root = tk.Tk()
root.title('Prosta aplikacja')
root.geometry('300x150')

label = tk.Label(root, text='Witaj w prostym GUI!')
label.pack(pady=20)

button = tk.Button(root, text='Zamknij', command=on_close)
button.pack()

root.mainloop()
