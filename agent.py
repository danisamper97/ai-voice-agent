from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    elevenlabs,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents.metrics import STTMetrics,LLMMetrics, TTSMetrics, EOUMetrics
import asyncio

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        stt=openai.STT()
        llm=openai.LLM(model="gpt-3.5-turbo")
        tts=elevenlabs.TTS()
        vad=silero.VAD.load()
        turn_detection=MultilingualModel()

        super().__init__(
            instructions="You are a helpful voice AI assistant expert in the field of soccer. You only respond to questions related to soccer. You are friendly and helpful.", 
            stt=stt,
            llm=llm,
            tts=tts,
            vad=vad,
            turn_detection=turn_detection,
            )

        # LLM Metrics: Most import ones are Time To First Token (ttft), and Tokens per second (tokens_per_second)
        def llm_metrics_wrapper(metrics: LLMMetrics):
            asyncio.create_task(self.on_llm_metrics_collected(metrics))
        llm.on("metrics_collected", llm_metrics_wrapper)

        # STT Metrics: Most import ones are the duration of the input audio (audio_duration) and whether streming was used (streamed)
        def stt_metrics_wrapper(metrics: STTMetrics):
            asyncio.create_task(self.on_stt_metrics_collected(metrics))
        stt.on("metrics_collected", stt_metrics_wrapper)

        # End Of Utterance Metrics: it is emitted whne the user is determined to have finished speaking.
        # 1. end_of_utterance_delay - Time from the end of speech to the point when the user's turn is considered complete.
        # 2. transcription_delay - Time between the end of speech and when final transcript is available. 
        def eou_metrics_wrapper(metrics: EOUMetrics):
            asyncio.create_task(self.on_eou_metrics_collected(metrics))
        stt.on("eou_metrics_collected", eou_metrics_wrapper)

        # TTS Metrics: 
        # 1. Time To First Byte (ttfb) - how fast the agent is starting to speak back to us. 
        # 2. audio_duration - duration of the output audio
        def tts_metrics_wrapper(metrics: TTSMetrics):
            asyncio.create_task(self.on_tts_metrics_collected(metrics))
        tts.on("metrics_collected", tts_metrics_wrapper)

    async def on_llm_metrics_collected(self, metrics: LLMMetrics) -> None:
        print("\n--- LLM Metrics ---")
        print(f"Prompt Tokens: {metrics.prompt_tokens}")
        print(f"Completion Tokens: {metrics.completion_tokens}")
        print(f"Tokens per second: {metrics.tokens_per_second:.4f}")
        print(f"TTFT: {metrics.ttft:.4f}s")
        print("------------------\n")

    async def on_stt_metrics_collected(self, metrics: STTMetrics) -> None:
        print("\n--- STT Metrics ---")
        print(f"Duration: {metrics.duration:.4f}s")
        print(f"Audio Duration: {metrics.audio_duration:.4f}s")
        print(f"Streamed: {'Yes' if metrics.streamed else 'No'}")
        print("------------------\n")

    async def on_eou_metrics_collected(self, metrics: EOUMetrics) -> None:
        print("\n--- End of Utterance Metrics ---")
        print(f"End of Utterance Delay: {metrics.end_of_utterance_delay:.4f}s")
        print(f"Transcription Delay: {metrics.transcription_delay:.4f}s")
        print("--------------------------------\n")

    async def on_tts_metrics_collected(self, metrics: TTSMetrics) -> None:
        print("\n--- TTS Metrics ---")
        print(f"TTFB: {metrics.ttfb:.4f}s")
        print(f"Duration: {metrics.duration:.4f}s")
        print(f"Audio Duration: {metrics.audio_duration:.4f}s")
        print(f"Streamed: {'Yes' if metrics.streamed else 'No'}")
        print("------------------\n")

# The AgentSession is the main orchestrator for the voice AI app. Therefore, the session is responsible for: 
# 1. Collecting user input
# 2. managing the voice pipeline
# 3. Invoking the LLM - Generating a response using the LLM
# 4. Sending the output back to the user - Converting the LLM response to speech
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        # stt=openai.STT(),
        # llm=openai.LLM(model="gpt-3.5-turbo"),
        # tts=elevenlabs.TTS(),
        # vad=silero.VAD.load(),
        # turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))