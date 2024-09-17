# 🩺 Doctor AI

Doctor AI is a real-time voice transcription tool that listens to your speech, converts it to text using the Azure Speech SDK, and interacts with an AI backend for insightful responses. Easily download your transcriptions and get real-time feedback!

## ✨ Features

- **Live Transcription**: Converts speech to text in real-time with Azure Speech SDK.
- **AI-Powered Responses**: Sends transcriptions to an AI backend and retrieves insightful responses.
- **Download Transcription**: Save your transcript as a text file.
- **User-Friendly Interface**: Simple controls to start/stop listening and view results.

## 🚀 Getting Started

### Prerequisites

- Node.js and npm installed.
- Azure Speech SDK credentials (Subscription Key & Region).
- AI backend (like a Flask API) to handle transcription and return responses.

### Installation

1. Clone the repo:

   ```bash
   git clone [https://github.com/your-username/doctor-ai.git](https://github.com/aayushkap/Doctor-AI---Real-time-Transcription-AI-Powered-Insights.git)
   ```

2. Navigate to the project folder:

   ```bash
   cd doctor-ai
   ```

3. Install dependencies:

   ```bash
   npm install
   ```

4. Create a `.env` file in the project root with your Azure Speech SDK credentials:

   ```bash
   REACT_APP_AZURE_SUBSCRIPTION_KEY=your_azure_key
   REACT_APP_AZURE_REGION=your_azure_region
   ```

5. Start the app:

   ```bash
   npm start
   ```

## 📜 Usage

- Click **Start Listening** to start the transcription process.
- Your live transcription will display on the screen.
- Once done, click **Stop Listening** to send the transcript to the AI orchestrator and download the transcription file.

## 🔧 Technologies

- **React**: Frontend framework
- **Azure Speech SDK**: Real-time transcription
- **React Markdown**: Rendering AI responses in markdown format
- **REST API**: Backend server handling AI interactions

## 🛠️ To Do

- Implement better error handling.
- Add support for different languages.
- Improve the UI/UX with additional controls and feedback options.

## 📄 License

This project is licensed under the MIT License.

---

Happy transcribing! 🗣️📄🤖
