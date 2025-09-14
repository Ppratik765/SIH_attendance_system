import qrcode
from pyngrok import ngrok, conf
from PIL import Image, ImageTk
import tkinter as tk
import time

def get_public_url():
    """Start ngrok tunnel and return public URL"""
    conf.get_default().auth_token = "32gDXrlaNrndK3SdKLuPEdERKQy_5BuQFA6ptKT74LW37sAAs"
    tunnel = ngrok.connect(5000, "http")
    return tunnel.public_url

if __name__ == "__main__":
    print("Starting ngrok tunnel... please wait")
    url = get_public_url()
    print(f"QR will point to: {url}")

    # Small delay to ensure QR file is saved before Tkinter loads it
    qr = qrcode.make(url)
    qr.save("attendance_qr.png")
    time.sleep(1)

    # --- Tkinter Window ---
    root = tk.Tk()
    root.title("Attendance QR Code")

    label = tk.Label(root, text="Scan this QR to mark attendance", font=("Arial", 16))
    label.pack(pady=10)

    img = Image.open("attendance_qr.png")
    qr_img = ImageTk.PhotoImage(img)

    qr_label = tk.Label(root, image=qr_img)
    qr_label.pack(pady=10)


    root.mainloop()
