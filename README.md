# Imagino

Imagino is a Streamlit-based application that allows users to generate AI-powered images using Hugging Face's Stable Diffusion model. It also includes Firebase authentication for user login and signup.

## Project Structure

```
Imagino/
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── main.py               # Entry point of the application
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── app/
│   ├── main_app.py       # Main application logic for image generation
│   └── __pycache__/      # Compiled Python files
├── auth/
│   ├── firebase_auth.py  # Firebase authentication logic
│   └── __pycache__/      # Compiled Python files
```

## Configuration

### Environment Variables

The application requires a `.env` file to store sensitive information. Below is an example of the `.env` file:

```plaintext
# Hugging Face Token
HF_TOKEN=your_hugging_face_token

# OpenAI API Key
GEMINI_API_KEY=your_openai_api_key

# Tawk.to API Keys
TAWK_PROPERTY_ID=your_tawk_property_id
TAWK_WIDGET_ID=your_tawk_widget_id

# Firebase Config
FIREBASE_KEY_PATH=firebase_key.json
FIREBASE_DB_URL=https://your-firebase-database-url

# Firebase Authentication
FIREBASE_API_KEY=your_firebase_api_key
```

### Dependencies

The required Python dependencies are listed in the `requirements.txt` file:

```plaintext
streamlit
requests
python-dotenv
pillow
```

Install them using the following command:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/imagino.git
   cd imagino
   ```

2. Create a `.env` file in the root directory and add the required environment variables as shown above.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   streamlit run main.py
   ```

5. Open the application in your browser at `http://localhost:8501`.

## Features

- **AI Image Generation**: Generate images using Hugging Face's Stable Diffusion model.
- **Prompt Builder**: Customize prompts with style, mood, and use case options.
- **User Authentication**: Secure login and signup using Firebase Authentication.
- **Chat Support**: Integrated Tawk.to chat widget for expert consultation.

## License

This project is licensed under the MIT License. See the LICENSE file for details.