import customtkinter as ctk

def create_settings_tab(parent, logout_callback, password_change_callback):
    # Use a scrollable frame so no buttons get hidden on smaller screens
    frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # --- Title ---
    ctk.CTkLabel(frame, text="Settings", font=("Cooper Black", 24), text_color="#434242").pack(pady=(10, 20))

    # --- Logout ---
    ctk.CTkButton(frame, text="logout", command=logout_callback, font=("Cooper Black", 16)).pack(pady=10)

    # Divider
    ctk.CTkFrame(frame, height=2, fg_color="#E0E0E0").pack(fill="x", padx=50, pady=20)

    # --- Change Password Section ---
    ctk.CTkLabel(frame, text="Change Passphrase", font=("Cooper Black", 18), text_color="#434242").pack(pady=5)

    # 1. Input Fields
    old_pass_entry = ctk.CTkEntry(frame, placeholder_text="Current Passphrase", show="*", width=250)
    old_pass_entry.pack(pady=5)

    new_pass_entry = ctk.CTkEntry(frame, placeholder_text="New Passphrase", show="*", width=250)
    new_pass_entry.pack(pady=5)

    confirm_pass_entry = ctk.CTkEntry(frame, placeholder_text="Confirm New Passphrase", show="*", width=250)
    confirm_pass_entry.pack(pady=5)

    # 2. Feedback Label (To show "Success" or "Error")
    feedback_label = ctk.CTkLabel(frame, text="", font=("Arial Rounded MT Bold", 12))
    feedback_label.pack(pady=5)

    # 3. The Logic (The "Checking" part)
    def attempt_change():
        old_pw = old_pass_entry.get()
        new_pw = new_pass_entry.get()
        confirm_pw = confirm_pass_entry.get()

        # Check if passwords match
        if new_pw != confirm_pw:
            feedback_label.configure(text="New passphrases do not match!", text_color="red", font=("Arial Rounded MT Bold", 14))
            return
        
        if not new_pw:
            feedback_label.configure(text="New passphrase cannot be empty!", text_color="red", font=("Arial Rounded MT Bold", 14))
            return

        # Send to girlmath.py to verify old password and save to JSON
        success, message = password_change_callback(old_pw, new_pw)
        
        if success:
            feedback_label.configure(text=message, text_color="green", font=("Arial Rounded MT Bold", 14))
            # Clear boxes after success
            old_pass_entry.delete(0, 'end')
            new_pass_entry.delete(0, 'end')
            confirm_pass_entry.delete(0, 'end')
        else:
            feedback_label.configure(text=message, text_color="red", font=("Arial Rounded MT Bold", 14))

    # 4. The Submit Button (If you don't see this, increase your window size)
    change_btn = ctk.CTkButton(frame, text="update passphrase", command=attempt_change, font=("Cooper Black", 14), fg_color="#FFB6C1", text_color="black")
    change_btn.pack(pady=20)
    
    return frame