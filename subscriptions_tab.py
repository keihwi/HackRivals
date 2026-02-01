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

def get_next_payment_date(sub):
    """
    Parses '15th', '5', etc. and calculates the next specific calendar date.
    Returns datetime.max if no number is found, putting it at the bottom of the list.
    """
    date_str = sub.get('date', '')
    
    # Extract digits (e.g. "15th" -> 15)
    digits = ''.join(filter(str.isdigit, date_str))
    
    if not digits:
        return datetime.max

    day = int(digits)
    # Basic clamping if user entered 99
    if day > 31: day = 31 
    if day < 1: day = 1
    
    now = datetime.now()
    candidate_year = now.year
    candidate_month = now.month

    # If the day has already passed this month, move to next month
    if day < now.day:
        candidate_month += 1

    # Find the next valid date (handle month rollover and short months)
    while True:
        if candidate_month > 12:
            candidate_month = 1
            candidate_year += 1
            
        try:
            return datetime(candidate_year, candidate_month, day)
        except ValueError:
            # If day is invalid for this month (e.g. Feb 30), bump to next month
            candidate_month += 1

def create_subscriptions_tab(parent):
    # Main container for this tab
    main_container = ctk.CTkFrame(parent, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # Internal Navigation (The 3 Pages)
    sub_tabs = ctk.CTkTabview(main_container)
    sub_tabs.pack(fill="both", expand=True, padx=10, pady=10)
    sub_tabs._segmented_button.configure(font=("Cooper Black", 16))
    
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

        # Create a sorted copy for the "Upcoming" section
        sorted_subs = sorted(subs, key=get_next_payment_date)

        # Main Spending Display
        info_box = ctk.CTkFrame(frame, corner_radius=20, border_width=2)
        info_box.pack(fill="x", pady=10, padx=20)

        ctk.CTkLabel(info_box, text=f"${monthly_total:,.2f}", font=("Cooper Black", 50)).pack(pady=(20, 0))
        ctk.CTkLabel(info_box, text="MONTHLY SPENDING", font=("Cooper Black", 14)).pack()

        split_frame = ctk.CTkFrame(info_box, fg_color="transparent")
        split_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(split_frame, text=f"ANNUAL: ${annual_total:,.2f}", font=("Cooper Black", 16)).pack(side="left", expand=True)
        ctk.CTkLabel(split_frame, text=f"SUBSCRIPTIONS: {len(subs)}", font=("Cooper Black", 16)).pack(side="left", expand=True)

        # Scrollable list for records
        content_scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        content_scroll.pack(fill="both", expand=True, padx=20)

        # --- UPCOMING PAYMENTS SECTION ---
        ctk.CTkLabel(content_scroll, text="UPCOMING PAYMENTS", font=("Cooper Black", 20)).pack(anchor="w", pady=(10, 5))
        
        upcoming_count = 0
        for s in sorted_subs:
            if upcoming_count >= 3: break
            
            # Only show if there is a digit in the date string
            if any(char.isdigit() for char in s.get('date', '')):
                ctk.CTkLabel(content_scroll, 
                             text=f"• {s['name']} - Due: {s['date']}", 
                             font=("Arial Rounded MT Bold", 12)).pack(anchor="w", padx=15)
                upcoming_count += 1
        
        if upcoming_count == 0:
            ctk.CTkLabel(content_scroll, text="No immediate upcoming dates found.", font=("Arial", 12, "italic"), text_color="gray").pack(anchor="w", padx=15)

        # --- ALL SUBSCRIPTIONS SECTION ---
        ctk.CTkLabel(content_scroll, text="ALL SUBSCRIPTIONS", font=("Cooper Black", 20)).pack(anchor="w", pady=(20, 5))
        
        # We use the original 'subs' list here so indices match for the Delete button
        for i, s in enumerate(subs):
            item = ctk.CTkFrame(content_scroll, height=50, corner_radius=10)
            item.pack(fill="x", pady=3, padx=5)
            
            ctk.CTkLabel(item, text=f"{s['name']}", font=("Arial Rounded MT Bold", 13)).pack(side="left", padx=(15, 5))
            ctk.CTkLabel(item, text=f"({s['category']})", font=("Arial Rounded MT Bold", 11), text_color="gray").pack(side="left")

            # The Delete Button
            del_btn = ctk.CTkButton(item, text="✕", width=28, height=28, 
                                    fg_color="#F7DDE8", hover_color="#EBC5D6",
                                    font=("Arial Rounded MT Bold", 12),
                                    command=lambda idx=i: delete_subscription(idx))
            del_btn.pack(side="right", padx=10)

            ctk.CTkLabel(item, text=f"${float(s['cost']):,.2f}/mo", font=("Arial Rounded MT Bold", 13, "bold")).pack(side="right", padx=10)

    def delete_subscription(index):
        subs = load_subs()
        if 0 <= index < len(subs):
            subs.pop(index)
            save_subs(subs)
            refresh_all()

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

        date_dialog = ctk.CTkInputDialog(text="Payment Date (e.g. 15th):", title="Date")
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
            font=("Cooper Black", 15), 
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
            ctk.CTkLabel(frame, text="NO DATA TO ANALYZE", font=("Cooper Black", 20)).pack(pady=100)
            return

        # Prepare Categorical Totals
        cat_data = {}
        for s in subs:
            c = s['category']
            yearly = float(s['cost']) * 12
            cat_data[c] = cat_data.get(c, 0) + yearly

        # Matplotlib Pie Chart
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#F2F1ED') 
        
        colors = ['#FFB6C1', '#ADD8E6', '#90EE90', '#F0E68C', '#E6E6FA', '#FFDAB9', '#AFEEEE', '#D3D3D3']
        
        # Create pie chart and unpack the return values to style them
        wedges, texts, autotexts = ax.pie(
            cat_data.values(), 
            labels=cat_data.keys(), 
            autopct='%1.1f%%', 
            startangle=140,
            colors=colors,
            # This sets the props for the Category Labels (outside the pie)
            textprops={'fontname': 'Arial Rounded MT Bold', 'color': '#434242', 'size' : 14}
        )
        
        # Explicitly set style for the Percentages (inside the pie)
        plt.setp(autotexts, size=14, weight="bold", color="#434242", family="Arial Rounded MT Bold")

        ax.set_title("YEARLY SPENDING BY CATEGORY", fontdict={'family': 'Cooper Black', 'size': 18, 'color':'#434242'})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Bottom Key
        key_scroll = ctk.CTkScrollableFrame(frame, height=100, orientation="horizontal")
        key_scroll.pack(fill="x", padx=20, pady=10)
        
        for cat, total in cat_data.items():
            ctk.CTkLabel(
                key_scroll, 
                text=f" [{cat}: ${total:,.2f}/yr] ", 
                font=("Arial Rounded MT Bold", 14),
                text_color="#434242"
            ).pack(side="left", padx=10)

    # Initial Render
    refresh_all()
    return main_container