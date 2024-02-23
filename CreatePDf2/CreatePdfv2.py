# from reportlab import canvas
from CustomSize import create_pdf_with_custom_size_and_dpi
import csv
import os
from tkinter.filedialog import askdirectory
from bridgeqr import create_png

PAPER_WIDTH = 4


def ft_to_pts(ft):
    return ft * 12 * 72


def put_text_at(address, height_inch, canvas, suffix, thickness, name):
    canvas.setFont('Helvetica', 33) # draw a line
    canvas.drawString(0, ft_to_pts(height_inch), f"_________________________________________________________________")
    canvas.setFont('Helvetica', 10) # draw some text
    canvas.drawString(5, ft_to_pts(height_inch) - 20, f"Bridge  Span Beam Point Side  Dir")
    canvas.setFont('Courier', 15) # draw values under the text
    # needs python 3.11 to parse these strings.
    if len(address["Bridge"]) == 2:
        bm_location = f"{address["Bridge"]}  {address["Span"]} {address["Beam"]} {address["Point"]} {address["Side"]}"
    else:
        bm_location = f"{address["Bridge"]} {address["Span"]} {address["Beam"]} {address["Point"]} {address["Side"]}"
    canvas.drawString(10, ft_to_pts(height_inch) - 40, f"{bm_location} {suffix}")
    canvas.rotate(90) # draw some rotated text
    canvas.setFont('Helvetica', 10)
    canvas.drawString(ft_to_pts(height_inch) - 35, -282, f"{round(thickness, 2)}")
    canvas.rotate(-90)
    create_png(name)
    canvas.drawInlineImage("./qrcodes/" + name + ".png", 200, ft_to_pts(height_inch) - 40)

# def put_text_at_10(address, height_inch, canvas, suffix):
#     canvas.drawString(0, ft_to_pts(height_inch), f"_________________________________________________________________")
#     canvas.setFontSize(size=14)
#     canvas.drawString(5, ft_to_pts(height_inch) - 30, f" Bridge    Span  Beam  Point Side  Dir")
#     canvas.setFontSize(size=29)
#     # needs python 3.11 to parse these strings.
#     bm_location = f"{address["Bridge"]} {address["Span"]} {address["Beam"]} {address["Point"]} {address["Side"]}"
#     canvas.drawString(10, ft_to_pts(height_inch) - 65, f"{bm_location}  {suffix}")


def find_sum_height_needed(array):
    sum = 0
    for foamfill in array:
        _, thickness = foamfill[0], float(foamfill[1])

        sum += thickness  # sum = sum + thickness
    return sum


def create_pdf(dest_file_path, array, suffix):
    # Create a PDF document

    # Specify the custom size in points (1 inch = 72 points)
    custom_width = 288  # 4 inches
    # custom_height = 3456  # 48inches

    height = find_sum_height_needed(array)
    custom_height = ft_to_pts(height)

    # Set the desired DPI
    desired_dpi = 300
    # create_pdf_with_custom_size_and_dpi
    # Create the PDF with the specified DPI
    pdf_canvas = create_pdf_with_custom_size_and_dpi(dest_file_path, custom_width, custom_height, desired_dpi)
    pdf_canvas.setFontSize(size=33)

    sum = 0
    firstPoint = 0
    firstSide = 'R'
    for foamfill in array:
        name, thickness = foamfill[0], float(foamfill[1])
        if len(name) == 9:
            address = {
                "Bridge": name[0:2],
                "Span": name[2:4],
                "Beam": name[4:6],
                "Point": name[6:8],
                "Side": name[8:]
            }
            if sum == 0:
                firstPoint = address["Point"]
                firstSide = address["Side"]
            print(str(address) + " " + suffix)
            sum += thickness  # sum = sum + thickness
            put_text_at(address, sum, pdf_canvas, suffix, thickness, name)
        elif len(name) == 10:
            address = {
                "Bridge": name[0:3],
                "Span": name[3:5],
                "Beam": name[5:7],
                "Point": name[7:9],
                "Side": name[9:]
            }
            if sum == 0:
                firstPoint = address["Point"]
                firstSide = address["Side"]
            print(str(address) + " " + suffix)
            sum += thickness  # sum = sum + thickness
            put_text_at(address, sum, pdf_canvas, suffix, thickness, name)

    pdf_canvas.setFontSize(size=50)
    if firstSide == 'L':  # left side starts on left
        if str(firstPoint) == '01':
            pdf_canvas.drawString(-3, 1, f".")  # left side
        if str(firstPoint) == '02':
            pdf_canvas.drawString(custom_width - 11, 1, f".")  # right side
    if firstSide == 'R':  # right side starts on right
        if str(firstPoint) == '01':
            pdf_canvas.drawString(custom_width - 11, 1, f".")  # right side
        if str(firstPoint) == '02':
            pdf_canvas.drawString(-3, 1, f".")  # left side

    # Save the PDF to the specified file path
    pdf_canvas.save()


def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(
                row
            )
    return data


if __name__ == "__main__":
    # Specify the file path for the new PDF
    # pdf_file_path_fwd = "example_fwd Richmond.pdf"
    # pdf_file_path_bk = "example_bk Richmond.pdf"
    # coords_file = "BR23 FOAMFILL SP 5 BM09 L.csv"

    csvpath = askdirectory(title='Select a Folder Full of TABLES')  # shows dialog box and return the path

    # TODO: if pdfs folder does not exist, create it
    for file in os.listdir(csvpath):
        if file.endswith(".csv"):
            # Specify the file path for the new PDF
            coords_file = csvpath + "/" + file
            pdf_file_path_fwd = "/pdfs/" + file.removesuffix(".csv") + "_fw.pdf"
            pdf_file_path_bk = "/pdfs/" + file.removesuffix(".csv") + "_bk.pdf"

            # Read data from the CSV
            csv_data = read_csv(coords_file)

            # Create the PDF
            create_pdf(csvpath + pdf_file_path_fwd, csv_data, "FW")
            create_pdf(csvpath + pdf_file_path_bk, csv_data[1:], "BK")
            # create_pdf(right_pdf_file_path, right_coords_file, "Right")
