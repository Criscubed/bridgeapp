from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf_with_custom_size_and_dpi(file_path, width, height, dpi):
    # Create a PDF document with custom size
    pdf_canvas = canvas.Canvas(file_path, pagesize=(width, height))

    # Set the resolution (dots per inch) for the canvas
    # pdf_canvas.setEncrypt(dpi, dpi)


    return pdf_canvas

# doesnt get run since we are runnning the CreatePDF instead
# if __name__ == "__main__":
#     # Specify the file path for the new PDF
#     pdf_file_path = "pdf_with_high_dpi_example.pdf"
#
#     # Specify the custom size in points (1 inch = 72 points)
#     custom_width = 288  # 4 inches
#     custom_height = 3456  # 48inches
#
#     # Set the desired DPI
#     desired_dpi = 300
#
#     # Create the PDF with the specified DPI
#     create_pdf_with_high_dpi(pdf_file_path, custom_width, custom_height, desired_dpi)
#
#     print(f"PDF with {desired_dpi} DPI created successfully at: {pdf_file_path}")
