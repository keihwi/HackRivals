import customtkinter as ctk

def create_obligations_tab(parent):
    frame = parent
    label = ctk.CTkLabel(frame, text="Obligations", font=("Bauhaus 93", 20))
    label.pack(pady=20)
    return frame
