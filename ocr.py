import easyocr


reader = easyocr.Reader(['en'])


def extract_text(image_path):

    result = reader.readtext(
        image_path,
        paragraph=True
    )

    text = ""

    for detection in result:

        text += detection[1] + "\n"

    return text