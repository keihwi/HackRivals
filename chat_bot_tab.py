import threading # Required for the loading symbol logic
import customtkinter as ctk
from google import genai
from google.genai import types

# 1. Initialize Client with v1beta
# System instructions are much more stable on v1beta
client = genai.Client(
    api_key="CHANGE",
    http_options={'api_version': 'v1beta'}
)

def create_chatbot_tab(parent):
    frame = parent
    finance_system_instruction = """
    ROLE: You are a "GirlMathBot" & Personal Finance Expert. 
    OBJECTIVE: Help the user rationalize their spending with fun 'GirlMath' logic, 
    but ALWAYS follow up with a 'RealMath' reality check.
    CONSTRAINTS: Stay witty, use bullet points, and always add a RealMath disclaimer.
    """

    chat_display = ctk.CTkTextbox(frame, state="disabled", wrap="word", corner_radius=10)
    chat_display.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=10, pady=(0, 10))

    user_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask GirlMath Anything...")
    user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def update_chat(sender, message):
        chat_display.configure(state="normal")
        chat_display.insert("end", f"{sender}: {message}\n\n")
        chat_display.configure(state="disabled")
        chat_display.see("end")

    def send_message():
        user_text = user_entry.get()
        if not user_text.strip():
            return

        update_chat("You", user_text)
        user_entry.delete(0, "end")
        
        # Add the Loading Symbol/Text
        update_chat("GirlMathBot", "Thinking... 💭")

        # Run API call in a separate thread so the GUI doesn't freeze
        def fetch_ai_response():
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    config=types.GenerateContentConfig(
                        system_instruction=finance_system_instruction,
                        temperature=0.7,
                    ),
                    contents=user_text
                )
                final_text = response.text
            except Exception as e:
                final_text = f"Error: {str(e)}"

            # Remove the "Thinking..." line and post real response
            frame.after(0, lambda: finalize_chat(final_text))

        def finalize_chat(text):
            chat_display.configure(state="normal")
            # Deletes the "Thinking..." message (last 2 lines)
            chat_display.delete("end-3l", "end") 
            chat_display.configure(state="disabled")
            update_chat("GirlMathBot", text)

        threading.Thread(target=fetch_ai_response, daemon=True).start()

    # Initial Welcome
    update_chat("GirlMathBot", "Hi! I'm your financial bestie. What are we spending on today?")

    send_btn = ctk.CTkButton(input_frame, text="Send", width=80, command=send_message)
    send_btn.pack(side="right")
    user_entry.bind("<Return>", lambda event: send_message())

    return frame