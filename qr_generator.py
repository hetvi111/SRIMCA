import qrcode

def generate_visitor_qr(url: str, output_file: str = "visitor_qr.png"):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

    print("QR Generated Successfully")


if __name__ == "__main__":

    visitor_url = "http:/ 10.149.15.181:5000/#/visitor"

    generate_visitor_qr(visitor_url)