# Imprimir Data - Gerador de Separadores 🖨️

Este é um utilitário desenvolvido em Python para otimizar e automatizar a criação de separadores físicos de arquivos em folhas A4. O aplicativo exibe uma interface limpa, preenche automaticamente a data atual e faz a impressão duplicada e estrategicamente espaçada para dobras perfeitas.

## 🚀 Funcionalidades

* **Preenchimento automático**: Inicia com o dia atual do sistema.
* **Bloqueio de segurança (Bug Fix)**: Trava o botão de impressão de forma automática enquanto a janela do calendário estiver aberta, evitando impressões acidentais.
* **Impressão nativa e silenciosa**: Comunicação direta com a API do Windows (sem abrir telas de navegadores ou PDFs em segundo plano).
* **Layout otimizado para arquivos**: Imprime duas datas com fonte gigante (tamanho 105) centralizadas nas metades superior e inferior da folha A4 para servir como divisor.

## 🛠️ Tecnologias Utilizadas

* [Python](https://python.org)
* Tkinter (Interface Gráfica)
* `tkcalendar` (Seletor de datas nativo)
* `pywin32` (Comunicação direta com a API de impressão do Windows)

## 📦 Como gerar o Executável (.exe)

Caso precise gerar o executável novamente a partir do código fonte, utilize o comando do PyInstaller abaixo com a pasta limpa:

```bash
pyinstaller --noconsole --onefile --icon=icone.ico --add-data "icone.ico;." -n imprimir_data main.py
```
