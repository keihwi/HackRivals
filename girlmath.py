import customtkinter as ctk

from PIL import Image
from PIL import ImageTk
import os

from budgeting_tab import create_budgeting_tab
from expenses_tab import create_expenses_tab
from obligations_tab import create_obligations_tab
from resources_tab import create_resources_tab
from settings_tab import create_settings_tab


# Appearance Mode: "light" or "dark", defaulted to dark
ctk.set_appearance_mode("light")

ctk.set_default_color_theme("girl-math.json")

# ctk.CTk means we want the app to act exactly like a standard window (inheritance)
class GirlMath(ctk.CTk):

    # runs automatically the moment the app starts
    # self means it is referring to the GirlMath app
    def __init__(self):

        # this function uses the ctk.CTk blueprint to set up behind-the-scenes window stuff
        super().__init__()

        # title of the app
        self.title("GirlMath")

        self.after(200, lambda: self.iconbitmap(os.path.join(os.path.dirname(__file__), "images", "girl-math-logo-acronym.ico")))

        # Default window size, can be changed later
        self.geometry("600x450")

        # Prevents user from making it smaller than 400x300 pixels
        self.minsize(400, 300)

        # Show login screen
        self.show_login()

    def show_login(self):
        # Main login container
        # creates a container inside the window, self meaning GirlMath is that window
        self.login_frame = ctk.CTkFrame(self)
        # change the frame color forcefully
        self.login_frame.configure(fg_color="white")

        # says to throw this onto the window and center it. Pad adds space above and below.
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)


        # Configure two columns: logo on left, login fields on right
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_rowconfigure(0, weight=1)


        # Left side: Logo
        # creates a text box and throws it onto the window
        # sticky = "nsew" makes its central north, east, west.
        self.logo_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)



        logo_path = os.path.join(os.path.dirname(__file__), "images", "girl-math-logo.png")
        self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(310, 200))
        self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.logo_image, text="")
        self.logo_label.pack(expand=True)

        

        # Right side: Login fields
        self.fields_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.fields_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.fields_frame.configure(fg_color="#F2F1ED")
        

        # Inner frame to center login fields vertically
        self.fields_inner = ctk.CTkFrame(self.fields_frame, fg_color="transparent")
        self.fields_inner.place(relx=0.5, rely=0.5, anchor="center")

        self.label = ctk.CTkLabel(self.fields_inner, text="Welcome!", font=("Bauhaus 93", 24))
        self.label.pack(pady=12, padx=10)

        # Show="*" means it will add asterisks as passphrase is typed in. Throws onto screen.
        self.passphrase_entry = ctk.CTkEntry(self.fields_inner, placeholder_text="passphrase", show="*", font=("Bauhaus 93", 15), justify="center" )
        self.passphrase_entry.pack(pady=12, padx=10)

        # creates a button and calls login function below. Throws it onto the window.
        self.login_button = ctk.CTkButton(self.fields_inner, text="Login", command=self.login_action, font=("Bauhaus 93", 16))
        self.login_button.pack(pady=12, padx=10)

    def login_action(self):
        # Passphrase
        if self.passphrase_entry.get() == "Picture JohnCena SpaceX":
            # Remove login screen
            self.login_frame.destroy()
            # Show dashboard
            self.show_dashboard()
        else:
            self.label.configure(text="Wrong passphrase!", text_color="red", font=("Verdana", 16))

    # Show Dashboard Function
    def show_dashboard(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(padx=20, pady=20, fill="both", expand=True)
        self.tabs._segmented_button.configure(font=("Bauhaus 93", 20))

        # Add tabs
        self.tabs.add("Budgeting")
        self.tabs.add("Expenses")
        self.tabs.add("Obligations")
        self.tabs.add("Resources")
        self.tabs.add("Settings")

        # Populate each tab using the external files
        create_budgeting_tab(self.tabs.tab("Budgeting"))
        create_expenses_tab(self.tabs.tab("Expenses"))
        create_obligations_tab(self.tabs.tab("Obligations"))
        create_resources_tab(self.tabs.tab("Resources"))
        create_settings_tab(self.tabs.tab("Settings"), self.logout_action)

    # Logout Function
    def logout_action(self):
        # Remove the tabs
        self.tabs.destroy()

        #Go back to login
        self.show_login()

if __name__ == "__main__":
    app = GirlMath()
    app.mainloop()