import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import serial

# Inicializar a comunicação serial com o Arduino (ajuste a porta conforme necessário)
arduino = serial.Serial('COM3', 9600)  # Verifique a porta correta do Arduino

# Lista de horários de alimentação
alimentar = ["05:00:00", "11:30:00", "17:00:00", "22:00:00"]

def check_horas_alimentar(hora_atual):
    if hora_atual in alimentar:
        arduino.write(b'F\n')  # Envia o comando para liberar ração
        

def resetar_leds(hora_atual):
    if hora_atual == "23:50:00":
        arduino.write(b'RESET\n')  # Envia o comando para resetar os LEDs

def atualizar_relogio():
    hora_atual = time.strftime("%H:%M:%S")
    label.config(text=hora_atual)
    check_horas_alimentar(hora_atual)
    resetar_leds(hora_atual)
    arduino.write((hora_atual + '\n').encode())  # Envia o horário atual para o Arduino
    root.after(1000, atualizar_relogio)  # Atualiza o relógio a cada 1000 milissegundos (1 segundo)

# Criar a janela principal
root = tk.Tk()
root.title("Relógio 24 horas com Alertas de Alimentação")
root.geometry("350x150")  # Largura x Altura

# Criar um rótulo (label) para exibir o tempo
label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="white")
label.pack(expand=True)

# Iniciar a atualização do relógio
atualizar_relogio()

# Iniciar o loop principal
root.mainloop()

# Fechar a comunicação serial quando o programa for encerrado
arduino.close()
