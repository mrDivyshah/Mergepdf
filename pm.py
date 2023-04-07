from flask import Flask, render_template
import os
import datetime
import glob
import shutil
import time
from PyPDF4 import PdfFileMerger, PdfFileReader

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/merge_pdfs')
def merge_pdfs():
    src_folder = r"G:\My Drive\Mix documents\merged_pdfs\output_"
    dst_folder = r"G:\My Drive\Mix documents\merged_pdfs\past pdf\\"
    pattern = "\*.pdf"
    files_move = glob.glob(src_folder + pattern)
    for filem in files_move:
        file_name = os.path.basename(filem)
        while True:
            try:
                shutil.move(filem, dst_folder + file_name)
                print('Moved:', filem)
                break
            except PermissionError:
                time.sleep(1)

    def fetch_all_pdf_files(parent_folder: str):
        target_files = []
        for path, subdirs, files in os.walk(parent_folder):
            for name in files:
                if name.endswith(".pdf"):
                    target_files.append(os.path.join(path, name))
        return target_files

    def merge_pdf(list_of_pdfs, output_folder):
        merger = PdfFileMerger()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        suffix = ""
        while os.path.exists(os.path.join(output_folder, f"final_merged_pdf_{current_date}{suffix}.pdf")):
            suffix = "_" + str(int(suffix.split("_")[-1]) + 1) if suffix else "_1"
        output_pdf = os.path.join(output_folder, f"final_merged_pdf_{current_date}{suffix}.pdf")
        os.makedirs(output_folder, exist_ok=True) # create the output folder if it doesn't exist
        for file in list_of_pdfs:
            with open(file, 'rb') as pdf_file:
                merger.append(PdfFileReader(pdf_file, strict=False))
        with open(output_pdf, "wb") as f:
            merger.write(f)

    pdf_files = fetch_all_pdf_files("G:\My Drive\Mix documents\pc pdf")
    output_folder = "G:\My Drive\Mix documents\merged_pdfs\output_"
    merge_pdf(pdf_files, output_folder)
    src_folder = r"G:\My Drive\Mix documents\pc pdf"
    dst_folder = r"G:\My Drive\Mix documents\PastLabelPdf\\"
    pattern = "\*.pdf"
    files_move = glob.glob(src_folder + pattern)
    for filem in files_move:
        file_name = os.path.basename(filem)
        try:
            shutil.move(filem, dst_folder + file_name)
            print('Moved:', filem)
        except PermissionError as e:
            print(f"Failed to move {filem}: {e}")
            continue
    return render_template('inner-page.html')

if __name__ == '__main__':
    app.run(debug=True,port=5500)
