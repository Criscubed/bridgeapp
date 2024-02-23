import qrcode


def create_png(name):
    # Create a QR code object with a larger size and higher error correction
    qr = qrcode.QRCode(version=3, box_size=1, border=0, error_correction=qrcode.constants.ERROR_CORRECT_L)

    # Define the data to be encoded in the QR code
    data = "http://localhost:5500/b?x=" + name

    # Add the data to the QR code object
    qr.add_data(data)

    # Make the QR code
    qr.make(fit=True)

    # Create an image from the QR code with a black fill color and white background
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    img.save("./qrcodes/" + name + ".png")
