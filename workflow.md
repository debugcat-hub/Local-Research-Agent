# Cosmicon - Local Research Agent

## 1. Purpose

Cosmicon is a local AI research agent that can:

- Search the web
- Read webpages
- Create folders
- List folders
- Delete folders
- Write research reports to files
- Verify that file operations were completed successfully

The agent runs locally using an LLM through LM Studio.

---

# 2. Available Tools

## create_folder

Creates a folder or nested folder structure on the user's Desktop.

Example:

create_folder("Cosmic_data/cosmic_ai_keys")

Expected result:

Desktop/
└── Cosmic_data/
    └── cosmic_ai_keys/

The tool must verify that the requested folder exists after creation.

---

## list_folder

Lists folders present on the user's Desktop.

Used when Cosmicon needs to inspect the current Desktop structure.

---

## delete_folder

Deletes a folder from the user's Desktop.

The tool should:

1. Check whether the folder exists.
2. Check that the path is actually a folder.
3. Attempt deletion.
4. Report whether deletion succeeded.

---

## search_web

Searches DuckDuckGo for information.

Used when Cosmicon needs current or external information.

Example:

search_web("AI coding tools")

The search results should be passed back to the LLM for analysis.

---

## read_webpage

Downloads and extracts readable content from a webpage.

Used after search_web when Cosmicon needs more information from a specific source.

Example:

search_web
    ↓
find relevant URL
    ↓
read_webpage

---

## write_file

Creates a file and writes content into it.

The tool should:

1. Create missing parent directories.
2. Create the file.
3. Write the content.
4. Verify that the file exists.
5. Verify that the path is a file.
6. Verify that the saved content matches the requested content.

Example:

write_file(
    "Desktop/ai research tools/report.md",
    "Research report..."
)

---

# 3. Basic Agent Workflow

For a normal research request:

User
    ↓
Understand request
    ↓
Search web
    ↓
Analyze search results
    ↓
Read relevant webpages
    ↓
Analyze gathered information
    ↓
Generate report
    ↓
Create required folder
    ↓
Write report
    ↓
Verify report
    ↓
Return final response

---

# 4. Example Research Task

User request:

"Do marketing research on AI coding tools and store the report
in a folder called ai research tools."

Expected workflow:

search_web("AI coding tools")
    ↓
search_web("AI coding tools Reddit")
    ↓
read_webpage(relevant sources)
    ↓
Analyze information
    ↓
Generate research report
    ↓
create_folder("ai research tools")
    ↓
write_file(
    "ai research tools/AI Coding Tools Report.md",
    report_content
)
    ↓
Verify file
    ↓
Return result to user

---

# 5. Nested Folder Requests

When the user requests nested folders, the complete hierarchy
should be represented in one folder path.

Example:

"Create a folder called cosmicon's model and inside it create
star_keys."

The preferred tool call is:

create_folder("cosmicon's model/star_keys")

NOT:

create_folder("cosmicon's model")
create_folder("star_keys")

The second approach creates two sibling folders on the Desktop.

---

# 6. Tool Verification

Every tool should verify the result of its operation whenever
possible.

The basic pattern is:

LLM
    ↓
Tool
    ↓
Execute action
    ↓
Verify result
    ↓
Return SUCCESS or FAILED
    ↓
LLM

The LLM should not assume that an operation succeeded merely
because the tool was called.

---

# 7. Success and Failure

Tools should return clear results.

Success example:

SUCCESS:
Folder created and verified at:
C:\Users\...\Desktop\research

Failure example:

FAILED:
Folder was not created.

The LLM should use the tool result to determine what happened.

The LLM must not claim that an operation succeeded if the tool
reported failure.

---

# 8. Agent Tool Chaining

Cosmicon currently uses an iterative tool-calling loop.

Conceptually:

LLM
 ↓
Tool call
 ↓
Execute tool
 ↓
Tool result
 ↓
LLM
 ↓
Next tool call
 ↓
Execute tool
 ↓
Tool result
 ↓
LLM
 ↓
Final response

The LLM decides what tool should be called next based on the
previous tool result.

---

# 9. Future Architecture

The current agent will eventually be improved using LangGraph.

Possible future workflow:

START
  ↓
Plan
  ↓
Research
  ↓
Read Sources
  ↓
Analyze
  ↓
Generate Report
  ↓
Save Report
  ↓
Verify
  ↓
Success?
  ├── YES → END
  └── NO → Retry / Correct