import customtkinter as ctk


def create_reverse_budgeting_tab(parent):
    frame = parent

    # Budgeting toggle button
    from budgeting_tab import create_budgeting_tab

    def switch_to_budgeting():
        for widget in frame.winfo_children():
            widget.destroy()
        create_budgeting_tab(frame)

    ctk.CTkButton(frame, text="← Budgeting", font=("Arial Rounded MT Bold", 14),
                  fg_color="#F7DDE8", hover_color="#EBC5D6", text_color="black",
                  corner_radius=8, width=180,
                  command=switch_to_budgeting).pack(anchor="se", side="bottom", padx=20, pady=10)

    # Reverse Budgeting content
    ctk.CTkLabel(frame, text="Reverse Budgeting", font=("Bauhaus 93", 24),
                 text_color="black", fg_color="transparent").pack(pady=(20, 10))

    ctk.CTkLabel(frame, text="Coming soon!",
                 font=("Arial Rounded MT Bold", 14), text_color="gray",
                 fg_color="transparent").pack(pady=(5, 10))

    return frame
