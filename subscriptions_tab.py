import customtkinter as ctk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "subscriptions_data.json"

# --- Data Helpers ---
def load_subs():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_subs(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def create_subscriptions_tab(parent):
    # Main container for this tab
    main_container = ctk.CTkFrame(parent, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # Internal Navigation (The 3 Pages)
    # Fixed: Removed segmented_button_fg_color="transparent" to prevent ValueError
    sub_tabs = ctk.CTkTabview(main_container)
    sub_tabs.pack(fill="both", expand=True, padx=10, pady=10)
    sub_tabs._segmented_button.configure(font=("Bauhaus 93", 16))
    
    tab_home = sub_tabs.add("Home")
    tab_categories = sub_tabs.add("Categories")
    tab_stats = sub_tabs.add("Statistics")

    def refresh_all():
        """Redraws the Home and Stats views whenever data changes"""
        render_home(tab_home)
        render_stats(tab_stats)

    # --- PAGE 1: HOME ---
    def render_home(frame):
        for widget in frame.winfo_children():
            widget.destroy()

        subs = load_subs()
        monthly_total = sum(float(s.get('cost', 0)) for s in subs)
        annual_total = monthly_total * 12

        # Main Spending Display
        info_box = ctk.CTkFrame(frame, corner_radius=20, border_width=2)
        info_box.pack(fill="x", pady=10, padx=20)

        ctk.CTkLabel(info_box, text=f"${monthly_total:,.2f}", font=("Bauhaus 93", 50)).pack(pady=(20, 0))
        ctk.CTkLabel(info_box, text="MONTHLY SPENDING", font=("Bauhaus 93", 14)).pack()

        split_frame = ctk.CTkFrame(info_box, fg_color="transparent")
        split_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(split_frame, text=f"ANNUAL: ${annual_total:,.2f}", font=("Bauhaus 93", 16)).pack(side="left", expand=True)
        ctk.CTkLabel(split_frame, text=f"SUBSCRIPTIONS: {len(subs)}", font=("Bauhaus 93", 16)).pack(side="left", expand=True)

        # Scrollable list for records
        content_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        content_scroll.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(content_scroll, text="UPCOMING RENEWALS", font=("Bauhaus 93", 20)).pack(anchor="w", pady=(10, 5))
        # Simple display of the last 3 entries
        for s in subs[-3:]:
            ctk.CTkLabel(content_scroll, text=f"• {s['name']} - Renewal: {s['date']}", font=("Arial", 12)).pack(anchor="w", padx=15)

        ctk.CTkLabel(content_scroll, text="ALL SUBSCRIPTIONS", font=("Bauhaus 93", 20)).pack(anchor="w", pady=(20, 5))
        for s in subs:
            item = ctk.CTkFrame(content_scroll, height=40, corner_radius=10)
            item.pack(fill="x", pady=3, padx=5)
            ctk.CTkLabel(item, text=f"{s['name']}", font=("Arial", 13, "bold")).pack(side="left", padx=15)
            ctk.CTkLabel(item, text=f"{s['category']}", font=("Arial", 11), text_color="gray").pack(side="left")
            ctk.CTkLabel(item, text=f"${s['cost']}/mo", font=("Arial", 13, "bold")).pack(side="right", padx=15)

    # --- PAGE 2: CATEGORIES ---
    def add_sub_logic(cat):
        # Dialogs to capture data
        name_dialog = ctk.CTkInputDialog(text=f"Enter name for {cat}:", title="Subscription Name")
        name = name_dialog.get_input()
        if not name: return

        cost_dialog = ctk.CTkInputDialog(text="Monthly Cost (numerical):", title="Cost")
        cost_input = cost_dialog.get_input()
        try:
            cost = float(cost_input) if cost_input else 0.0
        except ValueError:
            cost = 0.0

        date_dialog = ctk.CTkInputDialog(text="Renewal Date (e.g. 15th):", title="Date")
        date = date_dialog.get_input() or "Monthly"

        current_subs = load_subs()
        current_subs.append({
            "name": name.upper(),
            "category": cat,
            "cost": cost,
            "date": date
        })
        save_subs(current_subs)
        refresh_all()

    # Category Grid Styling
    categories = ["Entertainment", "Productivity", "Lifestyle", "Utilities", "Finance", "Health", "Gaming", "Other"]
    cat_container = ctk.CTkFrame(tab_categories, fg_color="transparent")
    cat_container.pack(expand=True, pady=20)

    for i, cat in enumerate(categories):
        btn = ctk.CTkButton(
            cat_container, 
            text=cat.upper(), 
            font=("Bauhaus 93", 15), 
            width=170, 
            height=90, 
            corner_radius=15,
            border_width=2,
            command=lambda c=cat: add_sub_logic(c)
        )
        btn.grid(row=i//3, column=i%3, padx=15, pady=15)

    # --- PAGE 3: STATISTICS ---
    def render_stats(frame):
        for widget in frame.winfo_children():
            widget.destroy()
            
        plt.close('all')

        subs = load_subs()
        if not subs:
            ctk.CTkLabel(frame, text="NO DATA TO ANALYZE", font=("Bauhaus 93", 20)).pack(pady=100)
            return

        # Prepare Categorical Totals
        cat_data = {}
        for s in subs:
            c = s['category']
            yearly = float(s['cost']) * 12
            cat_data[c] = cat_data.get(c, 0) + yearly

        # Matplotlib Pie Chart
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        # Using a soft background color to blend with the app
        fig.patch.set_facecolor('#F2F1ED') 
        
        colors = ['#FFB6C1', '#ADD8E6', '#90EE90', '#F0E68C', '#E6E6FA', '#FFDAB9', '#AFEEEE', '#D3D3D3']
        
        wedges, texts, autotexts = ax.pie(
            cat_data.values(), 
            labels=cat_data.keys(), 
            autopct='%1.1f%%', 
            startangle=140,
            colors=colors,
            textprops={'fontname': 'Arial', 'weight': 'bold'}
        )
        ax.set_title("YEARLY SPENDING BY CATEGORY", fontdict={'family': 'Bauhaus 93', 'size': 18})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Bottom Key
        key_scroll = ctk.CTkScrollableFrame(frame, height=100, orientation="horizontal")
        key_scroll.pack(fill="x", padx=20, pady=10)
        
        for cat, total in cat_data.items():
            ctk.CTkLabel(key_scroll, text=f" [{cat}: ${total:,.2f}/yr] ", font=("Arial", 12, "bold")).pack(side="left", padx=10)

    # Initial Render
    refresh_all()
    return main_container