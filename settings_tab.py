import customtkinter as ctk

def create_settings_tab(parent, logout_callback):
    frame = parent
    label = ctk.CTkLabel(frame, text="Settings", font=("Bauhaus 93", 20))
    label.pack(pady=20)

    logout_button = ctk.CTkButton(frame, text="Logout", command=logout_callback, font=("Bauhaus 93", 16))
    logout_button.pack(pady=12)
    
    return frame