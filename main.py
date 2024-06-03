import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk
import qrcode

def generate_qr_codes():
    data = entry.get()
    if data:
        words = [word.strip() for word in data.split(",")]  # Split input into individual words/phrases
        for i, word in enumerate(words):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(word)
            qr.make(fit=True)

            img = qr.make_image(fill_color=qr_fill_color, back_color=qr_back_color)
            img = img.resize((qr_size, qr_size))  # Resize image for display

            # Insert logo/image in the center of the QR code
            if logo_path:
                logo = Image.open(logo_path)
                logo = logo.convert("RGBA")
                logo = logo.resize((qr_size//4, qr_size//4))  # Resize logo to fit in the center
                position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, position, logo)

            img.save(f"qr_code_{i + 1}.png")  # Save image as PNG file
            img_tk = ImageTk.PhotoImage(img)
            qr_labels[i].config(image=img_tk)
            qr_labels[i].image = img_tk
    else:
        for label in qr_labels:
            label.config(image="")
            label.image = None
        messagebox.showerror("Error", "Please enter data to generate QR Codes.")

def save_qr_codes():
    directory = filedialog.askdirectory()
    if directory:
        for i, img in enumerate(qr_images):
            img.save(f"{directory}/qr_code_{i + 1}.png")
        messagebox.showinfo("Success", "QR Codes saved successfully.")
    else:
        messagebox.showerror("Error", "Please select a directory to save the QR Codes.")

def choose_qr_color():
    color = colorchooser.askcolor(title="Choose QR Code Color")[1]
    if color:
        global qr_fill_color
        qr_fill_color = color

def choose_background_color():
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        global qr_back_color
        qr_back_color = color

def choose_qr_size():
    global qr_size
    size = simpledialog.askinteger("QR Code Size", "Enter QR Code size (pixels):", initialvalue=200)
    if size:
        qr_size = size

def choose_logo():
    global logo_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        logo_path = file_path

def clear_input():
    entry.delete(0, tk.END)
    for label in qr_labels:
        label.config(image="")
        label.image = None

# Default values for QR code customization
qr_fill_color = "black"
qr_back_color = "white"
qr_size = 200
logo_path = None  # Path to the logo/image

# Create tkinter window
root = tk.Tk()
root.title("QR Code Generator by (((T)))")

# Create entry widget
entry = tk.Entry(root, width=50)
entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Create button to generate QR codes
generate_button = tk.Button(root, text="Generate QR Codes", command=generate_qr_codes, bg="blue", fg="white")
generate_button.grid(row=1, column=0, padx=10, pady=5)

# Create button to save QR codes
download_button = tk.Button(root, text="Download QR Codes", command=save_qr_codes, bg="green", fg="white")
download_button.grid(row=1, column=2, padx=10, pady=5)

# Create button to choose QR code color
qr_color_button = tk.Button(root, text="Choose QR Color", command=choose_qr_color)
qr_color_button.grid(row=2, column=1, padx=10, pady=5)

# Create button to choose background color
background_color_button = tk.Button(root, text="Choose Background Color", command=choose_background_color)
background_color_button.grid(row=2, column=0, padx=10, pady=5)

# Create button to choose logo/image
choose_logo_button = tk.Button(root, text="Choose Logo", command=choose_logo)
choose_logo_button.grid(row=2, column=2, padx=10, pady=5)

# Create button to clear input
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.grid(row=3, column=1, padx=10, pady=5)

# Create labels to display QR codes
qr_labels = []
qr_images = []
for i in range(5):  # Assuming a maximum of 5 QR codes to display
    label = tk.Label(root)
    label.grid(row=4, column=i, padx=10, pady=5)
    qr_labels.append(label)

# Run tkinter event loop
root.mainloop()
