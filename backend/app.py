from flask import Flask, request
import whisper
import os

app = Flask(__name__)

UPLOAD_FOLDER = '../tmp_folder/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return "<h1>SafePal AI!</h1>"

@app.route('/transcribe', methods=["POST"])
def transcribe():

    if "file" not in request.files:
        return {"status": 400, "message": "No file uploaded"}
    
    file = request.files['file']

    if file.filename == "":
        return {"status": 400, "message": "No file selected"}

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print("File received....")

    print("Transcribing....")

    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    print("Transcription done..")
    print(result["text"])

    os.remove(file_path)

    return {"status": 200, "message": "Transcription successful", "data": result["text"]}

if __name__ == '__main__':
    app.run(debug=True)
