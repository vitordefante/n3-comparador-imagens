import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# ================================================================
#  FUNÇÃO PRINCIPAL DE COMPARAÇÃO ENTRE IMAGENS
# ================================================================
def comparar_imagens(origem_path, destino_path):
    LIMIAR_L2 = 0.85
    MIN_INLIERS = 10

    try:
        img_gray1 = cv2.imread(origem_path, cv2.IMREAD_GRAYSCALE)
        img_gray2 = cv2.imread(destino_path, cv2.IMREAD_GRAYSCALE)

        img_color1 = cv2.imread(origem_path)
        img_color2 = cv2.imread(destino_path)

        if img_gray1 is None or img_gray2 is None:
            raise IOError("Falha ao carregar uma das imagens.")

    except Exception as erro:
        messagebox.showerror("Erro ao abrir arquivo", str(erro))
        return None

    # Detector ORB
    orb = cv2.ORB_create(nfeatures=10000)
    kps1, desc1 = orb.detectAndCompute(img_gray1, None)
    kps2, desc2 = orb.detectAndCompute(img_gray2, None)

    # Validação inicial
    if desc1 is None or desc2 is None or len(desc1) < 2 or len(desc2) < 2:
        return cv2.drawMatches(img_color1, kps1, img_color2, kps2, [], None)

    # BFMatcher + KNN
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches_knn = matcher.knnMatch(desc1, desc2, k=2)

    # Filtro de razão
    correspondencias_boas = []
    for m, n in matches_knn:
        if m.distance < LIMIAR_L2 * n.distance:
            correspondencias_boas.append(m)

    print("Correspondências filtradas:", len(correspondencias_boas))

    if len(correspondencias_boas) > MIN_INLIERS:
        src_pts = np.float32([kps1[m.queryIdx].pt for m in correspondencias_boas]).reshape(-1, 1, 2)
        dst_pts = np.float32([kps2[m.trainIdx].pt for m in correspondencias_boas]).reshape(-1, 1, 2)

        H, mascara = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if mascara is not None:
            mascara_list = mascara.ravel()
            total = int(np.sum(mascara_list))

            print("Inliers:", total)
            if total > MIN_INLIERS:
                print("Imagens compatíveis — MESMO LOCAL detectado")

                # Desenho das linhas válidas
                params = dict(matchColor=(0, 255, 0), matchesMask=mascara_list.tolist(), flags=2)
                img_linhas = cv2.drawMatches(img_color1, kps1, img_color2, kps2, correspondencias_boas, None, **params)

                # Pontos isolados
                pts1_valid = [kps1[m.queryIdx] for i, m in enumerate(correspondencias_boas) if mascara_list[i] == 1]
                pts2_valid = [kps2[m.trainIdx] for i, m in enumerate(correspondencias_boas) if mascara_list[i] == 1]

                img_p1 = cv2.drawKeypoints(img_color1, pts1_valid, None, color=(0, 0, 255))
                img_p2 = cv2.drawKeypoints(img_color2, pts2_valid, None, color=(0, 0, 255))

                h1, w1 = img_p1.shape[:2]
                h2, w2 = img_p2.shape[:2]
                canvas = np.zeros((max(h1, h2), w1 + w2, 3), dtype="uint8")
                canvas[:h1, :w1] = img_p1
                canvas[:h2, w1:w1+w2] = img_p2

                # Salvando resultados
                os.makedirs("resultados", exist_ok=True)
                cv2.imwrite("resultados/linhas.png", img_linhas)
                cv2.imwrite("resultados/pontos.png", canvas)

                print("Resultados salvos em /resultados.")
                return img_linhas

    print("Imagens NÃO correspondem ao mesmo local.")
    return cv2.drawMatches(img_color1, kps1, img_color2, kps2, [], None)

# ================================================================
#  VARIÁVEIS DE CAMINHO
# ================================================================
img1_path = ""
img2_path = ""

# ================================================================
#  FUNÇÕES DA INTERFACE
# ================================================================
def selecionar_img1():
    global img1_path
    arq = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg *.bmp *.tiff")])
    if arq:
        img1_path = arq
        lbl1.config(text=f"Imagem 1: {os.path.basename(arq)}", fg="green")

def selecionar_img2():
    global img2_path
    arq = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg *.bmp *.tiff")])
    if arq:
        img2_path = arq
        lbl2.config(text=f"Imagem 2: {os.path.basename(arq)}", fg="green")

def processar():
    if not img1_path or not img2_path:
        messagebox.showwarning("Aviso", "Selecione as duas imagens antes de continuar.")
        return

    status.config(text="Processando...", fg="blue")
    janela.update_idletasks()

    saida = comparar_imagens(img1_path, img2_path)
    if saida is None:
        status.config(text="Erro ao processar.", fg="red")
        return

    status.config(text="Concluído! Verifique a pasta /resultados.", fg="green")

    # Redimensionamento
    max_w = 1200
    h, w = saida.shape[:2]
    if w > max_w:
        scale = max_w / w
        saida = cv2.resize(saida, (max_w, int(h * scale)))

    rgb = cv2.cvtColor(saida, cv2.COLOR_BGR2RGB)
    tk_img = ImageTk.PhotoImage(Image.fromarray(rgb))

    painel.config(image=tk_img)
    painel.image = tk_img

# ================================================================
#  INTERFACE GRÁFICA
# ================================================================
janela = tk.Tk()
janela.title("Comparação Visual — ORB + RANSAC")
janela.geometry("1280x800")

# Topo
top = tk.Frame(janela, pady=10)
top.pack()

btn1 = tk.Button(top, text="Imagem 1", width=20, command=selecionar_img1)
btn1.pack(side=tk.LEFT, padx=10)

lbl1 = tk.Label(top, text="Nenhuma", width=30, fg="gray")
lbl1.pack(side=tk.LEFT)

btn2 = tk.Button(top, text="Imagem 2", width=20, command=selecionar_img2)
btn2.pack(side=tk.LEFT, padx=10)

lbl2 = tk.Label(top, text="Nenhuma", width=30, fg="gray")
lbl2.pack(side=tk.LEFT)

# Botão principal
wrapper_btn = tk.Frame(janela, pady=10)
wrapper_btn.pack()

btn_exec = tk.Button(
    wrapper_btn,
    text="Comparar",
    command=processar,
    width=30,
    height=2,
    bg="#4A90E2",
    fg="white",
    font=("Arial", 12, "bold")
)
btn_exec.pack()

status = tk.Label(janela, text="Aguardando seleção...", font=("Arial", 10))
status.pack(pady=5)

# Área de resultado
frame = tk.Frame(janela, bg="#333", relief=tk.SUNKEN, borderwidth=1)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

painel = tk.Label(frame, bg="#333")
painel.pack(fill=tk.BOTH, expand=True)

janela.mainloop()
