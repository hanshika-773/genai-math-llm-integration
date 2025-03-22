#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import openai
import json
from dotenv import load_dotenv, find_dotenv


# In[4]:


_ = load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY") 


# In[5]:


def calculate_cylinder_volume(radius, height):
    """Calculates the volume of a cylinder."""
    volume = 3.14159265359 * (radius ** 2) * height
    return json.dumps({"radius": radius, "height": height, "volume": volume})


# In[6]:


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


# In[10]:


messages = [{"role": "user", "content": "What is the volume of a cylinder with radius 10 and height 5?"}]


# In[11]:


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=functions
)


# In[12]:


response_message = response["choices"][0]["message"]
if "function_call" in response_message:
    args = json.loads(response_message["function_call"]["arguments"])
    result = calculate_cylinder_volume(**args)
    
    
    messages.append({
        "role": "function",
        "name": "calculate_cylinder_volume",
        "content": result,
    })
    
    # Get final response
    final_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    print(final_response["choices"][0]["message"]["content"])

