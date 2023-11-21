# As-You-Go GPT - Interactive Chat with AI

As-You-Go GPT is an intuitive and interactive application that enables users to have a conversation with AI on-the-fly. The program is designed to assist with chat sessions, file handling, and URL content retrieval, making it an indispensable tool for users who need AI-powered assistance in real-time.

![As-You-Go GPT UI](homeImage.png)

## Features

- Chat with AI: Engage in a natural conversation with an advanced AI model, and receive responses in real-time.
- File Handling: Easily upload and analyze content from various file formats, including text, images, and PDFs.
- URL Content Retrieval: Input URLs to fetch and process the text content for use in the chat session or analysis.
- Session Management: Start new conversations, save chat history, and clear messages effortlessly.
- Customizable Settings: Configure AI model parameters such as temperature and top P to tailor the response generation.

## Installation

Before running the application, ensure you have the necessary dependencies installed.

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/Abdel-Siam/As-You-Go-GPT.git
    ```

2. Install the required Python libraries using pip:

    ```
    pip install -r requirements.txt
    ```

3. Configure your OpenAI API key in the `.config` file:

    ```ini
    [OPENAI]
    API_KEY = Your-OpenAI-API-Key
    MODEL = gpt-3.5-turbo-1106
    ```

4. Run the application:

    ```
    python main.py
    ```

## Usage

Upon launching the application, you will be greeted with a user-friendly interface where you can interact with the AI by typing messages in the chatbox or uploading files for analysis.

- To chat, simply enter your message in the textbox and press "Submit" or hit the enter key.
- To upload files, drag and drop them into the designated area or use the file picker.
- To save the chat history, click on the "Save Chat" button.
- To adjust AI settings, head to the "Settings" tab and tweak the sliders to your preference.

## Additional Implementations

While As-You-Go GPT is feature-packed and ready to use, there are additional implementations that could further enhance the user experience:

- **Message Regeneration**: Adding the ability of regenerating previous messages.
- **Complete Output Copy**: Adjust message copying to not only be for code but also text.
- **Custom Themes**: Implementation of additional themes to personalize the UI.
- **Multilingual Support**: Adding support for multiple languages in chat.
- **Voice Interaction**: Incorporating voice recognition and text-to-speech features.
- **Advanced File Analysis**: Extending support for more file types and providing in-depth content analysis.

Feel free to contribute to these additional implementations or suggest new ones!

## Contribute

Your contributions are welcome! Please feel free to fork the repository, make changes, and submit pull requests.

## Feedback

If you encounter any issues or have any suggestions, please open an issue on the GitHub repository, and we'll get back to you as soon as possible.

Enjoy chatting with AI using As-You-Go GPT!

---

*Note: As-You-Go GPT is a project that utilizes OpenAI's API and is not officially affiliated with OpenAI.*