import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def vigenere_cipher(text, key, mode):
    result = ""
    key_length = len(key)
    key_int = [ord(i) for i in key]
    text_int = [ord(i) for i in text]
    
    for i in range(len(text)):
        if mode == 'encrypt':
            value = (text_int[i] + key_int[i % key_length]) % 256
        else:
            value = (text_int[i] - key_int[i % key_length]) % 256
        result += chr(value)
    return result

def playfair_cipher(text, key, mode):
    key = key.upper().replace("J", "I")  # Replace J with I
    matrix = []
    seen = set()
    
    # Create the 5x5 matrix
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
    
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # I/J are combined
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    def get_pairs(text):
        text = text.upper().replace("J", "I").replace(" ", "")
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i + 1]
                if a == b:
                    pairs.append(a + 'X')  # Insert 'X' if same letters
                    i += 1
                else:
                    pairs.append(a + b)
                    i += 2
            else:
                pairs.append(a + 'X')  # If odd, append 'X'
                i += 1
        return pairs

    pairs = get_pairs(text)
    result = ""

    for pair in pairs:
        row1, col1 = divmod(matrix.index(pair[0]), 5)
        row2, col2 = divmod(matrix.index(pair[1]), 5)

        if row1 == row2:  # Same row
            result += matrix[row1 * 5 + (col1 + 1) % 5]
            result += matrix[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:  # Same column
            result += matrix[((row1 + 1) % 5) * 5 + col1]
            result += matrix[((row2 + 1) % 5) * 5 + col2]
        else:  # Rectangle swap
            result += matrix[row1 * 5 + col2]
            result += matrix[row2 * 5 + col1]

    return result if mode == 'encrypt' else decrypt_playfair(result, matrix)

def decrypt_playfair(text, matrix):
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row1, col1 = divmod(matrix.index(a), 5)
        row2, col2 = divmod(matrix.index(b), 5)

        if row1 == row2:  # Same row
            result += matrix[row1 * 5 + (col1 - 1) % 5]
            result += matrix[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:  # Same column
            result += matrix[((row1 - 1) % 5) * 5 + col1]
            result += matrix[((row2 - 1) % 5) * 5 + col2]
        else:  # Rectangle swap
            result += matrix[row1 * 5 + col2]
            result += matrix[row2 * 5 + col1]

    return result

def hill_cipher(text, key, mode):
    # Convert key to a 2x2 matrix
    key_matrix = [[ord(key[0]) - 65, ord(key[1]) - 65],
                  [ord(key[2]) - 65, ord(key[3]) - 65]]
    
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'  # Padding if odd length

    # Create text matrix
    text_matrix = []
    for i in range(0, len(text), 2):
        text_matrix.append([ord(text[i]) - 65, ord(text[i + 1]) - 65])
    
    result_matrix = []
    
    if mode == 'encrypt':
        for row in text_matrix:
            result_row = [
                (row[0] * key_matrix[0][0] + row[1] * key_matrix[0][1]) % 26,
                (row[0] * key_matrix[1][0] + row[1] * key_matrix[1][1]) % 26
            ]
            result_matrix.append(result_row)
    else:
        # Inverse of the key matrix for decryption
        det = (key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]) % 26
        det_inv = pow(det, -1, 26)  # Modular inverse of determinant

        # Adjugate matrix
        key_matrix_inv = [
            [key_matrix[1][1] * det_inv % 26, -key_matrix[0][1] * det_inv % 26],
            [-key_matrix[1][0] * det_inv % 26, key_matrix[0][0] * det_inv % 26]
        ]

        for row in text_matrix:
            result_row = [
                (row[0] * key_matrix_inv[0][0] + row[1] * key_matrix_inv[0][1]) % 26,
                (row[0] * key_matrix_inv[1][0] + row[1] * key_matrix_inv[1][1]) % 26
            ]
            result_matrix.append(result_row)

    result = ''.join(chr(num + 65) for row in result_matrix for num in row)
    return result

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, file.read())

def process_text(action):
    text = input_text.get(1.0, tk.END).strip()
    key = key_entry.get().strip()
    
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus minimal 12 karakter.")
        return
    
    if cipher_var.get() == "Vigenere":
        result = vigenere_cipher(text, key, action)
    elif cipher_var.get() == "Playfair":
        result = playfair_cipher(text, key, action)
    elif cipher_var.get() == "Hill":
        result = hill_cipher(text, key[:4], action)  # Use first 4 chars for 2x2 matrix
    
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

root = tk.Tk()
root.title("Cipher Application")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

cipher_var = tk.StringVar(value="Vigenere")

ttk.Label(main_frame, text="Pilih Cipher:").grid(row=0, column=0, columnspan=2, sticky="w")
ttk.Radiobutton(main_frame, text="Vigenere", variable=cipher_var, value="Vigenere").grid(row=1, column=0, sticky="w")
ttk.Radiobutton(main_frame, text="Playfair", variable=cipher_var, value="Playfair").grid(row=2, column=0, sticky="w")
ttk.Radiobutton(main_frame, text="Hill", variable=cipher_var, value="Hill").grid(row=3, column=0, sticky="w")

ttk.Label(main_frame, text="Kunci (min 12 karakter):").grid(row=4, column=0, columnspan=2, sticky="w")
key_entry = ttk.Entry(main_frame, width=50)
key_entry.grid(row=5, column=0, columnspan=2, pady=5)

ttk.Label(main_frame, text="Masukkan Teks:").grid(row=6, column=0, columnspan=2, sticky="w")
input_text = tk.Text(main_frame, height=10, width=50)
input_text.grid(row=7, column=0, columnspan=2, pady=5)

upload_button = ttk.Button(main_frame, text="Upload File", command=upload_file)
upload_button.grid(row=8, column=0, columnspan=2, pady=5)

encrypt_button = ttk.Button(main_frame, text="Enkripsi", command=lambda: process_text('encrypt'))
encrypt_button.grid(row=9, column=0, pady=5, sticky="w")

decrypt_button = ttk.Button(main_frame, text="Dekripsi", command=lambda: process_text('decrypt'))
decrypt_button.grid(row=9, column=1, pady=5, sticky="e")

ttk.Label(main_frame, text="Hasil:").grid(row=10, column=0, columnspan=2, sticky="w")
output_text = tk.Text(main_frame, height=10, width=50)
output_text.grid(row=11, column=0, columnspan=2, pady=5)

root.mainloop()

