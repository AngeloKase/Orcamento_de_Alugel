# PARTE 1/2
import csv
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pathlib import Path
import customtkinter as ctk

# ---------- CONFIGURAÇÃO DO TEMA ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def get_downloads_folder():
    try:
        home = Path.home()
        return home / "Downloads"
    except Exception:
        return Path.home()


class LocadoraGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1250x760")
        self.minsize(1100, 680)
        self.update_idletasks()
        self.title("Locadora de Imóveis — Sistema de Orçamento")


        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w, win_h = 1250, 760
        x = int((screen_w / 2) - (win_w / 2))
        y = int((screen_h / 2) - (win_h / 2))
        self.geometry(f"{win_w}x{win_h}+{x}+{y}")


        # Valores base
        self.apartamento = 700
        self.casa = 900
        self.estudio = 1200
        self.quarto_casa = 250
        self.quarto_apartamento = 200
        self.vaga = 300
        self.estudio_vaga = 250  # pacote 2 vagas para estúdio
        self.vaga_extra_valor = 60
        self.contrato = 2000
        self.desconto = 5  # 5%

        # Variáveis de estado
        self.nome_cliente = ctk.StringVar()
        self.imovel = ctk.IntVar(value=0)  # 1=casa 2=apart 3=estudio
        self.quarto_choice = ctk.StringVar(value="Não")
        self.vaga_choice = ctk.StringVar(value="Não")
        self.tem_crianca_choice = ctk.StringVar(value="Sim")
        self.estudio_duas_vagas = ctk.StringVar(value="Não")
        self.vaga_extra_qtd = ctk.IntVar(value=0)
        self.parcelas = ctk.IntVar(value=1)

        self.step_index = 0
        self.frames = []

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        header = ctk.CTkFrame(self, height=80, corner_radius=0)
        header.pack(fill="x")
    
        ctk.CTkLabel(header, text="Locadora de Imóveis",
                     font=ctk.CTkFont(size=28, weight="bold")).place(relx=0.02, rely=0.18)

        ctk.CTkLabel(header,
                     text="Orçamento mensal personalizado — passo a passo",
                     font=ctk.CTkFont(size=14)).place(relx=0.02, rely=0.62)

        self.total_label = ctk.CTkButton(
            header,
            text="💰 Total: R$ 0,00",
            width=230,
            height=40,
            fg_color="#1f6aa5",
            hover_color="#2ea9ff",
            state="disabled",
            command=self._mostrar_detalhes_total
        )
        self.total_label.place(relx=0.75, rely=0.25)

        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=20, pady=(12, 10))

        # Cria frames de cada etapa
        f0 = ctk.CTkFrame(content); self.frames.append(f0); self._build_step0(f0)
        f1 = ctk.CTkFrame(content); self.frames.append(f1); self._build_step1(f1)
        f2 = ctk.CTkFrame(content); self.frames.append(f2); self._build_step2(f2)
        f3 = ctk.CTkFrame(content); self.frames.append(f3); self._build_step3(f3)
        f4 = ctk.CTkFrame(content); self.frames.append(f4); self._build_step4(f4)

        # Navegação (botões maiores)
        nav = ctk.CTkFrame(self, height=80)
        nav.pack(fill="x", side="bottom", padx=20, pady=(0, 12))

        self.btn_back = ctk.CTkButton(nav, text="◀ Voltar", command=self.prev_step, width=160, height=50)
        self.btn_back.pack(side="left", padx=12)

        self.btn_next = ctk.CTkButton(nav, text="Próximo ▶", command=self.next_step, width=160, height=50)
        self.btn_next.pack(side="right", padx=12)

        self.show_step(0)

    # ---------- controle de etapas ----------
    def hide_all_frames(self):
        for f in self.frames:
            f.pack_forget()

    def show_step(self, idx):
        self.hide_all_frames()
        self.step_index = idx
        frame = self.frames[idx]
        frame.pack(fill="both", expand=True)

        self.btn_back.configure(state="normal" if idx > 0 else "disabled")
        if idx == len(self.frames) - 1:
            self.btn_next.configure(text="Finalizar", command=self.finalize_and_save)
        else:
            self.btn_next.configure(text="Próximo ▶", command=self.next_step)

    def next_step(self):
        # validações por etapa
        if self.step_index == 0:
            nome = self.nome_cliente.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite o nome do cliente.")
                return
        if self.step_index == 1 and self.imovel.get() not in (1, 2, 3):
            messagebox.showerror("Erro", "Escolha um imóvel antes de prosseguir.")
            return
        self.show_step(min(self.step_index + 1, len(self.frames) - 1))

    def prev_step(self):
        self.show_step(max(self.step_index - 1, 0))

    # ---------- ETAPA 0 (sem botão Iniciar) ----------
    def _build_step0(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(frame, text="Seja Bem-Vindo à Nossa Locadora de Imóveis!",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(frame, text="Digite seu nome para começar:",
                     font=ctk.CTkFont(size=15)).pack(pady=(0, 8))

        # Entrada de nome — NÃO tem botão iniciar; avança com Enter
        entry = ctk.CTkEntry(frame, textvariable=self.nome_cliente, width=520, height=44,
                             font=ctk.CTkFont(size=15))
        entry.pack(pady=6)
        entry.bind("<Return>", lambda e: self._try_advance_from_name())

    def _try_advance_from_name(self):
        nome = self.nome_cliente.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do cliente.")
            return
        # avança para seleção de imóvel
        self.show_step(1)
# PARTE 2/2 (cole logo após a PARTE 1)

    # ---------- ETAPA 1: escolha de imóvel ----------
    def _build_step1(self, parent):
        ctk.CTkLabel(parent, text="Escolha o tipo de imóvel desejado",
                 font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(28, 18))

        frame = ctk.CTkFrame(parent)
        frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Faz as colunas crescerem igualmente
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)

        for i, (txt, val, preco, emoji) in enumerate([
            ("Casa", 1, 900, "🏠"),
            ("Apartamento", 2, 700, "🏢"),
            ("Estúdio", 3, 1200, "🏙️")
        ]):
            btn = ctk.CTkButton(frame, text=f"{emoji}\n{txt}\nR$ {preco}",
                            height=180, font=ctk.CTkFont(size=17, weight="bold"),
                            command=lambda v=val: self._select_imovel(v))
            btn.grid(row=0, column=i, padx=15, pady=18, sticky="nsew")


    def _select_imovel(self, tipo):
        self.imovel.set(tipo)
        self.total_label.configure(state="normal")
        self._update_visibility_by_imovel()
        self._update_resumo()

    # ---------- ETAPA 2: personalização ----------
    def _build_step2(self, parent):
    # Frame principal (centralizado)
        container = ctk.CTkFrame(parent)
        container.place(relx=0.5, rely=0.5, anchor="center")

    # Frame interno que recebe as opções (mantém padding e layout)
        options_frame = ctk.CTkFrame(container)
        options_frame.pack(padx=20, pady=20)

        self.scroll_content = options_frame
        self._populate_personalizacao(options_frame)
    

    def _populate_personalizacao(self, frame):
    
        self.lbl_quarto = ctk.CTkLabel(
            frame, text="Deseja adicionar um quarto a mais? (+R$250)",
            anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.om_quarto = ctk.CTkOptionMenu(
            frame, values=["Sim", "Não"], variable=self.quarto_choice,
            width=200, height=40, font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda _: self._update_resumo()
        )

        self.lbl_vaga = ctk.CTkLabel(
            frame, text="Deseja adicionar uma vaga? (+R$300)",
            anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.om_vaga = ctk.CTkOptionMenu(
            frame, values=["Sim", "Não"], variable=self.vaga_choice,
            width=200, height=40, font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda _: self._update_resumo()
        )

    
        self.lbl_crianca = ctk.CTkLabel(
            frame, text="Tem criança? (Se NÃO, aplica 5% de desconto)",
            anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.om_crianca = ctk.CTkOptionMenu(
            frame, values=["Sim", "Não"], variable=self.tem_crianca_choice,
            width=200, height=40, font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda _: self._update_resumo()
        )

       
        self.lbl_duas_vagas = ctk.CTkLabel(
            frame, text="Estúdio: pacote de 2 vagas? (+R$250)",
            anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.om_duas_vagas = ctk.CTkOptionMenu(
            frame, values=["Sim", "Não"], variable=self.estudio_duas_vagas,
            width=200, height=40, font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda _: self._update_resumo()
        )

        self.lbl_vagas_extra = ctk.CTkLabel(
            frame, text="Vagas extras? (+R$60 cada)",
            anchor="w", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.slider_vagas = ctk.CTkSlider(
            frame, from_=0, to=20, number_of_steps=20,
            variable=self.vaga_extra_qtd,
            command=lambda _: self._update_resumo()
        )
        self.lbl_vagas_val = ctk.CTkLabel(
            frame, textvariable=self.vaga_extra_qtd,
            width=40, font=ctk.CTkFont(size=15, weight="bold")
        )

    # ---- Caixa de resumo (sempre aparece) ----
        self.resumo_text = ctk.CTkTextbox(frame, height=260)
        self.resumo_text.pack(fill="x", padx=20, pady=20)

    # Atualiza visibilidade conforme tipo de imóvel
        self._update_visibility_by_imovel()


    def _update_visibility_by_imovel(self):
        im = self.imovel.get()
        # Esconde todos
        for w in [getattr(self, name) for name in (
                "lbl_quarto", "om_quarto", "lbl_vaga", "om_vaga",
                "lbl_crianca", "om_crianca", "lbl_duas_vagas", "om_duas_vagas",
                "lbl_vagas_extra", "slider_vagas", "lbl_vagas_val") if hasattr(self, name)]:
            try:
                w.pack_forget()
            except Exception:
                pass

        # Mostra conforme tipo
        if im == 1:  # Casa
            self.lbl_quarto.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_quarto.pack(pady=(0, 10), anchor="w", padx=20)
            self.lbl_vaga.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_vaga.pack(pady=(0, 10), anchor="w", padx=20)
        elif im == 2:  # Apartamento
            self.lbl_quarto.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_quarto.pack(pady=(0, 10), anchor="w", padx=20)
            self.lbl_vaga.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_vaga.pack(pady=(0, 10), anchor="w", padx=20)
            self.lbl_crianca.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_crianca.pack(pady=(0, 10), anchor="w", padx=20)
        elif im == 3:  # Estúdio
            # Estúdio não permite quarto extra: apenas pacote e vagas extras
            self.lbl_duas_vagas.pack(pady=(10, 4), anchor="w", padx=20)
            self.om_duas_vagas.pack(pady=(0, 10), anchor="w", padx=20)
            self.lbl_vagas_extra.pack(pady=(10, 4), anchor="w", padx=20)
            self.slider_vagas.pack(pady=(0, 4), anchor="w", padx=20)
            self.lbl_vagas_val.pack(anchor="w", padx=20)

        self._update_resumo()

    def _update_resumo(self):
        # Protege caso o widget ainda não exista
        if not hasattr(self, "resumo_text"):
            return

        im = self.imovel.get()
        nome = self.nome_cliente.get().strip() or "<cliente>"
        total = 0.0
        detalhes = []

        if im == 1:  # Casa
            total += self.casa
            detalhes.append(("Base (Casa)", self.casa))
            if self.quarto_choice.get().lower() in ["sim", "s"]:
                total += self.quarto_casa
                detalhes.append(("Quarto extra", self.quarto_casa))
            if self.vaga_choice.get().lower() in ["sim", "s"]:
                total += self.vaga
                detalhes.append(("Vaga", self.vaga))

        elif im == 2:  # Apartamento
            total += self.apartamento
            detalhes.append(("Base (Apartamento)", self.apartamento))
            if self.quarto_choice.get().lower() in ["sim", "s"]:
                total += self.quarto_apartamento
                detalhes.append(("Quarto extra", self.quarto_apartamento))
            if self.vaga_choice.get().lower() in ["sim", "s"]:
                total += self.vaga
                detalhes.append(("Vaga", self.vaga))
            # desconto por NÃO ter criança
            if self.tem_crianca_choice.get().lower() in ["não", "nao", "n"]:
                desconto_val = self.desconto * total / 100
                total -= desconto_val
                detalhes.append((f"Desconto {self.desconto}%", -desconto_val))

        elif im == 3:  # Estúdio
            total += self.estudio
            detalhes.append(("Base (Estúdio)", self.estudio))
            if self.estudio_duas_vagas.get().lower() in ["sim", "s"]:
                total += self.estudio_vaga
                detalhes.append(("Pacote 2 vagas", self.estudio_vaga))
            extra = self.vaga_extra_qtd.get() * self.vaga_extra_valor
            if extra:
                total += extra
                detalhes.append((f"Vagas extras x{self.vaga_extra_qtd.get()}", extra))

        # Atualiza total no header e o texto do resumo
        self.total_label.configure(text=f"💰 Total: R$ {total:.2f}")
        self.resumo_text.configure(state="normal")
        self.resumo_text.delete("0.0", "end")
        self.resumo_text.insert("0.0", f"Cliente: {nome}\n\n")
        for d in detalhes:
            self.resumo_text.insert("end", f"{d[0]}: R$ {d[1]:.2f}\n")
        self.resumo_text.insert("end", f"\nPrévia do total mensal: R$ {total:.2f}")
        self.resumo_text.configure(state="disabled")

    # ---------- ETAPA 3: Parcelamento ----------
    def _build_step3(self, parent):
        container = ctk.CTkFrame(parent)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="Parcelamento do contrato (R$2000, até 5x)",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        opt = ctk.CTkOptionMenu(container, values=["1", "2", "3", "4", "5"], variable=self.parcelas)
        opt.pack(pady=8)
        ctk.CTkLabel(container, text="(1 = à vista | 2–5 = parcelado)", text_color="#aaa").pack(pady=6)


    # ---------- ETAPA 4: Revisão e Export ----------
    def _build_step4(self, parent):
    
        ctk.CTkLabel(
            parent,
            text="Revisão Final e Exportação CSV",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 5))

   
        ctk.CTkLabel(
            parent,
            text="⚠️ Clique no botão 'Finalizar' antes para gerar e visualizar a tabela de parcelas!",
            text_color="#ffcc00",
            font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=800,  
            justify="center"
        ).pack(pady=(0, 10))

    
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white",
                        rowheight=30,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), foreground="black")

    
        self.tree = ttk.Treeview(
            parent,
            columns=("Mês", "Aluguel Base", "Parcela", "Total"),
            show="headings",
            height=12,
            style="Treeview"
        )
        for c in ("Mês", "Aluguel Base", "Parcela", "Total"):
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=240)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    
        ctk.CTkButton(
            parent,
            text="💾 Baixar CSV (Excel)",
            width=220,
            height=44,
            command=self._save_csv_as
        ).pack(pady=10)


    # ---------- Geração de dados ----------
    def _generate_data(self):
        im = self.imovel.get()
        total = 0.0
        tipo = ""
        if im == 1:
            tipo = "Casa"
            total += self.casa
            if self.quarto_choice.get().lower() in ["sim", "s"]:
                total += self.quarto_casa
            if self.vaga_choice.get().lower() in ["sim", "s"]:
                total += self.vaga
        elif im == 2:
            tipo = "Apartamento"
            total += self.apartamento
            if self.quarto_choice.get().lower() in ["sim", "s"]:
                total += self.quarto_apartamento
            if self.vaga_choice.get().lower() in ["sim", "s"]:
                total += self.vaga
            if self.tem_crianca_choice.get().lower() in ["não", "nao", "n"]:
                total -= self.desconto * total / 100
        elif im == 3:
            tipo = "Estúdio"
            total += self.estudio
            if self.estudio_duas_vagas.get().lower() in ["sim", "s"]:
                total += self.estudio_vaga
            total += self.vaga_extra_qtd.get() * self.vaga_extra_valor

        parcelas = int(self.parcelas.get())
        parc_val = (self.contrato / parcelas) if parcelas > 1 else self.contrato
        meses = []
        for i in range(1, 13):
            parcela_val = f"R$ {parc_val:.2f}" if i <= parcelas else "R$ 0.00"
            total_mes = total + (parc_val if i <= parcelas else 0)
            meses.append([i, f"R$ {total:.2f}", parcela_val, f"R$ {total_mes:.2f}"])
        total_anual = sum(float(m[3].replace("R$ ", "")) for m in meses)
        return meses, total_anual, tipo

    # ---------- Finalizar / preencher tabela ----------
    def finalize_and_save(self):
    
        self.show_step(len(self.frames) - 1)

    
        meses, total_anual, tipo = self._generate_data()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for m in meses:
            self.tree.insert("", "end", values=m)

        messagebox.showinfo("Concluído", f"Total anual: R$ {total_anual:.2f}")


    def _save_csv_as(self):
        meses, total_anual, tipo = self._generate_data()
        nome = self.nome_cliente.get().strip() or "cliente"
        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"orcamento_{nome}.csv",
            filetypes=[("CSV Excel", "*.csv")]
        )
        if not file:
            return
        with open(file, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(["Cliente:", nome])
            w.writerow(["Tipo de imóvel:", tipo])
            w.writerow([])
            w.writerow(["Mês", "Aluguel Base", "Parcela", "Total"])
            w.writerows(meses)
            w.writerow([])
            w.writerow(["", "", "Total Anual:", f"R$ {total_anual:.2f}"])
        messagebox.showinfo("Salvo", f"Arquivo salvo: {file}")

    def _mostrar_detalhes_total(self):
        meses, total, tipo = self._generate_data()
        messagebox.showinfo("Resumo", f"Tipo: {tipo}\nTotal anual estimado: R$ {total:.2f}")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    app = LocadoraGUI()
    app.mainloop()
 