from flask import Flask, render_template, request, send_file, session
import os
import PyPDF2 

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def cropper(start_page, end_page, file_path):
    """Crop a PDF to the specified page range."""
    try:
        output_file = os.path.join(OUTPUT_FOLDER, os.path.basename(file_path).replace(".pdf", "_cropped.pdf"))

        with open(file_path, "rb") as input_pdf:
            reader = PyPDF2.PdfReader(input_pdf)
            writer = PyPDF2.PdfWriter()

        
            for i in range(start_page - 1, end_page):
                if i < len(reader.pages):
                    writer.add_page(reader.pages[i])
                else:
                    break

         
            with open(output_file, "wb") as output_pdf:
                writer.write(output_pdf)

        return output_file
    except Exception as e:
        print(f"Error in cropper: {e}")
        return None


@app.route("/")
def upload():
    return render_template("file_upload.html")


@app.route("/success", methods=["POST"])
def success():
    try:
        session["start_page"] = int(request.form['start'])
        session["end_page"] = int(request.form['end'])
        f = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(file_path)
        session["file_path"] = file_path

        return render_template("success.html", start=session["start_page"],
                               end=session["end_page"], name=f.filename)
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route("/convert")
def cropper_view():
    start_page = session.get("start_page")
    end_page = session.get("end_page")
    file_path = session.get("file_path")

    if not all([start_page, end_page, file_path]):
        return "Session data is missing, please start over.", 400

    if not os.path.exists(file_path):
        return "Input file not found. Please upload the file again.", 400

    output_file = cropper(start_page, end_page, file_path)
    if not output_file or not os.path.exists(output_file):
        return "Error during PDF cropping. Please try again.", 500

    session["output_file"] = output_file 
    return render_template("download.html")


@app.route("/download")
def download():
    output_file = session.get("output_file")
    if not output_file or not os.path.exists(output_file):
        return "Output file not found. Please try again.", 400

    return send_file(output_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
