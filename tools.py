from pathlib import Path
from langchain_core.tools import tool
from ddgs import DDGS
import trafilatura
import os
DESKTOP=Path.home()/"OneDrive"/"Desktop"
@tool
def create_folder(folder_name:str):
    """Create a new folder or nested folder in the users desktop"""
    folder_path= DESKTOP/folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    if folder_path.exists() and folder_path.is_dir():
        return f"folder '{folder_name}'succesfully created"
    return f"folder '{folder_name}' was not created"


    return f"folder created '{folder_name}'at '{folder_path}'"
@tool
def list_folder():
    """List all folders in the users desktop"""
    folders=[item.name
             for item in DESKTOP.iterdir()
             if item.is_dir()
             ]
    return folders
@tool
def delete_folder(folder_name:str):
    """Delete a folder in the users desktop"""
    folder_path = DESKTOP/folder_name
    if not folder_path.exists():
        return f"folder '{folder_name} does not exist'"
    if not  folder_path.is_dir():
        return f"folder '{folder_name} ' isnt a folder"
    try:
        folder_path.rmdir()
    except PermissionError:
        return f"access denied for folder '{folder_name}'"
    except OSError:
        return f"folder '{folder_name}' cudnt be deleted"

    return f"folder '{folder_name}' deleted"
@tool
def search_web(search_term:str):
    """Search duckduckgo.com for the search term provided by the user"""
    try:
        with DDGS() as ddgs:
            results= [r for r in ddgs.text(search_term,max_results=5)]
            if not results:
                return f"search term '{search_term}' not found"
            formated_output =""
            for i , res in enumerate(results,1):
                formated_output += f"{i}. {res.get('title')}\n"
                formated_output += f"{i}. {res.get('body')}\n"
                formated_output += f"{i}. {res.get('href')}\n\n"
            return formated_output
    except Exception as ex:
        return f"search term '{search_term}' had an error {str(ex)}"
@tool
def read_webpage(webpage_url:str):
    """fetches and extractes the webpage content from the given url"""
    try:
        download= trafilatura.fetch_url(webpage_url)
        if not download:
            return f"webpage '{webpage_url}' not be downloaded"
        content = trafilatura.extract(download,include_comments=True)
        if not content:
            return f"webpage '{webpage_url}'cant be extracted"
        return content[:5000]
    except Exception as ex:
        return f"webpage '{webpage_url}' had an error {str(ex)}"
@tool
def write_file(file_path: str, content: str):
    """Create a file on the user's Desktop and write content into it."""

    try:
        file_path = Path(file_path)

        if not file_path.is_absolute():
            file_path = DESKTOP / file_path

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

        if not file_path.exists():
            return f"FAILED: File was not created at '{file_path}'"

        if not file_path.is_file():
            return f"FAILED: Path exists but is not a file: '{file_path}'"

        saved_content = file_path.read_text(encoding="utf-8")

        if saved_content != content:
            return "FAILED: File was created but content verification failed."

        return f"SUCCESS: File created and verified at '{file_path}'"

    except Exception as ex:
        return f"FAILED: Could not write file '{file_path}': {type(ex).__name__}: {ex}"
if __name__ == "__main__":
    result = write_file.invoke({
        "file_path": "S3_test/test2.md",
        "content": "hello from Cosmicon"
    })

    print(result)

