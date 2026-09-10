from pywinauto import Desktop
from lng import run_agent
import time
import keyboard
import pyperclip
notepad = Desktop(backend="uia").window(
    title_re=".*Notepad.*"
)

editor = notepad.child_window(
    control_type="Document"
)
editor.click_input()
editor.type_keys("You: ")

last_text = ""

while True:
    keyboard.wait("ctrl+enter")
    text = editor.window_text()

    if text.startswith("You:"):

        user_input = text[4:].strip()

        if user_input and user_input != last_text:

            last_text = user_input

            print("USER:", user_input)

            response = run_agent(user_input)

            print("COSMICON:", response)

            new_text = (
                f"You: {user_input}\n\n"
                f"Cosmicon: {response}\n\n"
                f"You: "
            )

            editor.click_input()
            editor.type_keys("^a")
            pyperclip.copy(new_text)
            editor.type_keys("^v")


    time.sleep(1)