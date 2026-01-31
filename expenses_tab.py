import customtkinter as ctk

def create_expenses_tab(parent):
    frame = parent
    label = ctk.CTkLabel(frame, text="Expenses", font=("Bauhaus 93", 20))
    label.pack(pady=20)
    return frame
