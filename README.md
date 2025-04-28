# Imagino

**Imagino** is an innovative Streamlit-based application that enables users to generate stunning, AI-powered images using Hugging Face's **Stable Diffusion** model. With **real-time feedback** and an integrated **expert consultation** feature, **Imagino** creates a bridge between AI-generated art and human refinement. When AI falls short, users can directly connect with professional designers to improve and perfect their images.
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
│   ├── info_page.py      # Additional information page
│   └── __pycache__/      # Compiled Python files
├── auth/
│   ├── firebase_auth.py  # Firebase authentication logic
│   ├── firebase_utils.py # Firebase utility functions
│   └── __pycache__/      # Compiled Python files
├── firebase/
│   ├── firebase_key.json # Firebase service account key
│   └── firebase-adminsdk.json # Firebase admin SDK configuration
├── mascot.png            # Application mascot image
├── set_background.py     # Script to set background images
├── clearhistory.py       # Script to clear user history
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
firebase-admin
```

Install them using the following command:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/sobhushan/Imagino.git
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

- **AI Image Generation**: Generate high-quality images using Hugging Face's Stable Diffusion XL model. Ideal for artists, marketers, and designers who need creative visuals quickly.
- **User Authentication**: Secure login and signup via Firebase Authentication, allowing users to save their history and preferences.
- **Expert Consultation**: If the AI-generated image doesn't meet your expectations, seamlessly connect with a human expert via an integrated Tawk.to chat for real-time design refinement.
- **Real-Time Feedback**: Provide immediate feedback on the generated images, enabling the AI to regenerate and refine the image according to your specifications.
- **History Management**: Start fresh by clearing chat history or saving images, ensuring users can manage their workflow without data overload.

## How It Works: Bridging the Gap Between AI and Human Expertise

Imagino isn't just another image generation tool; it’s a hybrid platform that blends the creative power of AI with the nuanced expertise of human designers. Here’s how it works:

- **AI-Powered Art Generation**: The application uses **Stable Diffusion XL** to generate images from simple prompts, offering fast, high-quality visual outputs. This is great for quickly brainstorming concepts or creating content for projects.
- **Instant Image Refinement**: Sometimes, AI doesn't fully capture your vision. That's where the **real-time feedback loop** comes in. You can immediately communicate with the AI to refine your designs through a chat interface, making quick changes to styles, colors, and elements.
- **Human Expertise for Perfection**: If the AI isn't quite getting it right, Imagino bridges the gap by offering the ability to directly connect with a **human expert designer** via the **Tawk.to chat widget**. Whether you need design tweaks, specific adjustments, or a fresh perspective, a professional designer can step in to enhance your image.
- **Seamless Transition Between AI and Human**: The flow from AI to human expert is smooth and intuitive, ensuring that users can keep their creative process moving forward without interruption.

## Why Choose Imagino?

- **Speed & Efficiency**: AI generates instant results, but when it doesn’t meet your expectations, human designers are just a click away.
- **Creative Freedom**: Enjoy a variety of AI-generated options, then work with a designer to fine-tune them to your precise needs.
- **Expert Guidance**: Get professional insights to turn good AI art into great, customized designs.
- **Personalized Design**: AI gives you a strong starting point, but the human touch ensures the final design perfectly matches your vision.

## Future Improvements

- **Enhanced AI Models**: Integrate more advanced AI models from **OpenAI** for better image generation, enabling even more creative possibilities.
- **Improved Chat Interface**: Upgrade the chat and expert consultation features to create a smoother, more engaging user experience.
- **Chat History Storage**: Implement better storage solutions to allow users to save and revisit old chats and feedback threads.
- **Prompt Builder**: Add a custom prompt builder to allow users to easily adjust style, mood, and use-case options for their generated images.
- **User Profiles**: Enable user profiles to save preferences, history, and personalized settings.
- **Mobile Optimization**: Improve the responsiveness of the app for better mobile device support.


##  Live Demo
🌐 [Imagino App](https://imagino-image-gen-2025.streamlit.app/)

> 🛠️ _This app is under active development. Features may evolve or temporarily break._


