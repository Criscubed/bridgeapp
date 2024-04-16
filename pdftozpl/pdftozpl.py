from zebrafy import ZebrafyPDF

with open("source.pdf", "rb") as pdf:
    zpl_string = ZebrafyPDF(pdf.read(), invert=True, dither=False, threshold=255).to_zpl()

with open("output.zpl", "w") as zpl:
    zpl.write(zpl_string)

# THIS PRODUCES REALLY UGLY ZPL FILES

