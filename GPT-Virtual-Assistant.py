

def input_x(persona):
    import pyaudio
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p=pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("start recording...")

    frames = []
    seconds = 5
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("output.wav",'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    import whisper

    model = whisper.load_model('base')
    result = model.transcribe('output.wav', fp16=False)
    myinput1 = result["text"]
    print(result["text"])


    import openai
    import pyttsx3

    openai.api_key = "'''API KEY'''"

    restart_sequence = "\nAI:"
    restart_sequence = "\nHuman: "

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=persona+myinput1,

    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    text = response['choices'][0]['text']
    print(text)

    text_speech = pyttsx3.init()

    text_speech.say(text)
    text_speech.runAndWait()

    # made by Patrick Lahoud

input_x("The following is a conversation with an office assitant, ready to help with any needs.")
