from PyPDF2 import PdfWriter, PdfReader
import os

def cropper(start, end, file):
    # Check if the file exists
    if not os.path.exists(file):
        print(f"Error: File not found at {file}")
        return

    try:
        # Open the input PDF
        inputPdf = PdfReader(file)
        outPdf = PdfWriter()

        # Adjust for zero-based indexing
        start_index = start - 1
        end_index = end - 1

        # Create the output file name
        output_file = file.split(".")[0] + "_cropped.pdf"

        # Write the selected pages to the new PDF
        with open(output_file, "wb") as ostream:
            for page_num in range(start_index, end_index + 1):
                outPdf.add_page(inputPdf.pages[page_num])
            outPdf.write(ostream)

        print(f"Cropped PDF saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
cropper(1, 4, r"C:\Users\Pramod\Downloads\Flask-Pdf-Splitter--master\Flask-Pdf-Splitter--master\sample.pdf")
