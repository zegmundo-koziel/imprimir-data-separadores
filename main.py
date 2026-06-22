import datetime
import os
import sys
import tkinter as tk
from tkcalendar import Calendar
import win32con
import win32print
import win32ui
import winshell


def criar_atalho_na_area_de_trabalho():
    if hasattr(sys, "frozen"):
        caminho_exe = sys.executable
        nome_programa = "Imprimir Data.lnk"
        caminho_desktop = os.path.join(winshell.desktop(), nome_programa)

        if not os.path.exists(caminho_desktop):
            try:
                pasta_base = getattr(
                    sys, "_MEIPASS", os.path.dirname(caminho_exe)
                )
                caminho_icone = os.path.join(pasta_base, "icone.ico")

                if not os.path.exists(caminho_icone):
                    caminho_icone = caminho_exe

                winshell.CreateShortcut(
                    Path=caminho_desktop,
                    Target=caminho_exe,
                    Icon=(caminho_icone, 0),
                    Description="Aplicativo para impressão de datas em separadores.",
                )
            except Exception as e:
                print(f"Erro ao criar atalho: {e}")


def abrir_calendario():
    # BUG FIX: Bloqueia o botão de imprimir imediatamente ao abrir o calendário
    btn_imprimir.config(state=tk.DISABLED, bg="#A0A0A0")

    janela_cal = tk.Toplevel(janela)
    janela_cal.title("Selecionar Data")
    janela_cal.geometry("300x320")
    janela_cal.resizable(False, False)

    # Garante que se o usuário fechar o calendário no "X" sem confirmar, o botão reativa
    def ao_fechar_calendario():
        btn_imprimir.config(state=tk.NORMAL, bg="#2ECC71")
        janela_cal.destroy()

    janela_cal.protocol("WM_DELETE_WINDOW", ao_fechar_calendario)

    cal = Calendar(
        janela_cal,
        selectmode="day",
        locale="pt_BR",
        date_pattern="dd/mm/yyyy",
    )
    cal.pack(pady=20, fill="both", expand=True)

    def confirmar_data():
        data_selecionada = cal.get_date()
        label_data.config(text=data_selecionada)

        # BUG FIX: Reativa o botão de imprimir com a cor verde original após confirmar
        btn_imprimir.config(state=tk.NORMAL, bg="#2ECC71")
        janela_cal.destroy()

    btn_confirmar = tk.Button(
        janela_cal,
        text="Confirmar",
        command=confirmar_data,
        bg="#2196F3",
        fg="white",
        font=("Calibri", 11, "bold"),
        relief="flat",
        pady=5,
    )
    btn_confirmar.pack(pady=10)


def imprimir_texto():
    data_para_imprimir = label_data.cget("text")

    try:
        nome_impressora = win32print.GetDefaultPrinter()

        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(nome_impressora)

        hdc.StartDoc("Impressão de Data")
        hdc.StartPage()

        fonte = win32ui.CreateFont(
            {
                "name": "Arial",
                "height": -900,
                "weight": win32con.FW_BOLD,
            }
        )
        hdc.SelectObject(fonte)

        largura_pagina = hdc.GetDeviceCaps(win32con.HORZRES)
        altura_pagina = hdc.GetDeviceCaps(win32con.VERTRES)

        def desenhar_texto_centralizado(hdc, texto, y_pos):
            largura_texto = hdc.GetTextExtent(texto)[0]
            x_pos = int((largura_pagina - largura_texto) / 2)
            hdc.TextOut(x_pos, y_pos, texto)

        posicao_superior = int(altura_pagina * 0.18)
        posicao_inferior = int(altura_pagina * 0.65)

        desenhar_texto_centralizado(hdc, data_para_imprimir, posicao_superior)
        desenhar_texto_centralizado(hdc, data_para_imprimir, posicao_inferior)

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

    except Exception as e:
        print(f"Erro ao enviar diretamente para a impressora: {e}")


criar_atalho_na_area_de_trabalho()

janela = tk.Tk()
janela.title("Imprimir Data")
janela.geometry("600x400")
janela.configure(bg="#F9F9F9")
janela.resizable(False, False)

data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

container = tk.Frame(janela, bg="#F9F9F9")
container.pack(expand=True)

label_data = tk.Label(
    container,
    text=data_atual,
    font=("Calibri", 54, "bold"),
    bg="#F9F9F9",
    fg="#2C3E50",
)
label_data.pack(pady=10)

frame_botoes = tk.Frame(janela, bg="#F9F9F9")
frame_botoes.pack(side="bottom", pady=40)

btn_calendario = tk.Button(
    frame_botoes,
    text="Selecionar Data 📅",
    font=("Calibri", 12),
    command=abrir_calendario,
    bg="#FFFFFF",
    fg="#2C3E50",
    relief="groove",
    padx=15,
    pady=5,
)
btn_calendario.pack(side="left", padx=15)

btn_imprimir = tk.Button(
    frame_botoes,
    text="Imprimir 🖨️",
    font=("Calibri", 12, "bold"),
    command=imprimir_texto,
    bg="#2ECC71",
    fg="white",
    relief="flat",
    padx=20,
    pady=6,
)
btn_imprimir.pack(side="left", padx=15)

janela.mainloop()
