
# CharacterAI Chatbot

This is a simple chatbot application built with Flask and Google's GenerativeAI. It allows users to interact with a character by asking questions and receiving responses based on the character's personality.

## Getting Started

To run the application, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/DebasishTripathy13/CharacterAI.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:

   - Sign up for the Google Cloud Platform and create a new project.
   - Enable the "Cloud AI Platform" and "Cloud AI Platform Notebooks" APIs.
   - Create an API key and replace `your_api_key_here` in `app.py` with your actual API key.

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open your web browser and navigate to `http://localhost:5000` to access the chatbot interface.

## Usage

1. Enter your name, the character's name, and a brief description of the character's personality in the form on the homepage.
2. ![image](https://github.com/DebasishTripathy13/CharacterAI/assets/94828569/ea78dceb-b30b-4b31-97a2-4f9d3f4fa9cc)


3. Click "Submit" to start the chat.

4. Ask a question in the text area and click "Submit" to see the character's response.
5. ![image](https://github.com/DebasishTripathy13/CharacterAI/assets/94828569/df00ae8d-2a43-4699-9774-49c43179fbfd)


6. The chat interface displays messages from both you (owner) and the character, showing a conversation-like interaction.

## Features

- Roleplay as a character with a predefined personality.
- Interactive chat interface.
- Dynamic responses based on user input.

## Technologies Used

- Flask: Web framework for Python.
- Google GenerativeAI: API for generating text-based responses.
- HTML/CSS: Frontend for the chat interface.
- JavaScript: Frontend for dynamic interactions.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GPL License. See the [LICENSE](LICENSE) file for details.

