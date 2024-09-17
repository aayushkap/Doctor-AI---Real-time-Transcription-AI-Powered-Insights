# import asyncio
# import websockets
# import azure.cognitiveservices.speech as speechsdk
# import os
# import subprocess
# import ffmpeg
# import tempfile
# from services.azure_openai_service import make_api_call

# # Set up Azure Speech SDK
# speech_key = os.getenv('AZURE_SPEECH_KEY')
# service_region = os.getenv('AZURE_SPEECH_REGION')
# print(f"Using Azure Speech SDK with key {speech_key} in region {service_region}")

# def speech_recognizer(audio_stream):
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#     audio_input = speechsdk.audio.AudioConfig(stream=audio_stream)
#     return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

# async def transcribe_audio(websocket, path):
#     # Create a push stream for incoming audio data
#     audio_stream = speechsdk.audio.PushAudioInputStream()

#     # Create a recognizer using the audio stream
#     recognizer = speech_recognizer(audio_stream)

#     def recognized(evt):
#         if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
#             print(f"Recognized: {evt.result.text}")
#             asyncio.run(websocket.send(evt.result.text))

#     recognizer.recognized.connect(recognized)

#     # Start continuous recognition
#     recognizer.start_continuous_recognition()

#     try:
#         await websocket.send("WebSocket connection established. Start sending audio!")

#         temp_audio_file = tempfile.NamedTemporaryFile(suffix=".webm", delete=False)

#         while True:
#             message = await websocket.recv()
#             if isinstance(message, bytes):
#                 # Write the binary audio data received from the WebSocket to a temporary file
#                 temp_audio_file.write(message)
#             elif message == "stop":
#                 # Close the temp file and process it
#                 temp_audio_file.close()

#                 # Convert the recorded WebM/Ogg file to PCM using ffmpeg
#                 pcm_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#                 ffmpeg.input(temp_audio_file.name).output(pcm_file.name, format="wav", acodec="pcm_s16le", ac=1, ar="16000").run()

#                 # Open the PCM file and write its contents to the PushAudioInputStream
#                 with open(pcm_file.name, 'rb') as pcm_data:
#                     while True:
#                         chunk = pcm_data.read(4096)
#                         if not chunk:
#                             break
#                         audio_stream.write(chunk)

#                 # Close the audio stream after processing
#                 audio_stream.close()

#                 await websocket.send("Recognition stopped.")
#                 break

#     except Exception as e:
#         await websocket.send(f"Error: {str(e)}")

# start_server = websockets.serve(transcribe_audio, "localhost", 8765)

# # Start WebSocket server
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
