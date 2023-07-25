import cv2
from pyzbar import pyzbar
import matplotlib.pyplot as plt

def ler_qrcode():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao acessar a câmera. Verifique se a câmera está conectada e funcionando corretamente.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar o quadro.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            text = f"Tipo: {barcode_type}, Dados: {barcode_data}"
            print(text)

        # Exibir o quadro usando o matplotlib com o backend TkAgg
        plt.switch_backend('TkAgg')
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_rgb)
        plt.title("Leitor QR")
        plt.axis("off")
        plt.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

ler_qrcode()
