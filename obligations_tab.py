import customtkinter as ctk
import json
import os

# Define the file name for saving data
DATA_FILE = "obligations_data.json"

def save_obligations(cs_date_entry, cs_notes_box, ss_date_entry, ss_notes_box):
    """Gathers text from widgets and saves to a JSON file."""
    data = {
        "child_support_date": cs_date_entry.get(),
        "child_support_notes": cs_notes_box.get("0.0", "end-1c"), # "end-1c" avoids adding an extra newline
        "spousal_support_date": ss_date_entry.get(),
        "spousal_support_notes": ss_notes_box.get("0.0", "end-1c")
    }
    
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
        # Optional: You could add a small popup here saying "Saved!"
    except Exception as e:
        print(f"Error saving data: {e}")

def load_obligations(cs_date_entry, cs_notes_box, ss_date_entry, ss_notes_box):
    """Checks if data file exists and populates widgets."""
    if not os.path.exists(DATA_FILE):
        return # No file to load
    
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            
        # Clear existing text and insert saved data
        # Child Support
        cs_date_entry.delete(0, "end")
        cs_date_entry.insert(0, data.get("child_support_date", ""))
        
        cs_notes_box.delete("0.0", "end")
        cs_notes_box.insert("0.0", data.get("child_support_notes", ""))
        
        # Spousal Support
        ss_date_entry.delete(0, "end")
        ss_date_entry.insert(0, data.get("spousal_support_date", ""))
        
        ss_notes_box.delete("0.0", "end")
        ss_notes_box.insert("0.0", data.get("spousal_support_notes", ""))
        
    except Exception as e:
        print(f"Error loading data: {e}")

def create_obligations_tab(parent):
    # 1. Scrollable Frame container
    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Main Title
    label = ctk.CTkLabel(scroll_frame, text="Obligations Diary", font=("Bauhaus 93", 26))
    label.pack(pady=(10, 20))

    warning_label = ctk.CTkLabel(
        scroll_frame, 
        text="WARNING: Save your changes at the bottom of the page before exiting.", 
        font=("Arial Rounded MT Bold", 12),
        text_color=("gray60", "gray80") # (Light mode color, Dark mode color)
    )
    warning_label.pack(pady=(0, 5))

    # --- Helper Function for UI ---
    def create_support_section(title, parent_frame):
        section_frame = ctk.CTkFrame(parent_frame)
        section_frame.pack(fill="x", pady=10, padx=5)

        header = ctk.CTkLabel(section_frame, text=title, font=("Bauhaus 93", 20))
        header.pack(pady=(10, 5), anchor="w", padx=10)

        # Date Row
        date_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=10, pady=5)
        
        date_label = ctk.CTkLabel(date_frame, text="Next Due Date:", font=("Arial Rounded MT Bold", 14))
        date_label.pack(side="left")
        
        date_entry = ctk.CTkEntry(date_frame, placeholder_text="e.g., 1st of every month", font=("Arial Rounded MT Bold", 12))
        date_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Notes Area
        notes_label = ctk.CTkLabel(section_frame, text="Payment Log & Notes:", font=("Arial Rounded MT Bold", 14))
        notes_label.pack(anchor="w", padx=10, pady=(10, 0))

        notes_box = ctk.CTkTextbox(section_frame, height=150, font=("Arial Rounded MT Bold", 12))
        notes_box.pack(fill="x", padx=10, pady=(5, 15))

        return date_entry, notes_box

    # 2. Create Sections
    cs_date, cs_notes = create_support_section("Child Support", scroll_frame)
    ss_date, ss_notes = create_support_section("Spousal Support", scroll_frame)

    # 3. Create Save Button
    # We use a lambda to pass the specific widgets to our save function
    save_btn = ctk.CTkButton(
        scroll_frame, 
        text="Save Changes", 
        width=200,
        height=40,
        font=("Arial Rounded MT Bold", 16, "bold"),
        command=lambda: save_obligations(cs_date, cs_notes, ss_date, ss_notes)
    )
    save_btn.pack(pady=30, padx=5)

    # 4. Load Data Immediately
    load_obligations(cs_date, cs_notes, ss_date, ss_notes)

    return parent