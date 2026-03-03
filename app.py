import os
import subprocess
from flask import Flask, render_template, request, send_file
import img2pdf
from pdf2docx import Converter
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
CONVERTED_FOLDER = '/tmp/converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def universal_convert():
    file = request.files['file']
    direction = request.form.get('direction')
    filename = file.filename
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)
    
    base_name = filename.rsplit('.', 1)[0]
    output_path = ""

    try:
        # 1. Any File -> PDF
        if direction == 'to_pdf':
            output_path = os.path.join(CONVERTED_FOLDER, f"{base_name}.pdf")
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert(input_path))
            else:
                subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', 
                               '--outdir', CONVERTED_FOLDER, input_path], check=True)

        # 2. PDF -> Word
        elif direction == 'to_doc':
            output_path = os.path.join(CONVERTED_FOLDER, f"{base_name}.docx")
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()

        # 3. PDF -> Image
        elif direction == 'pdf_to_img':
            output_path = os.path.join(CONVERTED_FOLDER, f"{base_name}.png")
            doc = fitz.open(input_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            pix.save(output_path)
            doc.close()

        return send_file(output_path, as_attachment=True)
    finally:
        # Cleanup to save space on Render
        if os.path.exists(input_path): os.remove(input_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    