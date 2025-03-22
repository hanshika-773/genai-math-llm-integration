## Integration of a Mathematical Calulations with a Chat Completion System using LLM Function-Calling

### AIM:
To design and implement a Python function for calculating the volume of a cylinder, integrate it with a chat completion system utilizing the function-calling feature of a large language model (LLM).

### PROBLEM STATEMENT: Design and implement a Python function to calculate the volume of a cylinder and integrate it with an LLM-powered chat system using function-calling. 

### DESIGN STEPS:

#### STEP 1: Load environment variables and set up the OpenAI API key for authentication.

#### STEP 2: Implement calculate_cylinder_volume(radius, height), which computes and returns the volume in JSON format.

#### STEP 3: Create a function definition in JSON format (functions list) to enable OpenAI's function-calling capability.

#### STEP 4: Send a user’s request to the OpenAI chat model (ChatCompletion.create) along with function metadata.

#### STEP 5:  If the model invokes calculate_cylinder_volume, extract arguments, compute the result, append it to the conversation, and send a final request to get the AI's response.

### PROGRAM:
```
import os
import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY") 

def calculate_cylinder_volume(radius, height):
    volume = 3.14159265359 * (radius ** 2) * height
    return json.dumps({"radius": radius, "height": height, "volume": volume})

functions = [
    {
        "name": "calculate_cylinder_volume",
        "description": "Calculate the volume of a cylinder given its radius and height.",
        "parameters": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "description": "The radius of the cylinder in meters."},
                "height": {"type": "number", "description": "The height of the cylinder in meters."}
            },
            "required": ["radius", "height"]
        }
    }
]

messages = [{"role": "user", "content": "What is the volume of a cylinder with radius 10 and height 5?"}]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=functions
)

response_message = response["choices"][0]["message"]
if "function_call" in response_message:
    args = json.loads(response_message["function_call"]["arguments"])
    result = calculate_cylinder_volume(**args)
    
    messages.append({
        "role": "function",
        "name": "calculate_cylinder_volume",
        "content": result,
    })
    
    final_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    print(final_response["choices"][0]["message"]["content"])

```

### OUTPUT:
![Screenshot 2025-03-22 112425](https://github.com/user-attachments/assets/a0436019-5520-49c8-b12d-e6c421f8dfe5)

### RESULT:  The code enables LLM-driven cylinder volume calculation via function calling.
