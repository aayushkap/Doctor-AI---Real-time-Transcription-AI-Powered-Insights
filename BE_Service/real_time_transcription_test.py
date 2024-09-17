# import os
# from dotenv import load_dotenv
# import azure.cognitiveservices.speech as speechsdk
# import pyaudio

# # List available microphones
# def list_microphones():
#     p = pyaudio.PyAudio()
#     for i in range(p.get_device_count()):
#         info = p.get_device_info_by_index(i)
#         if info['maxInputChannels'] > 0:
#             print(f"Device {i}: {info['name']}")

# # Set the microphone by index or name
# def speak_to_microphone(api_key, region, device_name=None):
#     speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
#     speech_config.speech_recognition_language = "en-US"

#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)  # Use the default microphone

#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

#     # Set timeout duration
#     speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "5000")  # 5 seconds
#     speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10000")  # 6 seconds

#     print("Say something...")

#     while True:
#         speech_recognition_result = speech_recognizer.recognize_once_async().get()

#         if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#             print("Recognized: {}".format(speech_recognition_result.text))
#         elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
#             print("No speech could be recognized")
#         elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
#             cancellation_details = speech_recognition_result.cancellation_details
#             print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#             if cancellation_details.reason == speechsdk.CancellationReason.Error:
#                 print("Error details: {}".format(cancellation_details.error_details))
#             break

# load_dotenv()

# api_key = os.getenv("AZURE_SPEECH_KEY")
# region = os.getenv("AZURE_SPEECH_REGION")

# # List available microphones before selecting one
# list_microphones()

# # Set the microphone by device name
# # For example, pass the device name "Headset (Eos Hands-Free AG Audio)"
# speak_to_microphone(api_key, region, device_name="Headset (Eos Hands-Free AG Audio)")
