import customtkinter as ctk

from PIL import Image
from PIL import ImageTk
import os
import sys
import json
import matplotlib.pyplot as plt

# HELPER FUNCTION FOR EXECUTABLE FILE
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from budgeting_tab import create_budgeting_tab
from subscriptions_tab import create_subscriptions_tab
from obligations_tab import create_obligations_tab
from resources_tab import create_resources_tab
from chat_bot_tab import create_chatbot_tab
from settings_tab import create_settings_tab


# Appearance Mode: "light" or "dark", defaulted to dark
ctk.set_appearance_mode("light")

ctk.set_default_color_theme(resource_path("girl-math.json"))

# ctk.CTk means we want the app to act exactly like a standard window (inheritance)
class GirlMath(ctk.CTk):

    # runs automatically the moment the app starts
    # self means it is referring to the GirlMath app
    def __init__(self):

        # this function uses the ctk.CTk blueprint to set up behind-the-scenes window stuff
        super().__init__()

        self.passphrase = "1234"  # Default password
        self.load_config()        # Load real password from file

        # title of the app
        self.title("GirlMath")

        icon_path = resource_path(os.path.join("images", "girl-math-logo-acronym.ico"))
        self.after(200, lambda: self.iconbitmap(icon_path))

        # Default window size, can be changed later
        self.geometry("800x450")

        # Prevents user from making it smaller than 400x300 pixels
        self.minsize(400, 300)

        # Tells app what to do when closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Show login screen
        self.show_login()

    def load_config(self):
        """Loads password from json, or creates default if missing."""
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    self.passphrase = data.get("passphrase", "1234")
            except json.JSONDecodeError:
                self.save_config() 
        else:
            self.save_config() 

    def save_config(self):
        """Saves current password to json."""
        with open("config.json", 'w') as f:
            json.dump({"passphrase": self.passphrase}, f)

    def handle_password_change(self, old_pass, new_pass):
        """Callback used by Settings tab to update password."""
        if old_pass == self.passphrase:
            self.passphrase = new_pass
            self.save_config()
            return True, "Password updated successfully!"
        else:
            return False, "Incorrect current passphrase."

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



        logo_path = resource_path(os.path.join("images", "girl-math-logo.png"))
        
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

        self.label = ctk.CTkLabel(self.fields_inner, text="Welcome!", font=("Cooper Black", 24), text_color=("#434242"))
        self.label.pack(pady=12, padx=10)

        # Show="*" means it will add asterisks as passphrase is typed in. Throws onto screen.
        self.passphrase_entry = ctk.CTkEntry(self.fields_inner, placeholder_text="passphrase", show="*", font=("Cooper Black", 15), placeholder_text_color=("#D4D2CE"), text_color=("#434242"), justify="center" )
        self.passphrase_entry.pack(pady=12, padx=10)

        # creates a button and calls login function below. Throws it onto the window.
        self.login_button = ctk.CTkButton(self.fields_inner, text="login", command=self.login_action, font=("Cooper Black", 16), text_color=("#434242"))
        self.login_button.pack(pady=12, padx=10)

    def login_action(self):
        # Compare against the loaded passphrase variable
        if self.passphrase_entry.get() == self.passphrase:
            # Remove login screen
            self.login_frame.destroy()
            # Show dashboard
            self.show_dashboard()
        else:
            self.label.configure(text="Wrong Passphrase!", text_color="#434242", font=("Cooper Black", 24))

    # Show Dashboard Function
    def show_dashboard(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(padx=20, pady=20, fill="both", expand=True)
        self.tabs._segmented_button.configure(font=("Cooper Black", 20))

        # Add tabs
        self.tabs.add("Budgeting")
        self.tabs.add("Subscriptions")
        self.tabs.add("Obligations")
        self.tabs.add("Resources")
        self.tabs.add("ChatBot")
        self.tabs.add("Settings")

        # Populate each tab using the external files
        create_budgeting_tab(self.tabs.tab("Budgeting"))
        create_subscriptions_tab(self.tabs.tab("Subscriptions"))
        create_obligations_tab(self.tabs.tab("Obligations"))
        create_resources_tab(self.tabs.tab("Resources"))
        create_chatbot_tab(self.tabs.tab("ChatBot"))
        create_settings_tab(self.tabs.tab("Settings"), self.logout_action, self.handle_password_change)

    # Logout Function
    def logout_action(self):
        # Remove the tabs
        self.tabs.destroy()

        #Go back to login
        self.show_login()

    def on_closing(self):
        """Cleanly shuts down everything to prevent background errors"""
        try:
            plt.close('all') # Closes all Matplotlib figures
        except:
            pass
        
        self.quit()      # Stops the mainloop
        self.destroy()   # Destroys the widgets
        os._exit(0)      # Forcefully kills the process to prevent the DPI error

if __name__ == "__main__":
    app = GirlMath()
    app.mainloop()