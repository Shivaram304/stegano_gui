🕵️‍♂️ Steganography Tool for Image/File Hiding
This is a simple GUI-based tool for hiding and extracting secret text messages within image files using LSB (Least Significant Bit) steganography. It supports drag-and-drop functionality and works with PNG and BMP image formats.

📌 Features
✅ Hide secret text messages in images (PNG/BMP)

✅ Extract hidden text from stego-images

✅ Drag-and-drop image upload support

✅ Image preview before encoding/decoding

✅ Save the stego-image to a new file

✅ Simple and intuitive tkinter GUI

🛠 Tools and Libraries Used
Python 3.x

Pillow (PIL) – image processing

tkinter – GUI

tkinterDnD2 – drag and drop support

🚀 How to Run
Clone the repository or download the script files.

Install dependencies:

pip install pillow tkinterDnD2
Run the GUI tool:
python steg_gui.py
💡 How It Works
The tool modifies the Least Significant Bit (LSB) of the RGB values of each pixel to hide the binary representation of each character in the message.

An EOF marker (11111110) is used to detect the end of the hidden message.

The message is extracted by reading the LSBs from the image until the EOF marker is found.

BMP

Note: JPEG is not supported due to lossy compression which distorts hidden data.


👤 Author
Shiva Ram
Computer Science Student | Cybersecurity Enthusiast
