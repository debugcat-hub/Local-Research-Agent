from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from data import CaseRecord
from langchain_core.messages import ToolMessage
from langchain_groq import ChatGroq
from tools import create_folder,list_folder,delete_folder,search_web,read_webpage,write_file
llm = ChatOpenAI(
    base_url="http://127.0.0.1:20128/v1",
    api_key="sk-7605b268e864287a-8c83d5-bb0751f4",
    model="auto/coding",
    temperature=0.1
)

tools = [create_folder,
         list_folder,
         delete_folder,
         search_web,
         read_webpage,
         write_file]
llm_with_tools= llm.bind_tools(tools)
tool_map={
    "create_folder":create_folder,
    "list_folder":list_folder,
    "delete_folder":delete_folder,
    "search_web":search_web,
    "read_webpage":read_webpage,
    "write_file":write_file
}
# structured= llm.with_structured_output(CaseRecord)


prompt = ChatPromptTemplate.from_messages([
    ("user", """You are an AI assistant named Cosmicon that can use tools when necessary.
    when the user prompts u to do folder management YOU have to follow these instructions
    
    FOLDER CREATION:
- When the user asks to create nested folders, create the complete folder hierarchy in a single create_folder tool call.
- Use "/" to represent nested folders.
- For example, if the user says "create folder A and inside it create folder B", call:
  create_folder("A/B")
- Do not create A and B as separate Desktop folders.
- The create_folder tool creates missing parent directories automatically.
    When the user asks you to research a product:

    1. Identify the specific product being researched.
    2. Search the web for reliable information about the product.
    3. Search Reddit for user reviews and experiences.
    4. Gather information from at least 5 relevant Reddit discussions or reviews when available.
    5. Provide a structured response containing:
       - Product description
       - Pros
       - Cons
       - Reddit user sentiment
       - Overall conclusion
    6. Clearly distinguish facts from user opinions.
    7. Do not invent reviews, pros, cons, or sources.
    8. If there is not enough information to provide 5 genuine Reddit-based pros or cons, say so instead of making them up.

    Use tools whenever current or external information is required.

    User request:
    {input}
    """)
])
chain =prompt | llm_with_tools.bind(tool_choice="auto")
def run_agent(user_input):
    response = chain.invoke({
        "input":user_input
    })
    messsage= [*prompt.invoke({"input":user_input}).to_messages(),
               response]
    print(response.tool_calls)
    while response.tool_calls:
        tool_message =[]
        for tool_call in response.tool_calls:
            print("TOOL:", tool_call["name"])
            print("ARGS:", tool_call["args"])
            tool = tool_map[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            tool_message.append(ToolMessage(
                content =str(result),
                tool_call_id = tool_call["id"]
            ))
        messsage.extend(tool_message)
        response= llm_with_tools.invoke(messsage)
        messsage.append(response)
    return response.content

#
# user_input = input("cosmos:")
# response = run_agent(user_input)
# print(response)



# for tool_call in response.tool_calls:
#
#     result=create_folder.invoke(tool_call["args"])
#     tool_message.append( ToolMessage( str(result),
#                         tool_call_id = tool_call["id"]))
# final_response= llm_with_tools.invoke([response]+tool_message)
# print(final_response.content)

