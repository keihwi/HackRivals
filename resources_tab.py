import customtkinter as ctk
import webbrowser

# list of websites that offer free credit checks.
CREDITRESOURCES = { "Myfico.com": "https://www.myfico.com/",
            "Experian": "https://www.experian.com/", 
            "Equifax": "https://www.equifax.com/", 
}

HELPRESOURCES = { "Financial abuse help": "https://womenshealth.gov/relationships-and-safety/other-types/financial-abuse",
}

HEALTHRESOURCES = { "Financial abuse help": "https://womenshealth.gov/relationships-and-safety/other-types/financial-abuse",
}
PROFESSIONALRESOURCES = { "Financial abuse help": "https://womenshealth.gov/relationships-and-safety/other-types/financial-abuse",
                         "Linkedin carreer resoures": "https://womenshealth.gov/relationships-and-safety/other-types/financial-abuse",

}


def create_resources_tab(parent):
    # 1. Create a Scrollable Frame instead of a regular Frame
    # 'parent' is the tabview or main window
    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Main Title
    title = ctk.CTkLabel(scroll_frame, text="Resources", font=("Bauhaus 93", 26))
    title.pack(pady=(10, 20))

    # --- Section: Credit Score ---
    credit_label = ctk.CTkLabel(scroll_frame, text="Free Credit Score Checks:", font=("Arial Rounded MT Bold", 18))
    credit_label.pack(anchor="w", padx=30, pady=(10, 5))
    
    for name, url in CREDITRESOURCES.items():
        link = ctk.CTkLabel(scroll_frame, text=name, text_color="#1f538d", cursor="hand2", font=("Arial Rounded MT Bold", 14, "underline")) 
        link.pack(anchor="w", padx=45, pady=2) 
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    # --- Section: Financial Abuse ---
    # Since you have multiple dicts (HEALTHRESOURCES, etc.), we can loop through them too
    abuse_label = ctk.CTkLabel(scroll_frame, text="Support & Safety:", font=("Arial Rounded MT Bold", 18))
    abuse_label.pack(anchor="w", padx=30, pady=(20, 5))

    for name, url in HELPRESOURCES.items():
        link = ctk.CTkLabel(scroll_frame, text=name, text_color="#1f538d", cursor="hand2", font=("Arial Rounded MT Bold", 14, "underline")) 
        link.pack(anchor="w", padx=45, pady=2) 
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    # Return the scroll_frame so it can be used by the main app
    return scroll_frame
