from flask import Flask, request
import whisper 
import os

app = Flask(__name__)

# Create a temporary folder to store uploaded files
UPLOAD_FOLDER = '../tmp_folder/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return "<h1>SafePal AI!</h1>"

@app.route('/transcribe', methods=["POST"])
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
    print(f"\n{result['text']}")

    # Clean up the uploaded file after transcription
    os.remove(file_path)

    return {"status": 200, "message": "Transcription successful", "data": result["text"]}

if __name__ == '__main__':
    app.run(debug=True)
