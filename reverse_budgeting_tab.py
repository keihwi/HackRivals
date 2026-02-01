import customtkinter as ctk
import json
import os

REVERSE_EXPENSE_FILE = os.path.join(os.path.dirname(__file__), "reverse_expense_data.json")

FREQUENCY_OPTIONS = {
    "Weekly (x52)": 52,
    "Biweekly (x26)": 26,
    "Monthly (x12)": 12,
    "Quarterly (x4)": 4,
    "Yearly (x1)": 1,
}


def load_reverse_expense_data():
    if os.path.exists(REVERSE_EXPENSE_FILE):
        with open(REVERSE_EXPENSE_FILE, "r") as f:
            return json.load(f)
    return {"transactions": [], "savings_goal": 0.0}


def save_reverse_expense_data(data):
    with open(REVERSE_EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_reverse_budgeting_tab(parent):
    frame = parent

    from budgeting_tab import create_budgeting_tab

    def switch_to_budgeting():
        for widget in frame.winfo_children():
            widget.destroy()
        create_budgeting_tab(frame)

    # Switch button at bottom
    ctk.CTkButton(frame, text="← Budgeting", font=("Arial Rounded MT Bold", 14),
                  fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                  corner_radius=8, width=180,
                  command=switch_to_budgeting).pack(anchor="se", side="bottom", padx=20, pady=10)

    # Main container
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # ── LEFT CONTAINER ──
    left_container = ctk.CTkFrame(main_container, fg_color="transparent", width=400)
    left_container.pack(side="left", fill="y", padx=(0, 0))
    left_container.pack_propagate(False)

    # Annual Need Summary
    summary_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400, height=80,
                                 border_width=2, border_color="#F7DDE8")
    summary_frame.pack(anchor="nw", padx=20, pady=20)
    summary_frame.pack_propagate(False)

    ctk.CTkLabel(summary_frame, text="Annual Need",
                 font=("Cooper Black", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    summary_total_label = ctk.CTkLabel(summary_frame, text="Total: $0.00 / year",
                                       font=("Arial Rounded MT Bold", 16),
                                       text_color="black", fg_color="transparent")
    summary_total_label.pack(pady=(5, 10))

    # Savings Goal Box
    savings_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400, height=120,
                                 border_width=2, border_color="#F7DDE8")
    savings_frame.pack(anchor="nw", padx=20, pady=(0, 20))
    savings_frame.pack_propagate(False)

    ctk.CTkLabel(savings_frame, text="Savings Goal",
                 font=("Cooper Black", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    savings_input_frame = ctk.CTkFrame(savings_frame, fg_color="transparent")
    savings_input_frame.pack(padx=10, pady=5, fill="x")

    savings_entry = ctk.CTkEntry(savings_input_frame, placeholder_text="Annual savings $",
                                 font=("Arial Rounded MT Bold", 12), corner_radius=8, width=200)
    savings_entry.pack(side="left", padx=(10, 5))

    savings_display_label = ctk.CTkLabel(savings_frame, text="Savings Goal: $0.00 / year",
                                          font=("Arial Rounded MT Bold", 14), text_color="black")
    savings_display_label.pack(pady=(0, 10))

    def set_savings_goal():
        try:
            goal = float(savings_entry.get())
        except ValueError:
            return
        ed = load_reverse_expense_data()
        ed["savings_goal"] = goal
        save_reverse_expense_data(ed)
        savings_entry.delete(0, "end")
        update_all()

    ctk.CTkButton(savings_input_frame, text="Set", font=("Arial Rounded MT Bold", 13),
                  fg_color="#B8D4E3", hover_color="#9FC4D6", text_color="black",
                  corner_radius=8, width=60, command=set_savings_goal).pack(side="left", padx=5)

    # ── RIGHT CONTAINER — Expense Tracker ──
    right_container = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=15,
                                   border_width=2, border_color="#F7DDE8")
    right_container.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

    # Header row
    header_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    header_frame.pack(fill="x", padx=10, pady=(10, 5))

    ctk.CTkLabel(header_frame, text="Expense Tracker", font=("Cooper Black", 20),
                 text_color="black", fg_color="transparent").pack(side="left", padx=10)

    clear_btn = ctk.CTkButton(header_frame, text="Clear", font=("Arial Rounded MT Bold", 12),
                               fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                               corner_radius=8, width=60, command=lambda: clear_expenses())
    clear_btn.pack(side="right", padx=10)

    # Two-column grid for wants/needs
    columns_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    columns_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
    columns_frame.grid_columnconfigure(0, weight=1, uniform="col")
    columns_frame.grid_columnconfigure(1, weight=1, uniform="col")
    columns_frame.grid_rowconfigure(0, weight=1)

    # Wants column
    wants_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    wants_col.grid(row=0, column=0, sticky="nsew", padx=5)

    ctk.CTkLabel(wants_col, text="WANTS", font=("Cooper Black", 16),
                 text_color="black").pack(pady=(5, 2))

    wants_annual_label = ctk.CTkLabel(wants_col, text="Wants: $0.00/yr",
                                      font=("Arial Rounded MT Bold", 11), text_color="black")
    wants_annual_label.pack()

    wants_list = ctk.CTkScrollableFrame(wants_col, fg_color="#FFF5F9", corner_radius=8, height=200)
    wants_list.pack(fill="both", expand=True, padx=5, pady=5)

    # Needs column
    needs_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    needs_col.grid(row=0, column=1, sticky="nsew", padx=5)

    ctk.CTkLabel(needs_col, text="NEEDS", font=("Cooper Black", 16),
                 text_color="black").pack(pady=(5, 2))

    needs_annual_label = ctk.CTkLabel(needs_col, text="Needs: $0.00/yr",
                                      font=("Arial Rounded MT Bold", 11), text_color="black")
    needs_annual_label.pack()

    needs_list = ctk.CTkScrollableFrame(needs_col, fg_color="#F0FFF0", corner_radius=8, height=200)
    needs_list.pack(fill="both", expand=True, padx=5, pady=5)

    # Manual entry area
    entry_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    entry_frame.pack(fill="x", padx=15, pady=(5, 15))

    desc_entry = ctk.CTkEntry(entry_frame, placeholder_text="Description",
                              font=("Arial Rounded MT Bold", 12), corner_radius=8, width=140)
    desc_entry.pack(side="left", padx=(0, 5))

    amount_entry = ctk.CTkEntry(entry_frame, placeholder_text="Amount",
                                font=("Arial Rounded MT Bold", 12), corner_radius=8, width=80)
    amount_entry.pack(side="left", padx=(0, 5))

    freq_var = ctk.StringVar(value="Monthly (x12)")
    freq_menu = ctk.CTkOptionMenu(entry_frame, values=list(FREQUENCY_OPTIONS.keys()),
                                   variable=freq_var, font=("Arial Rounded MT Bold", 11),
                                   fg_color="#E8E8E8", button_color="#D0D0D0",
                                   button_hover_color="#C0C0C0", text_color="black",
                                   corner_radius=8, width=130)
    freq_menu.pack(side="left", padx=(0, 5))

    want_btn = ctk.CTkButton(entry_frame, text="Want", font=("Arial Rounded MT Bold", 13),
                             fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                             corner_radius=8, width=60,
                             command=lambda: add_expense("want"))
    want_btn.pack(side="left", padx=3)

    need_btn = ctk.CTkButton(entry_frame, text="Need", font=("Arial Rounded MT Bold", 13),
                             fg_color="#D5ECD4", hover_color="#BDD9BC", text_color="black",
                             corner_radius=8, width=60,
                             command=lambda: add_expense("need"))
    need_btn.pack(side="left", padx=3)

    # ── Logic ──

    def update_all():
        ed = load_reverse_expense_data()
        savings_goal = ed.get("savings_goal", 0.0)

        wants_annual = sum(t["amount"] * t.get("frequency", 1) for t in ed["transactions"] if t.get("category") == "want")
        needs_annual = sum(t["amount"] * t.get("frequency", 1) for t in ed["transactions"] if t.get("category") == "need")

        annual_need = wants_annual + needs_annual + savings_goal
        summary_total_label.configure(text=f"Total: ${annual_need:,.2f} / year")
        savings_display_label.configure(text=f"Savings Goal: ${savings_goal:,.2f} / year")
        wants_annual_label.configure(text=f"Wants: ${wants_annual:,.2f}/yr")
        needs_annual_label.configure(text=f"Needs: ${needs_annual:,.2f}/yr")

    def refresh_expense_lists():
        ed = load_reverse_expense_data()

        for widget in wants_list.winfo_children():
            widget.destroy()
        for widget in needs_list.winfo_children():
            widget.destroy()

        for t in ed["transactions"]:
            freq = t.get("frequency", 1)
            annual = t["amount"] * freq
            text = f"{t['description']} — ${t['amount']:.2f} x{freq} = ${annual:.2f}"

            if t.get("category") == "want":
                row = ctk.CTkFrame(wants_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=text, font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)
            elif t.get("category") == "need":
                row = ctk.CTkFrame(needs_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=text, font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)

    def add_expense(category):
        description = desc_entry.get().strip()
        try:
            amount = float(amount_entry.get())
        except ValueError:
            return
        if not description:
            return

        frequency = FREQUENCY_OPTIONS.get(freq_var.get(), 12)

        ed = load_reverse_expense_data()
        ed["transactions"].append({
            "description": description,
            "amount": amount,
            "frequency": frequency,
            "category": category
        })
        save_reverse_expense_data(ed)

        desc_entry.delete(0, "end")
        amount_entry.delete(0, "end")

        refresh_expense_lists()
        update_all()

    def clear_expenses():
        ed = load_reverse_expense_data()
        ed["transactions"] = []
        save_reverse_expense_data(ed)
        refresh_expense_lists()
        update_all()

    # Initialize
    update_all()
    refresh_expense_lists()

    return frame
