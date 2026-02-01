import customtkinter as ctk
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "job_table.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"jobs": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_budgeting_tab(parent):
    frame = parent

    # Jobs Revenue Widget
    jobs_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF", corner_radius=15, width=400,
                              border_width=2, border_color="#F7DDE8")
    jobs_frame.pack(anchor="nw", padx=20, pady=20)
    jobs_frame.pack_propagate(False)

    # Title
    ctk.CTkLabel(jobs_frame, text="Jobs", font=("Bauhaus 93", 20),
                 text_color="black", fg_color="transparent").pack(pady=(10, 5))

    # Input row
    input_frame = ctk.CTkFrame(jobs_frame, fg_color="transparent")
    input_frame.pack(padx=10, pady=5, fill="x")

    name_entry = ctk.CTkEntry(input_frame, placeholder_text="Job Name",
                              font=("Arial Rounded MT Bold", 12), corner_radius=8, width=120)
    name_entry.pack(side="left", padx=(0, 5))

    rate_entry = ctk.CTkEntry(input_frame, placeholder_text="$/hr",
                              font=("Arial Rounded MT Bold", 12), corner_radius=8, width=70)
    rate_entry.pack(side="left", padx=(0, 5))

    hours_entry = ctk.CTkEntry(input_frame, placeholder_text="hrs/wk",
                               font=("Arial Rounded MT Bold", 12), corner_radius=8, width=70)
    hours_entry.pack(side="left", padx=(0, 5))

    add_btn = ctk.CTkButton(input_frame, text="Add", font=("Arial Rounded MT Bold", 14),
                            fg_color="#F7DDE8", hover_color="#EBC5D6",
                            text_color="black", corner_radius=8, width=60,
                            command=lambda: add_job())
    add_btn.pack(side="left")

    # Scrollable job list
    job_list_frame = ctk.CTkScrollableFrame(jobs_frame, fg_color="transparent",
                                            height=150)
    job_list_frame.pack(padx=10, pady=5, fill="x")

    # Total label inside jobs widget
    total_label = ctk.CTkLabel(jobs_frame, text="Total Monthly Revenue: $0.00",
                               font=("Bauhaus 93", 14), text_color="black",
                               fg_color="transparent")
    total_label.pack(pady=(5, 10))

    # Monthly Revenue Summary
    summary_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF", corner_radius=15, width=400, height=80,
                                 border_width=2, border_color="#F7DDE8")
    summary_frame.pack(anchor="nw", padx=20, pady=(0, 20))
    summary_frame.pack_propagate(False)

    ctk.CTkLabel(summary_frame, text="Monthly Revenue Summary",
                 font=("Bauhaus 93", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    summary_total_label = ctk.CTkLabel(summary_frame, text="Total: $0.00",
                                       font=("Arial Rounded MT Bold", 16),
                                       text_color="black", fg_color="transparent")
    summary_total_label.pack(pady=(5, 10))

    # Savings Goal Box
    savings_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF", corner_radius=15, width=400, height=200,
                                 border_width=2, border_color="#F7DDE8")
    savings_frame.pack(anchor="nw", padx=20, pady=(0, 20))
    savings_frame.pack_propagate(False)

    ctk.CTkLabel(savings_frame, text="Savings Goal",
                 font=("Bauhaus 93", 20), text_color="black",
                 fg_color="transparent").pack(pady=(10, 5))

    ctk.CTkLabel(savings_frame, text="Coming soon!",
                 font=("Arial Rounded MT Bold", 14), text_color="gray",
                 fg_color="transparent").pack(pady=(5, 10))

    # Job data storage
    data = load_data()
    jobs = data.get("jobs", [])

    def persist():
        save_data({"jobs": jobs})

    def update_summary():
        total = sum(job["monthly"] for job in jobs)
        summary_total_label.configure(text=f"Total: ${total:,.2f}")

    def update_total():
        total = sum(job["monthly"] for job in jobs)
        total_label.configure(text=f"Total Monthly Revenue: ${total:,.2f}")
        update_summary()

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

        text = f"{job['name']}  —  ${job['rate']:.2f}/hr  ×  {job['hours']:.1f} hrs/wk  =  ${job['monthly']:,.2f}/mo"
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
            rate = float(rate_entry.get())
            hours = float(hours_entry.get())
        except ValueError:
            return
        if not name:
            return

        monthly = rate * hours * 4
        job = {"name": name, "rate": rate, "hours": hours, "monthly": monthly}
        jobs.append(job)
        persist()
        create_job_row(len(jobs) - 1, job)
        update_total()

        name_entry.delete(0, "end")
        rate_entry.delete(0, "end")
        hours_entry.delete(0, "end")

    # Load existing jobs into UI
    for i, job in enumerate(jobs):
        create_job_row(i, job)
    update_total()

    return frame
