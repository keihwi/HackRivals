import customtkinter as ctk
from google import genai
from google.genai import types

# 1. Initialize Client with v1 forcing
# This usually bypasses the "v1beta not found" error
client = genai.Client(
    api_key="AIzaSyA6fdln8XzVq4dl-w6-38xZm6yrsFeWIEY",
    http_options={'api_version': 'v1'}
)

def create_chatbot_tab(parent):
    frame = parent
    
    chat_display = ctk.CTkTextbox(frame, state="disabled", wrap="word", corner_radius=10)
    chat_display.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="x", padx=10, pady=(0, 10))

    user_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask GirlMath anything...")
    user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def update_chat(message):
        chat_display.configure(state="normal")
        chat_display.insert("end", message + "\n\n")
        chat_display.configure(state="disabled")
        chat_display.see("end")

    def send_message():
        user_text = user_entry.get()
        if not user_text.strip():
            return

        # 1. Update the chat with your message ONLY ONCE
        update_chat("You: " + user_text)
        user_entry.delete(0, "end")

        try:
            # 2. Try the best model your key showed support for
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=user_text
            )
            update_chat("GirlMathBot: " + response.text)
            
        except Exception as e:
            # 3. If 2.5 fails, try 2.0
            print(f"Gemini 2.5 failed, trying 2.0...")
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=user_text
                )
                update_chat("GirlMathBot: " + response.text)
            except Exception as final_e:
                # 4. Final safety net: list authorized models if everything fails
                print(f"DEBUG: {final_e}")
                try:
                    authorized_models = [m.name for m in client.models.list()]
                    print(f"Supported models: {authorized_models}")
                    update_chat("Error: All models failed. See terminal for available models.")
                except:
                    update_chat("Error: Connection failed. Check your API key.")

    send_btn = ctk.CTkButton(input_frame, text="Send", width=80, command=send_message)
    send_btn.pack(side="right")
    
    user_entry.bind("<Return>", lambda event: send_message())

    return frame