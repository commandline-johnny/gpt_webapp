
# GPT Web App

A Django-based web application that allows users to have dynamic conversations with OpenAI's GPT models (e.g., `gpt-4`, `gpt-3.5-turbo`). Users can start new conversations, select different GPT models, and load existing conversation sessions.

## Features

- **Interactive Chat**: Chat with OpenAI's GPT models in real-time.
- **Session Management**: Start new chat sessions or continue existing ones.
- **GPT Model Selection**: Choose between available GPT models for each session.
- **API Key Handling**: Set your OpenAI API key securely through the UI or environment variables.
- **Session Naming**: Conversations are automatically named after the first message is sent.

## Prerequisites

- Python 3.7+
- OpenAI API Key (You can obtain one from [OpenAI](https://platform.openai.com/account/api-keys))
- Django 5.x
- OpenAI Python Library (`openai>=1.0.0`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gpt-web-app.git
   cd gpt-web-app
   ```

2. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   poetry install
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory of your project and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. Migrate the database:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create a superuser for the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and go to `http://127.0.0.1:8000/` to start the app.
2. You will be prompted to select a GPT model.
3. Start a conversation by entering your message.
4. You can start a new session at any time by clicking the "Start New Session" button.
5. You can also continue previous sessions from the "Load Session" page.
