from flask import Flask, request, render_template_string
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("base")

HTML = """
<!doctype html>
<title>Upload Audio to Transcribe</title>
<h1>Upload an MP3 file</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if transcription %}
<h2>Transcription:</h2>
<p>{{ transcription }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    transcription = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)
            result = model.transcribe(file_path)
            transcription = result["text"]
    return render_template_string(HTML, transcription=transcription)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
