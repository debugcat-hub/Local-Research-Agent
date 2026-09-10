from pywinauto import Desktop
import time

notepad = Desktop(backend="uia").window(
    title_re=".*Notepad.*"
)

editor = notepad.child_window(
    control_type="Document"
)

editor.click_input()

while True:
    print(repr(editor.window_text()))
    time.sleep(1)