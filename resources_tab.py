import customtkinter as ctk
import webbrowser

# list of websites that offer free credit checks.
CREDITRESOURCES = { "Myfico.com": "https://www.myfico.com/",
            "Experian": "https://www.experian.com/", 
            "Equifax": "https://www.equifax.com/", 

}

def create_resources_tab(parent):
    frame = parent
    label = ctk.CTkLabel(frame, text="Resources", font=("Bauhaus 93", 20))
    label.pack(pady=20)
    label = ctk.CTkLabel(frame, text="Resources", font=("Bauhaus 93", 20))
    label.pack(pady=5)
    for name, url in CREDITRESOURCES.items():
         link = ctk.CTkLabel( frame, text=name, text_color="blue", cursor="hand2", font=("Verdana", 14) ) 
         link.pack(anchor="w", padx=30, pady=1) # bind click to open the URL 
         link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    return frame
