import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os

# ----- LSB Encode -----
def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    binary = ''.join([format(ord(c), '08b') for c in message]) + '1111111111111110'  # EOF
    data_index = 0
    img_data = list(img.getdata())

    for i in range(len(img_data)):
        pixel = list(img_data[i])
        for j in range(3):  # RGB
            if data_index < len(binary):
                pixel[j] = pixel[j] & ~1 | int(binary[data_index])
                data_index += 1
        img_data[i] = tuple(pixel)
        if data_index >= len(binary):
            break

    img.putdata(img_data)
    img.save(output_path)
    return True

# ----- LSB Decode -----
def decode_image(image_path):
    img = Image.open(image_path)
    binary = ""
    for pixel in img.getdata():
        for value in pixel[:3]:  # RGB
            binary += str(value & 1)

    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ""
    for ch in chars:
        if ch == '11111110':  # EOF
            break
        message += chr(int(ch, 2))
    return message

# ----- GUI Class -----
class StegGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("600x500")
        self.root.config(bg="#1e1e1e")

        self.image_path = None
        self.img_preview = None

        # --- Drag & Drop Setup ---
        self.dnd_frame = tk.Label(root, text="Drag and Drop Image Here",
                                  bg="#333", fg="white", font=("Arial", 14), width=60, height=10)
        self.dnd_frame.pack(pady=10)
        self.dnd_frame.drop_target_register(DND_FILES)
        self.dnd_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # --- Message Entry ---
        self.msg_entry = tk.Text(root, height=5, width=70)
        self.msg_entry.pack(pady=10)

        # --- Buttons ---
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.pack()

        tk.Button(button_frame, text="Browse Image", command=self.browse_image).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Hide Message", command=self.hide_message).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Extract Message", command=self.extract_message).grid(row=0, column=2, padx=5)

    def browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp")])
        if path:
            self.set_image(path)

    def handle_drop(self, event):
        path = event.data.strip("{}")  # Remove curly braces on Windows paths
        if os.path.isfile(path):
            self.set_image(path)

    def set_image(self, path):
        self.image_path = path
        img = Image.open(path)
        img.thumbnail((400, 300))
        self.img_preview = ImageTk.PhotoImage(img)
        self.dnd_frame.config(image=self.img_preview, text='')

    def hide_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        message = self.msg_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "No message entered.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png")])
        if save_path:
            try:
                encode_image(self.image_path, message, save_path)
                messagebox.showinfo("Success", "Message hidden and image saved.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encode image: {e}")

    def extract_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return
        try:
            message = decode_image(self.image_path)
            self.msg_entry.delete("1.0", tk.END)
            self.msg_entry.insert(tk.END, message)
            messagebox.showinfo("Success", "Message extracted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract message: {e}")

# ---- Main ----
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = StegGUI(root)
    root.mainloop()
