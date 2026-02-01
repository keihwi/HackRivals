import customtkinter as ctk

def create_settings_tab(parent, logout_callback):
    frame = parent
    label = ctk.CTkLabel(frame, text="Settings", font=("Cooper Black", 20))
    label.pack(pady=20)

    logout_button = ctk.CTkButton(frame, text="logout", command=logout_callback, font=("Cooper Black", 16))
    logout_button.pack(pady=12)
    
    return frame