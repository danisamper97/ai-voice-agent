# AI Voice Agent for Soccer Conversations

This project implements a simple yet powerful AI voice agent focused on soccer-related conversations. Leveraging the **LiveKit** platform and the WebRTC protocol, the agent enables real-time, low-latency voice interactions. It integrates advanced speech and language technologies, including OpenAI for language understanding and speech recognition, ElevenLabs for text-to-speech, and robust audio processing components such as Voice Activity Detection (VAD), turn detection, and noise cancellation.

---

## Features

### 1. Real-Time Voice Interaction with LiveKit & WebRTC

- **LiveKit** provides the backbone for real-time audio streaming using the WebRTC protocol, ensuring seamless, low-latency communication between users and the AI agent.

### 2. Advanced Speech and Language Processing

- **OpenAI** powers both the Large Language Model (LLM) for generating intelligent, soccer-focused responses and the Speech-to-Text (STT) engine for transcribing user speech.
- **ElevenLabs** delivers high-quality, natural-sounding Text-to-Speech (TTS), allowing the agent to respond in a lifelike voice.

### 3. Enhanced Audio Pipeline

- **Voice Activity Detection (VAD):** Detects when the user is speaking, improving responsiveness and reducing false triggers.
- **Turn Detector:** Determines when the user has finished speaking, enabling natural conversational flow.
- **Noise Cancellation:** Filters out background noise, ensuring clear and intelligible audio input.

### 4. Comprehensive Metrics Collection

The agent tracks and prints detailed metrics for each stage of the voice pipeline:

- **STT Metrics:** Measures input audio duration and whether streaming was used.
- **LLM Metrics:** Tracks prompt and completion token counts, tokens processed per second, and **Time To First Token (TTFT)**—the time from sending a prompt to receiving the first token from the LLM.
- **TTS Metrics:** Includes **Time To First Byte (TTFB)**—how quickly the agent starts speaking after generating a response, and the duration of the output audio.
- **End Of Utterance (EOU) Metrics:** Captures **end_of_utterance_delay** (the time from the end of speech to when the user's turn is considered complete) and **transcription_delay** (the time between end of speech and final transcript availability).

---

## Objective

**Create a simple AI voice agent that engages in conversations exclusively about soccer.**  
The agent is friendly, knowledgeable, and only responds to soccer-related questions.

---

## Getting Started

### 1. Download Required Model Files

Before running the agent, download the necessary model files for the turn detector, Silero VAD, and noise cancellation plugins:

```bash
python agent.py download-files
```

### 2. Start the Voice Agent Console

Launch the agent in console mode:

```bash
python agent.py console
```

---

## How It Works

- The agent listens for user speech, detects when the user has finished speaking, and transcribes the audio using OpenAI's STT.
- The transcribed text is sent to OpenAI's LLM, which generates a soccer-focused response.
- The response is converted to speech using ElevenLabs TTS and played back to the user.
- Throughout the process, the agent collects and prints detailed metrics for transparency and debugging.

---

## Key Metrics Explained

- **TTFT (Time To First Token):**  
  The time it takes for the LLM to return the first token after receiving a prompt. Lower TTFT means faster, more responsive answers.

- **TTFB (Time To First Byte):**  
  The time from sending the TTS request to receiving the first byte of audio. Lower TTFB means the agent starts speaking sooner.

- **End Of Utterance Delay:**  
  The time between the user finishing speaking and the system recognizing the end of their turn. Lower delay improves conversational flow.

---

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- API keys for OpenAI, ElevenLabs, Livekit (set in your environment or `.env` file)

---

## Customization

- To change the agent’s domain, update the `instructions` parameter in the `Assistant` class.
- You can swap out STT, LLM, or TTS engines by modifying the corresponding plugin initialization.

---

## License

This project is for educational and research purposes.

---

**Enjoy talking soccer with your AI voice agent!**