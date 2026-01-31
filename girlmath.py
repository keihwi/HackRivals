import customtkinter as ctk

# Appearance Mode: "light" or "dark", defaulted to dark
ctk.set_appearance_mode("dark")

# Color Theme: "blue", "green", or "dark-blue" WILL BE CHANGED WITH JSON FILE
ctk.set_default_color_theme("green")

# ctk.CTk means we want the app to act exactly like a standard window (inheritance)
class GirlMath(ctk.CTk):

    # runs automatically the moment the app starts
    # self means it is referring to the GirlMath app
    def __init__(self):

        # this function uses the ctk.CTk blueprint to set up behind-the-scenes window stuff
        super().__init__()

        # title of the app
        self.title("Girl Math")

        # Default window size, can be changed later
        self.geometry("600x450")

        # Prevents user from making it smaller than 400x300 pixels
        self.minsize(400, 300)

        # Show login screen
        self.show_login()

    def show_login(self):
        # creates a container inside the window, self meaning GirlMath is that window
        self.login_frame = ctk.CTkFrame(self)

        # says to throw this onto the window and center it. Pad adds space above and below.
        self.login_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # creates a text box and throws it onto the window
        self.label = ctk.CTkLabel(self.login_frame, text="GirlMath Login", font=("Roboto", 24))
        self.label.pack(pady=12, padx=10)

        # Show="*" means it will add asterisks as passphrase is typed in. Throws onto screen.
        self.passphrase_entry = ctk.CTkEntry(self.login_frame, placeholder_text="passphrase", show="*")
        self.passphrase_entry.pack(pady=12, padx=10)

        # creates a button and calls login function below. Throws it onto the window.
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_action)
        self.login_button.pack(pady=12, padx=10)

    def login_action(self):
        # Passphrase
        if self.passphrase_entry.get() == "Picture JohnCena SpaceX":
            # Remove login screen
            self.login_frame.destroy()
            # Show dashboard
            self.show_dashboard()
        else:
            self.label.configure(text="Wrong passphrase!", text_color="red")

    # Show Dashboard Function
    def show_dashboard(self):
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(padx=20, pady=20, fill="both", expand=True)

        self.tabs.add("Summary")
        self.tabs.add("Expenses")
        self.tabs.add("Savings")
        self.tabs.add("Settings")

        # Add content to Summary Tab
        self.summary_label = ctk.CTkLabel(self.tabs.tab("Summary"), text="Welcome back! \n Total Balance: $5,240")
        self.summary_label.pack(pady=40)

        # Content for Settings Tab (Logout)
        self.logout_button = ctk.CTkButton(self.tabs.tab("Settings"), text="Logout", fg_color="red", hover_color="darkred", command=self.logout_action)
        self.logout_button.pack(pady=20)

    # Logout Function
    def logout_action(self):
        # Remove the tabs
        self.tabs.destroy()

        #Go back to login
        self.show_login()

if __name__ == "__main__":
    app = GirlMath()
    app.mainloop()