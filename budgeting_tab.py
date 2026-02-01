import customtkinter as ctk
import json
import os
import requests

DATA_FILE = os.path.join(os.path.dirname(__file__), "job_table.json")
EXPENSE_DATA_FILE = os.path.join(os.path.dirname(__file__), "expense_sorting_data.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"jobs": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_expense_data():
    if os.path.exists(EXPENSE_DATA_FILE):
        with open(EXPENSE_DATA_FILE, "r") as f:
            return json.load(f)
    return {"api_config": {"api_key": "", "account_id": ""}, "transactions": [], "unsorted_transactions": []}


def save_expense_data(data):
    with open(EXPENSE_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def fetch_nessie_transactions(api_key, account_id):
    url = f"http://api.nessieisreal.com/accounts/{account_id}/purchases?key={api_key}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def create_budgeting_tab(parent):
    frame = parent

    from reverse_budgeting_tab import create_reverse_budgeting_tab

    def switch_to_reverse():
        for widget in frame.winfo_children():
            widget.destroy()
        create_reverse_budgeting_tab(frame)

    # Reverse Budgeting button at the bottom
    reverse_btn = ctk.CTkButton(frame, text="Reverse Budgeting →", font=("Arial Rounded MT Bold", 14),
                  fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                  corner_radius=8, width=180,
                  command=switch_to_reverse)
    reverse_btn.pack(anchor="se", side="bottom", padx=20, pady=10)

    # Main container
    main_container = ctk.CTkFrame(frame, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # ── LEFT CONTAINER (existing widgets) ──
    left_container = ctk.CTkFrame(main_container, fg_color="transparent", width=400)
    left_container.pack(side="left", fill="y", padx=(0, 0))
    left_container.pack_propagate(False)

    # Jobs Revenue Widget
    jobs_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400,
                              border_width=2, border_color="#F7DDE8")
    jobs_frame.pack(anchor="nw", padx=20, pady=20)
    jobs_frame.pack_propagate(False)

    ctk.CTkLabel(jobs_frame, text="Jobs", font=("Cooper Black", 20),
                 text_color="black", fg_color="transparent").pack(pady=(10, 5))

    input_frame = ctk.CTkFrame(jobs_frame, fg_color="transparent")
    input_frame.pack(padx=10, pady=5, fill="x")

    name_entry = ctk.CTkEntry(input_frame, placeholder_text="Job Name",
                              font=("Arial Rounded MT Bold", 12), corner_radius=8, width=120)
    name_entry.pack(side="left", padx=(0, 5))

    monthly_entry = ctk.CTkEntry(input_frame, placeholder_text="$/month",
                                 font=("Arial Rounded MT Bold", 12), corner_radius=8, width=90)
    monthly_entry.pack(side="left", padx=(0, 5))

    add_btn = ctk.CTkButton(input_frame, text="Add", font=("Arial Rounded MT Bold", 14),
                            fg_color="#F7DDE8", hover_color="#EBC5D6",
                            text_color="black", corner_radius=8, width=60,
                            command=lambda: add_job())
    add_btn.pack(side="right")

    job_list_frame = ctk.CTkScrollableFrame(jobs_frame, fg_color="transparent", height=150)
    job_list_frame.pack(padx=10, pady=5, fill="x")

    total_label = ctk.CTkLabel(jobs_frame, text="Total Monthly Revenue: $0.00",
                               font=("Cooper Black", 14), text_color="black",
                               fg_color="transparent")
    total_label.pack(pady=(5, 10))

    # Monthly Revenue Summary
    summary_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400, height=80,
                                 border_width=2, border_color="#F7DDE8")
    summary_frame.pack(anchor="nw", padx=20, pady=(0, 20))
    summary_frame.pack_propagate(False)

    ctk.CTkLabel(summary_frame, text="Monthly Revenue Summary",
                 font=("Cooper Black", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    summary_total_label = ctk.CTkLabel(summary_frame, text="Total: $0.00",
                                       font=("Arial Rounded MT Bold", 16),
                                       text_color="black", fg_color="transparent")
    summary_total_label.pack(pady=(5, 10))

    # Savings Goal Box
    savings_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400, height=200,
                                 border_width=2, border_color="#F7DDE8")
    savings_frame.pack(anchor="nw", padx=20, pady=(0, 20))
    savings_frame.pack_propagate(False)

    ctk.CTkLabel(savings_frame, text="Savings Goal",
                 font=("Cooper Black", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    ctk.CTkLabel(savings_frame, text="Coming soon!",
                 font=("Arial Rounded MT Bold", 14), text_color="gray",
                 fg_color="transparent").pack(pady=(5, 10))

    # RIGHT CONTAINER (expense sorting)
    right_container = ctk.CTkFrame(main_container, fg_color="#FFFFFF", corner_radius=15,
                                   border_width=2, border_color="#F7DDE8")
    right_container.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

    ctk.CTkLabel(right_container, text="Expense Sorting", font=("Cooper Black", 20),
                 text_color="black", fg_color="transparent").pack(pady=(10, 5))

    # Three-column grid
    columns_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    columns_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    columns_frame.grid_columnconfigure(0, weight=1, uniform="col")
    columns_frame.grid_columnconfigure(1, weight=1, uniform="col")
    columns_frame.grid_columnconfigure(2, weight=1, uniform="col")
    columns_frame.grid_rowconfigure(0, weight=1)

    # Wants column (left)
    wants_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    wants_col.grid(row=0, column=0, sticky="nsew", padx=5)

    ctk.CTkLabel(wants_col, text="WANTS", font=("Cooper Black", 16),
                 text_color="black").pack(pady=(5, 2))

    wants_budget_label = ctk.CTkLabel(wants_col, text="Budget: $0.00",
                                      font=("Arial Rounded MT Bold", 11), text_color="black")
    wants_budget_label.pack()

    wants_progress = ctk.CTkProgressBar(wants_col, progress_color="#F7DDE8",
                                        fg_color="#E8E8E8", height=14, corner_radius=7)
    wants_progress.pack(fill="x", padx=5, pady=5)
    wants_progress.set(0)

    wants_spent_label = ctk.CTkLabel(wants_col, text="Spent: $0.00",
                                     font=("Arial Rounded MT Bold", 10), text_color="gray")
    wants_spent_label.pack()

    wants_list = ctk.CTkScrollableFrame(wants_col, fg_color="#FFF5F9", corner_radius=8, height=200)
    wants_list.pack(fill="both", expand=True, padx=5, pady=5)

    # Sorting column (center)
    sort_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    sort_col.grid(row=0, column=1, sticky="nsew", padx=5)

    ctk.CTkLabel(sort_col, text="SORTING", font=("Cooper Black", 16),
                 text_color="black").pack(pady=(5, 10))

    # API config inputs
    api_config_frame = ctk.CTkFrame(sort_col, fg_color="transparent")
    api_config_frame.pack(fill="x", padx=5, pady=(0, 5))

    ctk.CTkLabel(api_config_frame, text="GirlMath", font=("Cooper Black", 14),
                 text_color="black").pack(pady=2)

    account_id_entry = ctk.CTkEntry(api_config_frame, placeholder_text="Account ID",
                                    font=("Arial Rounded MT Bold", 10), corner_radius=8, height=28)
    account_id_entry.pack(fill="x", pady=2)

    # Display label showing masked account ID
    expense_data = load_expense_data()
    saved_account_id = expense_data["api_config"].get("account_id", "")

    def get_masked_id(full_id):
        if len(full_id) >= 4:
            return f"Account: ****{full_id[-4:]}"
        return ""

    account_display_label = ctk.CTkLabel(api_config_frame, text=get_masked_id(saved_account_id),
                                         font=("Arial Rounded MT Bold", 9), text_color="gray")
    if saved_account_id:
        account_display_label.pack(pady=(0, 2))

    # Transaction card
    card_frame = ctk.CTkFrame(sort_col, fg_color="#FFF5F9", corner_radius=12,
                              border_width=1, border_color="#F7DDE8", height=100)
    card_frame.pack(fill="x", padx=5, pady=10)
    card_frame.pack_propagate(False)

    card_desc_label = ctk.CTkLabel(card_frame, text="No transactions",
                                   font=("Arial Rounded MT Bold", 13), text_color="black",
                                   wraplength=150)
    card_desc_label.pack(pady=(15, 5))

    card_amount_label = ctk.CTkLabel(card_frame, text="",
                                     font=("Cooper Black", 16), text_color="black")
    card_amount_label.pack()

    # Sort buttons
    btn_frame = ctk.CTkFrame(sort_col, fg_color="transparent")
    btn_frame.pack(pady=5)

    want_btn = ctk.CTkButton(btn_frame, text="Want", font=("Arial Rounded MT Bold", 13),
                             fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                             corner_radius=8, width=70,
                             command=lambda: sort_transaction("want"))
    want_btn.pack(side="left", padx=5)

    need_btn = ctk.CTkButton(btn_frame, text="Need", font=("Arial Rounded MT Bold", 13),
                             fg_color="#D5ECD4", hover_color="#BDD9BC", text_color="black",
                             corner_radius=8, width=70,
                             command=lambda: sort_transaction("need"))
    need_btn.pack(side="left", padx=5)

    fetch_btn = ctk.CTkButton(sort_col, text="Fetch Transactions", font=("Arial Rounded MT Bold", 12),
                              fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                              corner_radius=8, width=140,
                              command=lambda: fetch_transactions())
    fetch_btn.pack(pady=(10, 5))

    fetch_status_label = ctk.CTkLabel(sort_col, text="", font=("Arial Rounded MT Bold", 10),
                                      text_color="gray")
    fetch_status_label.pack()

    # --- Needs column (right) ---
    needs_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    needs_col.grid(row=0, column=2, sticky="nsew", padx=5)

    ctk.CTkLabel(needs_col, text="NEEDS", font=("Cooper Black", 16),
                 text_color="black").pack(pady=(5, 2))

    needs_budget_label = ctk.CTkLabel(needs_col, text="Budget: $0.00",
                                      font=("Arial Rounded MT Bold", 11), text_color="black")
    needs_budget_label.pack()

    needs_progress = ctk.CTkProgressBar(needs_col, progress_color="#D5ECD4",
                                        fg_color="#E8E8E8", height=14, corner_radius=7)
    needs_progress.pack(fill="x", padx=5, pady=5)
    needs_progress.set(0)

    needs_spent_label = ctk.CTkLabel(needs_col, text="Spent: $0.00",
                                     font=("Arial Rounded MT Bold", 10), text_color="gray")
    needs_spent_label.pack()

    needs_list = ctk.CTkScrollableFrame(needs_col, fg_color="#F0FFF0", corner_radius=8, height=200)
    needs_list.pack(fill="both", expand=True, padx=5, pady=5)

    # ── Job data & logic ──
    data = load_data()
    jobs = data.get("jobs", [])

    def persist():
        save_data({"jobs": jobs})

    def get_total_revenue():
        return sum(job["monthly"] for job in jobs)

    def update_summary():
        total = get_total_revenue()
        summary_total_label.configure(text=f"Total: ${total:,.2f}")

    def update_total():
        total = get_total_revenue()
        total_label.configure(text=f"Total Monthly Revenue: ${total:,.2f}")
        update_summary()
        update_budgets()

    def delete_job(index):
        jobs.pop(index)
        persist()
        for widget in job_list_frame.winfo_children():
            widget.destroy()
        for i, job in enumerate(jobs):
            create_job_row(i, job)
        update_total()

    def create_job_row(index, job):
        row = ctk.CTkFrame(job_list_frame, fg_color="#FFFFFF", corner_radius=8)
        row.pack(fill="x", pady=2)

        text = f"{job['name']}  —  ${job['monthly']:,.2f}/mo"
        ctk.CTkLabel(row, text=text, font=("Arial Rounded MT Bold", 11),
                     text_color="black", fg_color="transparent").pack(side="left", padx=8, pady=4)

        del_btn = ctk.CTkButton(row, text="✕", width=28, height=28,
                                font=("Arial Rounded MT Bold", 12), fg_color="#F7DDE8",
                                hover_color="#EBC5D6", text_color="black",
                                corner_radius=8, command=lambda i=index: delete_job(i))
        del_btn.pack(side="right", padx=5, pady=4)

    def add_job():
        name = name_entry.get().strip()
        try:
            monthly = float(monthly_entry.get())
        except ValueError:
            return
        if not name:
            return

        job = {"name": name, "monthly": monthly}
        jobs.append(job)
        persist()
        create_job_row(len(jobs) - 1, job)
        update_total()

        name_entry.delete(0, "end")
        monthly_entry.delete(0, "end")

    # ── Expense sorting logic ──

    def update_budgets():
        total = get_total_revenue()
        wants_budget = total * 0.30
        needs_budget = total * 0.50
        wants_budget_label.configure(text=f"Budget: ${wants_budget:,.2f}")
        needs_budget_label.configure(text=f"Budget: ${needs_budget:,.2f}")
        update_progress_bars()

    def update_progress_bars():
        total = get_total_revenue()
        wants_budget = total * 0.30
        needs_budget = total * 0.50

        ed = load_expense_data()
        wants_spent = sum(t["amount"] for t in ed["transactions"] if t.get("category") == "want")
        needs_spent = sum(t["amount"] for t in ed["transactions"] if t.get("category") == "need")

        wants_spent_label.configure(text=f"Spent: ${wants_spent:,.2f}")
        needs_spent_label.configure(text=f"Spent: ${needs_spent:,.2f}")

        wants_progress.set(min(wants_spent / wants_budget, 1.0) if wants_budget > 0 else 0)
        needs_progress.set(min(needs_spent / needs_budget, 1.0) if needs_budget > 0 else 0)

    def refresh_sorted_lists():
        ed = load_expense_data()

        for widget in wants_list.winfo_children():
            widget.destroy()
        for widget in needs_list.winfo_children():
            widget.destroy()

        for t in ed["transactions"]:
            if t.get("category") == "want":
                row = ctk.CTkFrame(wants_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=f"{t['description']}", font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row, text=f"${t['amount']:.2f}", font=("Arial Rounded MT Bold", 10),
                             text_color="gray").pack(side="right", padx=5, pady=3)
            elif t.get("category") == "need":
                row = ctk.CTkFrame(needs_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=f"{t['description']}", font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row, text=f"${t['amount']:.2f}", font=("Arial Rounded MT Bold", 10),
                             text_color="gray").pack(side="right", padx=5, pady=3)

    def load_next_transaction():
        ed = load_expense_data()
        if ed["unsorted_transactions"]:
            t = ed["unsorted_transactions"][0]
            card_desc_label.configure(text=t["description"])
            card_amount_label.configure(text=f"${t['amount']:.2f}")
        else:
            card_desc_label.configure(text="No transactions")
            card_amount_label.configure(text="")

    def sort_transaction(category):
        ed = load_expense_data()
        if not ed["unsorted_transactions"]:
            return
        t = ed["unsorted_transactions"].pop(0)
        t["category"] = category
        t["sorted"] = True
        ed["transactions"].append(t)
        save_expense_data(ed)
        load_next_transaction()
        refresh_sorted_lists()
        update_progress_bars()

    def fetch_transactions():
        account_id = account_id_entry.get().strip()

        # Use saved values if fields are empty
        ed = load_expense_data()
        api_key = ed["api_config"].get("api_key", "")
        if not account_id:
            account_id = ed["api_config"].get("account_id", "")

        if not api_key or not account_id:
            fetch_status_label.configure(text="Enter API key & Account ID")
            return

        # Save API config
        ed["api_config"]["api_key"] = api_key
        ed["api_config"]["account_id"] = account_id

        # Update masked display and clear the entry
        account_display_label.configure(text=get_masked_id(account_id))
        account_display_label.pack(pady=(0, 2))
        account_id_entry.delete(0, "end")

        try:
            raw = fetch_nessie_transactions(api_key, account_id)
        except Exception as e:
            fetch_status_label.configure(text=f"Error: {str(e)[:40]}")
            return

        existing_ids = {t["id"] for t in ed["transactions"]}
        existing_ids.update(t["id"] for t in ed["unsorted_transactions"])

        new_count = 0
        for item in raw:
            tid = item.get("_id", "")
            if tid in existing_ids:
                continue
            t = {
                "id": tid,
                "description": item.get("description", item.get("merchant_id", "Purchase")),
                "amount": item.get("amount", 0),
                "date": item.get("purchase_date", ""),
                "category": None,
                "sorted": False,
            }
            ed["unsorted_transactions"].append(t)
            new_count += 1

        save_expense_data(ed)
        fetch_status_label.configure(text=f"Fetched {new_count} new transaction(s)")
        load_next_transaction()

    # Initialize existing jobs
    for i, job in enumerate(jobs):
        create_job_row(i, job)
    update_total()

    # Initialize expense sorting UI
    refresh_sorted_lists()
    load_next_transaction()

    return frame
