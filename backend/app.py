from flask import Flask, request, jsonify
from openai import OpenAI
import whisper 
import os

app = Flask(__name__)

# Load environment variables
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")
model = "gemini-2.5-flash"

# Create a temporary folder to store uploaded files
UPLOAD_FOLDER = '../tmp_folder/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def scam_analysis(transcribed_text):

    try:
        # Validate environment variables
        if not api_key:
               raise ValueError("GEMINI_API_KEY environment variable is not set")
        if not base_url:
               raise ValueError("GEMINI_BASE_URL environment variable is not set")

        # Initialize the OpenAI client
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        prompt = (
            "Analyze the following phone call transcript. Is the caller trying to scam or defraud the receiver? "
            "Answer only 'Scam' or 'Not Scam', and then briefly explain your reasoning, but don't be too lengthy.\n\n"
            f"Transcript:\n{transcribed_text.strip()}"
        )

        # Create chat completion request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a scam detection expert."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the verdict from the response
        verdict = response.choices[0].message.content

        return verdict

    # Handle exceptions
    except Exception as e:
        print(f"Error during scam analysis: {e}")

        return "Error during scam analysis"

@app.route('/')
def home():
    return "<h1>SafePal AI!</h1>"

@app.route('/transcribe', methods=["POST", "GET"])
def transcribe():

    # Check if a file is present in the request
    if "file" not in request.files:
        return {"status": 400, "message": "No file uploaded"}
    
    file = request.files['file']

    if file.filename == "":
        return {"status": 400, "message": "No file selected"}

    # Save the uploaded file to the temporary folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print("File received....")

    # Transcription logic using Whisper
    print("Transcribing....")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    print("Transcription done..")
    transcribed_text = result["text"]
    print(f"\n{transcribed_text}\n")

    # Scam analysis using Gemini API
    scam_result = scam_analysis(transcribed_text)
    print("Scam analysis done..")
    print(f"Verdict:\n{scam_result}\n")

    # Clean up the uploaded file after transcription
    os.remove(file_path)
    print("Temporary file removed.")

    return jsonify({
        "status": 200, 
        "message": "Transcription successful", 
        "data": transcribed_text, 
        "scam_analysis": scam_result
    })


if __name__ == '__main__':
    app.run(debug=True)
