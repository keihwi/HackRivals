import customtkinter as ctk

def create_chatbot_tab(parent):
    frame = parent
    label = ctk.CTkLabel(frame, text="chatbot", font=("Bauhaus 93", 20))
    label.pack(pady=20)
    return frame