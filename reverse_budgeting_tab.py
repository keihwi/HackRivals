import customtkinter as ctk
import json
import os

ORIGINAL_JOB_FILE = os.path.join(os.path.dirname(__file__), "job_table.json")
REVERSE_JOB_FILE = os.path.join(os.path.dirname(__file__), "reverse_job_table.json")
REVERSE_EXPENSE_FILE = os.path.join(os.path.dirname(__file__), "reverse_expense_data.json")


def load_data():
    if os.path.exists(REVERSE_JOB_FILE):
        with open(REVERSE_JOB_FILE, "r") as f:
            return json.load(f)
    # Seed from job_table.json on first use
    if os.path.exists(ORIGINAL_JOB_FILE):
        with open(ORIGINAL_JOB_FILE, "r") as f:
            data = json.load(f)
        save_data(data)
        return data
    return {"jobs": []}


def save_data(data):
    with open(REVERSE_JOB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_reverse_expense_data():
    if os.path.exists(REVERSE_EXPENSE_FILE):
        with open(REVERSE_EXPENSE_FILE, "r") as f:
            return json.load(f)
    return {"transactions": []}


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

    # Jobs Revenue Widget
    jobs_frame = ctk.CTkFrame(left_container, fg_color="#FFFFFF", corner_radius=15, width=400,
                              border_width=2, border_color="#F7DDE8")
    jobs_frame.pack(anchor="nw", padx=20, pady=20)
    jobs_frame.pack_propagate(False)

    jobs_header = ctk.CTkFrame(jobs_frame, fg_color="transparent")
    jobs_header.pack(fill="x", padx=10, pady=(10, 5))

    ctk.CTkLabel(jobs_header, text="Jobs", font=("Cooper Black", 20),
                 text_color="black", fg_color="transparent").pack(side="left", padx=(5, 0))

    def undo_jobs():
        if os.path.exists(ORIGINAL_JOB_FILE):
            with open(ORIGINAL_JOB_FILE, "r") as f:
                original = json.load(f)
        else:
            original = {"jobs": []}
        save_data(original)
        jobs.clear()
        jobs.extend(original.get("jobs", []))
        for widget in job_list_frame.winfo_children():
            widget.destroy()
        for i, job in enumerate(jobs):
            create_job_row(i, job)
        update_total()

    ctk.CTkButton(jobs_header, text="Undo", font=("Arial Rounded MT Bold", 12),
                  fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                  corner_radius=8, width=60, command=undo_jobs).pack(side="right", padx=(0, 5))

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

    savings_budget_label = ctk.CTkLabel(savings_frame, text="Budget: $0.00",
                                        font=("Arial Rounded MT Bold", 11), text_color="black")
    savings_budget_label.pack()

    savings_progress = ctk.CTkProgressBar(savings_frame, progress_color="#B8D4E3",
                                          fg_color="#E8E8E8", height=14, corner_radius=7)
    savings_progress.pack(fill="x", padx=20, pady=5)
    savings_progress.set(1.0)

    savings_remaining_label = ctk.CTkLabel(savings_frame, text="Remaining: $0.00",
                                           font=("Arial Rounded MT Bold", 10), text_color="gray")
    savings_remaining_label.pack(pady=(0, 10))

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

    # Needs column
    needs_col = ctk.CTkFrame(columns_frame, fg_color="transparent")
    needs_col.grid(row=0, column=1, sticky="nsew", padx=5)

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

    # Manual entry area
    entry_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    entry_frame.pack(fill="x", padx=15, pady=(5, 15))

    desc_entry = ctk.CTkEntry(entry_frame, placeholder_text="Description",
                              font=("Arial Rounded MT Bold", 12), corner_radius=8, width=160)
    desc_entry.pack(side="left", padx=(0, 5))

    amount_entry = ctk.CTkEntry(entry_frame, placeholder_text="Amount",
                                font=("Arial Rounded MT Bold", 12), corner_radius=8, width=90)
    amount_entry.pack(side="left", padx=(0, 5))

    want_btn = ctk.CTkButton(entry_frame, text="Want", font=("Arial Rounded MT Bold", 13),
                             fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                             corner_radius=8, width=70,
                             command=lambda: add_expense("want"))
    want_btn.pack(side="left", padx=5)

    need_btn = ctk.CTkButton(entry_frame, text="Need", font=("Arial Rounded MT Bold", 13),
                             fg_color="#D5ECD4", hover_color="#BDD9BC", text_color="black",
                             corner_radius=8, width=70,
                             command=lambda: add_expense("need"))
    need_btn.pack(side="left", padx=5)

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

    # ── Expense logic ──

    def update_budgets():
        total = get_total_revenue()
        wants_budget = total * 0.30
        needs_budget = total * 0.50
        savings_budget = total * 0.20
        wants_budget_label.configure(text=f"Budget: ${wants_budget:,.2f}")
        needs_budget_label.configure(text=f"Budget: ${needs_budget:,.2f}")
        savings_budget_label.configure(text=f"Budget: ${savings_budget:,.2f}")
        update_progress_bars()

    def update_progress_bars():
        total = get_total_revenue()
        wants_budget = total * 0.30
        needs_budget = total * 0.50

        ed = load_reverse_expense_data()
        wants_spent = sum(t["amount"] for t in ed["transactions"] if t.get("category") == "want")
        needs_spent = sum(t["amount"] for t in ed["transactions"] if t.get("category") == "need")

        wants_spent_label.configure(text=f"Spent: ${wants_spent:,.2f}")
        needs_spent_label.configure(text=f"Spent: ${needs_spent:,.2f}")

        wants_progress.set(min(wants_spent / wants_budget, 1.0) if wants_budget > 0 else 0)
        needs_progress.set(min(needs_spent / needs_budget, 1.0) if needs_budget > 0 else 0)

        savings_budget = total * 0.20
        wants_overflow = max(0, wants_spent - wants_budget)
        needs_overflow = max(0, needs_spent - needs_budget)
        savings_remaining = max(0, savings_budget - wants_overflow - needs_overflow)
        savings_progress.set(savings_remaining / savings_budget if savings_budget > 0 else 1.0)
        savings_remaining_label.configure(text=f"Remaining: ${savings_remaining:,.2f}")

    def refresh_expense_lists():
        ed = load_reverse_expense_data()

        for widget in wants_list.winfo_children():
            widget.destroy()
        for widget in needs_list.winfo_children():
            widget.destroy()

        for t in ed["transactions"]:
            if t.get("category") == "want":
                row = ctk.CTkFrame(wants_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=t["description"], font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row, text=f"${t['amount']:.2f}", font=("Arial Rounded MT Bold", 10),
                             text_color="gray").pack(side="right", padx=5, pady=3)
            elif t.get("category") == "need":
                row = ctk.CTkFrame(needs_list, fg_color="#FFFFFF", corner_radius=6)
                row.pack(fill="x", pady=2, padx=2)
                ctk.CTkLabel(row, text=t["description"], font=("Arial Rounded MT Bold", 10),
                             text_color="black").pack(side="left", padx=5, pady=3)
                ctk.CTkLabel(row, text=f"${t['amount']:.2f}", font=("Arial Rounded MT Bold", 10),
                             text_color="gray").pack(side="right", padx=5, pady=3)

    def add_expense(category):
        description = desc_entry.get().strip()
        try:
            amount = float(amount_entry.get())
        except ValueError:
            return
        if not description:
            return

        ed = load_reverse_expense_data()
        ed["transactions"].append({
            "description": description,
            "amount": amount,
            "category": category
        })
        save_reverse_expense_data(ed)

        desc_entry.delete(0, "end")
        amount_entry.delete(0, "end")

        refresh_expense_lists()
        update_progress_bars()

    def clear_expenses():
        save_reverse_expense_data({"transactions": []})
        refresh_expense_lists()
        update_progress_bars()

    # Initialize
    for i, job in enumerate(jobs):
        create_job_row(i, job)
    update_total()
    refresh_expense_lists()

    return frame
