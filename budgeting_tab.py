import customtkinter as ctk

def create_budgeting_tab(parent):
    frame = parent
    label = ctk.CTkLabel(frame, text="Welcome back! \n Total Balance: $5,240")
    label.pack(pady=40)
    return frame
