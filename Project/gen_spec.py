import json
import glob
from groq import Groq
import os

# Extract function details from AST JSON files
def extract_functions(ast_data):
    functions = []
    for node in ast_data.get("children", []):
        if node.get("kind") == "CursorKind.FUNCTION_DECL":
            # Extract function details
            function_info = {
                "name": node["spelling"],  # Function name
                "returnType": "Unknown",  # Return type isn't directly available in the provided JSON
                "parameters": []
            }
            # Extract parameters
            for child in node.get("children", []):
                if child.get("kind") == "CursorKind.PARM_DECL":
                    function_info["parameters"].append(child["spelling"])
            functions.append(function_info)
    return functions

# Read AST JSON files
function_list = []
for filename in glob.glob("*.json"):
    with open(filename, "r") as f:
        ast_data = json.load(f)
    function_list.extend(extract_functions(ast_data))

# Prepare Llama 3 prompt
doxygen_prompt = f"""
You are specialized in   Functional Specification Generation  . Generate a   detailed function specification   for the given input function. The specification should include:  
 
    1.   Function Description:    
       - A clear and concise explanation of what the function does.  
 
    2.   Input Specifications:    
       - Expected input types and formats.  
       - Constraints and assumptions on input parameters.  
       - Edge cases, boundary conditions, and corner cases that the function should handle.  
       - Valid and invalid input examples.  
       - Identify necessary validations and recommend macro-based checks where applicable.  
       - Detect function implementation issues related to parameter handling (e.g., null pointers, invalid lengths).  
 
    3.   Output Specifications:    
       - Expected output types and formats.  
       - Possible return values, including for edge cases and failure conditions.  
       - Expected results for different input scenarios, highlighting any function constraints.  
 
    4.   Constraint Detection & Edge Case Analysis:    
       - Identify function-specific constraints (e.g., dependencies, buffer overflows, undefined behavior risks).  
       - Highlight possible implementation issues based on input-output mapping.  
       - Provide test scenarios covering normal, edge, and erroneous cases, along with expected outcomes.  
 
       Do not generate function implementation.     
       Ensure that the recommended checks do not alter the intended functionality of the function.
"""
file = open('sample1.cc').read()
for function in function_list:
    doxygen_prompt += f"""
        code : {file}
    """

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": doxygen_prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
)

llama3_response = chat_completion.choices[0].message.content

# Save documentation
os.makedirs("docs", exist_ok=True)
with open("docs/functional_spec1.md", "w") as f:
    f.write(llama3_response)

print("Documentation updated in docs/functional_spec.md")
