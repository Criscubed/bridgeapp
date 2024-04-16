from tkinter.filedialog import askdirectory
import os
import csv
import errno
import shutil


def inches_to_dots(inch):
    # assuming printer prints at 300 dpi
    return inch * 12 * 203


def put_text_at(address, height_inch, zpl, suffix, thickness, name):

    # draw a line of width 900(~4.4 inches) height of 4 and some thickness
    line_y = inches_to_dots(height_inch)
    print(line_y)
    line_thickness = 4
    zpl.write("^FO0," + str(int(line_y)) + "^GB900,4," + str(line_thickness) + ",^FS\n")
    zpl.write("^FO780," + str(int(line_y) -100) + "^ADB,36,20^FD" + str(thickness) + "^FS\n")

    # canvas.setFont('Helvetica', 33) # draw a line
    # canvas.drawString(0, ft_to_pts(height_inch), f"_________________________________________________________________")
    # canvas.setFont('Helvetica', 10) # draw some text
    # canvas.drawString(5, ft_to_pts(height_inch) - 20, f"Bridge  Span Beam Point Side  Dir")
    # canvas.setFont('Courier', 15) # draw values under the text
    # # needs python 3.11 to parse these strings.
    # if len(address["Bridge"]) == 2:
    #     bm_location = f"{address["Bridge"]}  {address["Span"]} {address["Beam"]} {address["Point"]} {address["Side"]}"
    # else:
    #     bm_location = f"{address["Bridge"]} {address["Span"]} {address["Beam"]} {address["Point"]} {address["Side"]}"
    # canvas.drawString(10, ft_to_pts(height_inch) - 40, f"{bm_location} {suffix}")
    # canvas.rotate(90) # draw some rotated text
    # canvas.setFont('Helvetica', 10)
    # canvas.drawString(ft_to_pts(height_inch) - 35, -282, f"{round(thickness, 2)}")
    # canvas.rotate(-90)
    # create_png(name)
    # canvas.drawInlineImage("./qrcodes/" + name + ".png", 200, ft_to_pts(height_inch) - 40)


def create_zpl(file_path, csv_data_array, suffix):
    # create the zpl file
    # zpl file width is expected to be of 288 points (4 inches)
    # expected dpi of printer is 300
    zplfile = open(file_path, "a")
    zplfile.seek(0)
    zplfile.truncate()
    zplfile.write("^XA\n")

    sum = 0
    firstPoint = 0
    firstSide = 'R'
    for foamfill in csv_data_array:
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
            print("sum = " + str(sum) + " thickness = " + str(thickness))
            sum += thickness  # sum = sum + thickness
            put_text_at(address, sum, zplfile, suffix, thickness, name)
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
            print("sum = " + str(sum) + " thickness = " + str(thickness))
            sum += thickness  # sum = sum + thickness
            put_text_at(address, sum, zplfile, suffix, thickness, name)

    # if firstSide == 'L':  # left side starts on left
    #     if str(firstPoint) == '01':
    #         pdf_canvas.drawString(-3, 1, f".")  # left side
    #     if str(firstPoint) == '02':
    #         pdf_canvas.drawString(custom_width - 11, 1, f".")  # right side
    # if firstSide == 'R':  # right side starts on right
    #     if str(firstPoint) == '01':
    #         pdf_canvas.drawString(custom_width - 11, 1, f".")  # right side
    #     if str(firstPoint) == '02':
    #         pdf_canvas.drawString(-3, 1, f".")  # left side
    zplfile.write("^XZ")
    zplfile.close()


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

    # get csv path from user
    csvpath = askdirectory(title='Select a Folder Full of TABLES')  # shows dialog box and return the path


    try:
        os.makedirs(csvpath + "/zpl")
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for file in os.listdir(csvpath):
        if file.endswith(".csv"):
            # Specify the file path for the new zpl
            coords_file = csvpath + "/" + file
            zpl_file_path_fwd = csvpath + "/zpl/" + file.removesuffix(".csv") + "_fw.zpl"
            zpl_file_path_bk = csvpath + "/zpl/" + file.removesuffix(".csv") + "_bk.zpl"

            # Read data from the CSV
            csv_data = read_csv(coords_file)

            # Create the zpl
            create_zpl(zpl_file_path_fwd, csv_data, "FW")
            create_zpl(zpl_file_path_bk, csv_data, "BK")
