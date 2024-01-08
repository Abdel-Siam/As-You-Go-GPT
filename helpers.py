import xml.etree.ElementTree as ET
import base64
import os
import fitz  # PyMuPDF
from openai import OpenAI

# Function to handle different types of files
def handle_file(filepath):
    # Extract file extension and base name
    file_extension = filepath.split('.')[-1].lower()
    baseName = os.path.basename(filepath)
    
    # Handling text files
    if file_extension in ['java', 'py', 'txt', 'c', 'md']:
        try:
            with open(filepath, 'r') as file:
                file_contents = file.read()
                
            FileMessage = {
                "type": "text",
                "text": "The following are the contents of " + baseName + ": " + file_contents,
            }
            
            return FileMessage, file_contents
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    # Handling image files    
    elif file_extension in ['jpg', 'png']:
        try:
            with open(filepath, "rb") as image_file:
                FileMessage = { 
                    "type": "image_url",
                    "image_url": {
                    "url": f"""data:image/{file_extension};base64,{base64.b64encode(image_file.read()).decode('utf-8')}"""
                    }
                }
                
                return FileMessage, ""
        except FileNotFoundError:
            print(f"Error: Image file '{filepath}' not found.")
            return None
        except Exception as e:
            print(f"Error encoding image file: {e}")
            return None
        
    # Handling XML files
    elif file_extension == 'xml':
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
            
            FileMessage = {
                "type": "text",
                "text": "The following are the contents of " + baseName + ": " + xml_string,
            }
            
            return FileMessage, xml_string
        except FileNotFoundError:
            print(f"Error: XML file '{filepath}' not found.")
            return None
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            return None
        
    # Handling PDF files        
    elif file_extension == 'pdf':
        try:
            pdf_contents = ""
            with fitz.open(filepath) as pdf:
                for page in pdf:
                    pdf_contents += page.get_text()
                    
            FileMessage = {
                "type": "text",
                "text": "The following are the contents of " + baseName + ": " + pdf_contents,
            }

            return FileMessage, pdf_contents
        except FileNotFoundError:
            print(f"Error: PDF file '{filepath}' not found.")
            return None
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return None
            
    else:
        print(f"Unsupported file type: {file_extension}. Please provide a supported file type (.java, .py, .txt, .jpg, .png, .xml, .pdf, .md).")
        return None


import requests 

# DEPRECATED - changed with an open ai function call Ideally, add topP: float and maxTokens: int parameters to the method signature.
def getResponse(apiKey: str, model: str, messages: list, temperature: int, topP: float, maxTokens: int):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": maxTokens,
        "temperature": temperature,
        "top_p": topP,  # Add this line to include topP in the API request
        "stream": True,
        # You might also want to handle 'stop sequences' or other parameters here
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response

# DEPRECATED - removed with the get response function, Function to print response information from OpenAI API
def printResponseInformation(response):
    # Assuming the response is in JSON format
    print("Prompt Tokens: ", response["usage"]["prompt_tokens"])
    print('Completion Tokens: ', response["usage"]["completion_tokens"])
    print("Total Tokens: ", response["usage"]["total_tokens"])
    print("")
    print(response["choices"][0]['message']['role'])
    print(response["choices"][0]['message']['content'])
         
# Function to create messages for the OpenAI API request
def createMessages(systemMessage:str, message:str, background:list, chat_history:list):
    # Implementation for creating messages based on systemMessage, user message, background, and chat history
    
    # no history
    if chat_history == []:
        if background == []:
            payloadMessage = [
                    {
                        "role": "system",
                        "content": systemMessage
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message
                            },
                        ]
                    }
                ]
        else:
            payloadMessage = [
                    {
                        "role": "system",
                        "content": systemMessage
                    },
                ]
            
            content = [] 
            for i in range(len(background)):
                content.append(background[i])
            
            userMessage = {
                            "type": "text",
                            "text": message
                        }
            content.append(userMessage)
            
            newUserMessage = {
                        "role": "user",
                        "content": content
                    }
            payloadMessage.append(newUserMessage)
            
    # history present
    else:
        payloadMessage = [
                {
                    "role": "system",
                    "content": systemMessage
                },
        ]
        
        content = [] 
        if background != []:
            for i in range(len(background)):
                content.append(background[i])
            
        for i in range(len(chat_history)):
            currHist = chat_history[i]
            
            if i == 0 and background != []:
                prevUserMessages = currHist[0].split("\n\n\nPrompt")[0]
                content.append({'type': 'text', 'text': prevUserMessages})
                user = {
                        "role": "user",
                        "content": content
                    }
                assistant = {
                        "role": "assistant",
                        "content": currHist[1]
                    }
            else:
                prevUserMessages = currHist[0].split("\n\n\nPrompt")[0]
                user = {
                        "role": "user",
                        "content": currHist[0]
                    }
                assistant = {
                        "role": "assistant",
                        "content": currHist[1]
                    }
            
            payloadMessage.append(user)
            payloadMessage.append(assistant)
        
        newUserMessage = {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message
                            },
                        ]
                    }
        payloadMessage.append(newUserMessage)
        
        print(payloadMessage)    
        
    return payloadMessage

# Function to clear chat history
def clearhistory(chat_history:list):
    return []

import tiktoken
# Function to count tokens in text
def count_tokens(text):
    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = enc.encode(text, disallowed_special=())
    return len(tokens)

import json

def insertUserMessage(message:str, chat_history:list):
    print(chat_history)
    return "", chat_history + [[message, None]]
    
# Function to get AI response from OpenAI API
def respond(systemMessage:str, background:list, chat_history:list, apiKey:str, model:str, temperature:int, topP:int, maxTokens:int):
    client = OpenAI(api_key=apiKey)
    
    message = chat_history[-1][0]
    # initalize it to a string
    chat_history[-1][1] = ""
    # Implementation for API call and handling the response
    messages = createMessages(systemMessage, message, background, chat_history)
    
    completion = client.chat.completions.create(
    model=model,
    temperature=temperature,
    top_p=topP,
    max_tokens=maxTokens,
    messages=messages,
    stream=True
    )
     
    for chunk in completion:
        # print(chunk.choices[0].delta)
        if chunk.choices[0].delta.content != None:
            chat_history[-1][1] += str(chunk.choices[0].delta.content)
            yield chat_history    
    
    
# Function to upload multiple files
def uploadFile(files, backgroundInfo:list):
    # Implementation for uploading and handling file contents

    doneMessage = '# Done Uploading'
    
    for file in files:
        name = file.name
        baseName = os.path.basename(name)
        contentMessage, content = handle_file(file)
        
        if content != None:
            numTokens = count_tokens(content)
            doneMessage += "\n" + baseName + " contains: " +  str(numTokens) + " Tokens" 
            
        if contentMessage != None:
            backgroundInfo.append(contentMessage)
    
    return doneMessage, backgroundInfo

# Function to clear files
def clearFiles(files):
    # Implementation for clearing files
    fileContents = []
    doneMessage = '# Files Cleared'
    
    return doneMessage, fileContents

import os
# Function to save the chat
def save_chat(chat_history):
    
    # Directory where the file will be saved
    directory = './'

    # Name of the file
    file_name = 'Saved_Chats.txt'

    # Full path to the file
    file_path = os.path.join(directory, file_name)

    # Check if the file already exists
    counter = 1
    while os.path.exists(file_path):
        # If file exists, add a number to the filename and check again
        file_name = f'Saved_Chats_{counter}.txt'
        file_path = os.path.join(directory, file_name)
        counter += 1

    # Write the lines to the file
    with open(file_name, "w") as file:
        for chat in chat_history:
            file.write(f"User: {chat[0]}\n")
            file.write(f"Assistant: {chat[1]}\n\n")

    print(f'File saved to: {file_path}')
    
import concurrent.futures
import requests
import re

from bs4 import BeautifulSoup

def _download_single(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download URL: {url}")
    except Exception as e:
        return None

def _download_urls(urls, threads=1):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(_download_single, url): url for url in urls}
        
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if data:
                results[url] = data
    return results

def urls_to_strings(urls, threads=5, strong_cleanup=False):
    urls = [url.strip() for url in urls.split('\n') if url.strip()]
    content_dict = _download_urls(urls, threads=threads)
    results = {}
    
    for url, content in content_dict.items():
        soup = BeautifulSoup(content, features="lxml")
        for script in soup(["script", "style"]):
            script.extract()

        strings = soup.stripped_strings
        if strong_cleanup:
            strings = [s for s in strings if re.search("[A-Za-z] ", s)]

        text = '\n'.join([s.strip() for s in strings])
        results[url] = text
    
    return results

# Update the urls_to_strings_func to process URLs and update the background list correctly
def urls_to_strings_func(urls, status, backgroundInfo):
    # Call the urls_to_strings function from helpers.py
    Status = "# URLs processed successfully."
    strong_cleanup = True  # You can make this an option in your UI if needed
    urls_results = urls_to_strings(urls, strong_cleanup=strong_cleanup)
    
    # Iterate over the results and add each to the background list separately
    for url, content in urls_results.items():
        # Create a dictionary entry for each URL's text content
        url_entry = {
            "type": "text",
            "text": "The following are the contents of " + url + ": " + content,
        }
        # Append this entry to the background information state
        backgroundInfo.append(url_entry)
        numTokens = count_tokens(content)
        Status += "\n" + url + " contains: " +  str(numTokens) + " Tokens" 
    
    # Return a confirmation message and the updated background information state.
    return Status, backgroundInfo
