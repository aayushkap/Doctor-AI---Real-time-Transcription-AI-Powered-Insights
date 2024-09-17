import React, { useState, useEffect } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";
import Loader from "./Loader";

const RealTimeTranscription = () => {
  const [recognizer, setRecognizer] = useState(null);
  const [transcription, setTranscription] = useState("");
  const [accumulatedTranscription, setAccumulatedTranscription] = useState("");
  const [downloadLink, setDownloadLink] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isSdkLoaded, setIsSdkLoaded] = useState(false);
  const [orchestratorResponse, setOrchestratorResponse] = useState("");
  const [loadingRes, setLoadingRes] = useState(false);
  const [orchestratorTime, setOrchestratorTime] = useState("");

  // Load Speech SDK on component mount
  useEffect(() => {
    if (window.SpeechSDK) {
      setIsSdkLoaded(true);
    } else {
      const script = document.createElement("script");
      script.src = "https://aka.ms/csspeech/jsbrowserpackageraw";
      script.onload = () => setIsSdkLoaded(true);
      document.body.appendChild(script);
    }
  }, []);

  const startListening = () => {
    setTranscription("");
    setAccumulatedTranscription("");
    setLoadingRes(false);
    setOrchestratorResponse("");
    setOrchestratorTime("");

    if (!isSdkLoaded) {
      console.error("Speech SDK is not loaded yet.");
      return;
    }

    // Initialize speech config and audio input
    const speechConfig = window.SpeechSDK.SpeechConfig.fromSubscription(
      process.env.REACT_APP_AZURE_SUBSCRIPTION_KEY,
      process.env.REACT_APP_AZURE_REGION
    );
    const audioConfig =
      window.SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

    const recognizerInstance = new window.SpeechSDK.SpeechRecognizer(
      speechConfig,
      audioConfig
    );

    // Event handlers
    recognizerInstance.recognizing = (s, e) => {
      setTranscription(e.result.text);
    };

    recognizerInstance.recognized = (s, e) => {
      if (e.result.reason === window.SpeechSDK.ResultReason.RecognizedSpeech) {
        setTranscription(e.result.text);
        setAccumulatedTranscription((prev) => prev + e.result.text + "\n");
      } else if (e.result.reason === window.SpeechSDK.ResultReason.NoMatch) {
        setTranscription("No speech could be recognized.");
      }
    };

    recognizerInstance.canceled = (s, e) => {
      console.error(`Canceled: ${e.reason}`);
      if (e.reason === window.SpeechSDK.CancellationReason.Error) {
        console.error(`Error details: ${e.errorDetails}`);
      }
      stopListening();
    };

    recognizerInstance.sessionStopped = () => {
      console.log("Stopped listening.");
      stopListening();
    };

    // Start continuous recognition
    recognizerInstance.startContinuousRecognitionAsync();
    setRecognizer(recognizerInstance);
    setIsListening(true);
  };

  const stopListening = () => {
    recognizer?.stopContinuousRecognitionAsync(() => {
      recognizer.close();
      setRecognizer(null);

      const blob = new Blob([accumulatedTranscription], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      setDownloadLink(url);

      console.log("Session stopped. Sending transcription to orchestrator.");
      setLoadingRes(true); // Ensure the loader shows here

      fetch("http://localhost:8000/orchestrator", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ transcription: accumulatedTranscription }),
      })
        .then((response) => response.json())
        .then((data) => {
          setLoadingRes(false); // Hide loader after the response
          setOrchestratorResponse(data?.message || "No response from server");
          setOrchestratorTime(data?.time_taken || "No response from server");
        })
        .catch((error) => {
          console.error("Error:", error);
          setLoadingRes(false); // Hide loader on error
          setOrchestratorResponse(
            "Error occurred while processing transcription."
          );
        });

      setIsListening(false);
    });
  };
  return (
    <main className="container">
      <h1>Doctor AI</h1>
      <div className="controls">
        {!isListening ? (
          <button onClick={startListening} disabled={!isSdkLoaded}>
            Start Listening
          </button>
        ) : (
          <button onClick={stopListening} disabled={!isListening}>
            Stop Listening
          </button>
        )}
      </div>

      {accumulatedTranscription && (
        <p className="transcription">{accumulatedTranscription}</p>
      )}

      {loadingRes && <Loader />}

      {orchestratorResponse && (
        <>
          <ReactMarkdown className="response">
            {orchestratorResponse}
          </ReactMarkdown>
          <p>Time taken by orchestrator: {orchestratorTime}</p>
        </>
      )}

      {downloadLink && (
        <a href={downloadLink} download="transcription.txt">
          Download Transcription
        </a>
      )}
    </main>
  );
};

export default RealTimeTranscription;
