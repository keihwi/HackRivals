import customtkinter as ctk
import webbrowser

# list of websites that offer free credit checks.
CREDITRESOURCES = { "Myfico.com": "https://www.myfico.com/",
            "Experian": "https://www.experian.com/", 
            "Equifax": "https://www.equifax.com/", 
}
#list of websites that contain health resources
HELPRESOURCES = { "Financial abuse help": "https://womenshealth.gov/relationships-and-safety/other-types/financial-abuse",
                 "Health Resources and Services Administration" : "https://www.hrsa.gov/",
                 "Identifying and protecting youself from financia abuse":"https://www.womenslaw.org/about-abuse/forms-abuse/financial-abuse",
}
#list of websites that contain professional resources.
PROFESSIONALRESOURCES = {
                        "Linkedin career resoures": "https://careers.linkedin.com/ResourceLibrary?selectedFilter=all",
                        "How to write a strong resume": "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/",
                        "Tax filing tips and resources for women":"https://www.savvyladies.org/education/taxes-quick-tips-free-resources-for-women/",

}


def create_resources_tab(parent):
    # 1. Create a Scrollable Frame instead of a regular Frame
    # 'parent' is the tabview or main window. creates spacing for next element.
    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Main Title
    title = ctk.CTkLabel(scroll_frame, text="Resources", font=("Cooper Black", 26), text_color=("#434242"))
    title.pack(pady=(10, 20))

    #Credit Scores
    credit_label = ctk.CTkLabel(scroll_frame, text="Free Credit Score Checks:", font=("Arial Rounded MT Bold", 18), text_color=("#434242"))
    credit_label.pack(anchor="w", padx=30, pady=(10, 5))
    #iterates each credit score link and prints them on the page.
    for name, url in CREDITRESOURCES.items():
        link = ctk.CTkLabel(scroll_frame, text=name, text_color="#1f538d", cursor="hand2", font=("Arial Rounded MT Bold", 14, "underline")) 
        link.pack(anchor="w", padx=45, pady=2) 
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    # Financial Abuse
    abuse_label = ctk.CTkLabel(scroll_frame, text="Support & Safety:", font=("Arial Rounded MT Bold", 18), text_color=("#434242"))
    abuse_label.pack(anchor="w", padx=30, pady=(20, 5))
    # iterates each healp source link and prints them on the page.
    for name, url in HELPRESOURCES.items():
        link = ctk.CTkLabel(scroll_frame, text=name, text_color="#1f538d", cursor="hand2", font=("Arial Rounded MT Bold", 14, "underline")) 
        link.pack(anchor="w", padx=45, pady=2) 
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    #Section: Professional resources
    abuse_label = ctk.CTkLabel(scroll_frame, text="Professional Resources:", font=("Arial Rounded MT Bold", 18), text_color=("#434242"))
    abuse_label.pack(anchor="w", padx=30, pady=(20, 5))
    #iterates each professional source link and prints them on the page.
    for name, url in PROFESSIONALRESOURCES.items():
        link = ctk.CTkLabel(scroll_frame, text=name, text_color="#1f538d", cursor="hand2", font=("Arial Rounded MT Bold", 14, "underline")) 
        link.pack(anchor="w", padx=45, pady=2) 
        link.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))

    # Return the scroll_frame so it can be used by the main app
    return scroll_frame
