# Import necessary modules
import gradio as gr
import random
import time
import configparser
from helpers import *
import openai

# Read API configurations from .config file
config = configparser.ConfigParser()
config.read('.config')
api_key = config.get('OPENAI', 'API_KEY', fallback="Input-OpenAI-key")  # Replace 'your-fallback-api-key' if you want a default
model_name = config.get('OPENAI', 'MODEL', fallback="gpt-3.5-turbo-1106")

# Define the theme for the Gradio app
theme = gr.themes.Default(
    font=['Noto Sans', 'Helvetica', 'ui-sans-serif', 'system-ui', 'sans-serif'],
    font_mono=['IBM Plex Mono', 'ui-monospace', 'Consolas', 'monospace'],
).set(
    border_color_primary='#c5c5d2',
    button_large_padding='6px 12px',
    body_text_color_subdued='#484848',
    background_fill_secondary='#eaeaea'
)

# Import the UI CSS
import UIcss
css = UIcss.css

# Initialize the Gradio blocks with the imported css and theme
blocks = gr.Blocks(css=css, theme=theme)

with blocks as demo:
    # Create the main markdown header
    gr.Markdown("# As-You-Go GPT")

    # Create a state to retain background information throughout the session
    backgroundInfo = gr.State(value=[])

    # Create tabs for different UI sections
    with gr.Tabs(elem_classes="Tabs"):
        with gr.Tab("Home"):
            
            # Create a row for the chat history display
            with gr.Row():
                chatHistory = gr.Chatbot(elem_classes="ChatBox")

            # Create a row for user input and actions
            with gr.Row(equal_height=True):
                userInput = gr.Textbox(lines=3, container=False, placeholder="User Input...", elem_classes=["inputBox", 'add_scrollbar textarea','pretty_scrollbar'], autofocus=True)
                tokenCounterDefault = gr.HTML(value="<span>0</span>", elem_classes=["token-counter"])
                submitBtn = gr.Button("Submit", elem_classes="inputButton")
                newConvoBtn = gr.Button("New Conversation", elem_classes="inputButton")
                
            # Create a row for saving the chat session
            with gr.Row():
                saveChat = gr.Button("Save Chat")

            # Create an accordion for file uploading and URL input
            with gr.Accordion(label="Load File", open=False):
                with gr.Group():
                    status = gr.Markdown("")
                    addFileDrop = gr.Files(file_types=["image", "video", "audio", "text"])
                    url_input = gr.Textbox(lines=10, label='Input URLs', info='Enter one or more URLs separated by newline characters.')
                    addURLS = gr.Button("Load URLs")
                
        with gr.Tab("Settings", elem_classes="Tabs"):
            
            # Display OpenAI settings
            gr.Markdown("# OpenAi: ")
            with gr.Row():
                # Use API configurations from the .config file
                apiKey = gr.Textbox(label="API key", value=api_key)
                modelName = gr.Dropdown(label="Model: ", value=model_name, choices=["gpt-4-1106-preview", "gpt-4-vision-preview", "gpt-4", "gpt-3.5-turbo-1106"])
            
            # Display model message settings
            gr.Markdown("# Model Settings: ")
            with gr.Row():
                systemMessage = gr.Textbox(label="System Message", value="You are a helpful assistant.")
            
            # Adding max_tokens slider
            with gr.Row():
                maxTokens = gr.Slider(label="Max tokens:", minimum=1, maximum=4096, value=4096, step=1)
                
            with gr.Row():
                temperature = gr.Slider(label= "Temperature: ", minimum=0, maximum=2, value=1, step=0.01)
            
            # Adding top_p slider
            with gr.Row():
                topP = gr.Slider(label="Top P:", minimum=0.0, maximum=1.0, value=1.0, step=0.01)
            
            with gr.Row():
                saveSettings = gr.Button("Save Settings")
        
        # Register functions for various user interactions
        submitBtn.click(respond, [userInput, systemMessage, backgroundInfo, chatHistory, apiKey, modelName, temperature, topP, maxTokens], [userInput, chatHistory], trigger_mode='once')
        userInput.submit(respond, [userInput, systemMessage, backgroundInfo, chatHistory, apiKey, modelName, temperature, topP, maxTokens], [userInput, chatHistory])
        userInput.change(lambda x: f"<span>{count_tokens(x)}</span>", userInput, tokenCounterDefault, show_progress=False)
        newConvoBtn.click(clearhistory, chatHistory, chatHistory)
        addFileDrop.upload(uploadFile, [addFileDrop], [status, backgroundInfo])
        addFileDrop.clear(clearFiles, [addFileDrop], [status, backgroundInfo])
        saveChat.click(save_chat, chatHistory)

        addURLS.click(urls_to_strings_func, [url_input, status, backgroundInfo], [status, backgroundInfo])
        # addFile.upload(uploadFile, addFileDrop, addFileDrop)
        
# Uncomment the following line if you want to enable queueing for handling requests
# demo.queue()

# Run the Gradio app
if __name__ == "__main__":
    demo.launch()