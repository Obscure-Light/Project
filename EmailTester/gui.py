"""
File gui.py
Contiene la definizione dell'interfaccia grafica (Tkinter) migliorata e la logica di controllo
per raccogliere i dati e invocare la funzione di invio email.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import smtplib
import os
import time

from email_service import invia_email, valida_email_indirizzi

# Variabili globali
attachments = []
MIN_DELAY_SECONDS = 1

def avvia_gui():
    root = tk.Tk()
    root.title("Email Tester - SMTP/API con Token")
    root.geometry("900x700")
    root.resizable(True, True)
    root.minsize(800, 600)

    # Variabili controllate da Tk
    var_token_required = tk.BooleanVar(value=False)
    var_starttls_25 = tk.BooleanVar(value=False)
    var_starttls_587 = tk.BooleanVar(value=True)  # Default a 587
    var_smtps_465 = tk.BooleanVar(value=False)
    var_auth_method = tk.StringVar(value="smtp")  # Default SMTP
    body_format = tk.StringVar(value="plain")
    var_multi_count = tk.IntVar(value=1)
    var_multi_delay = tk.DoubleVar(value=MIN_DELAY_SECONDS)

    # Stile per una GUI più moderna
    style = ttk.Style()
    style.theme_use('clam')

    # Configurazione del canvas scorrevole
    main_container = ttk.Frame(root)
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind mousewheel per scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame principale con padding
    main_frame = ttk.Frame(scrollable_frame, padding="20")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Configurazione colonne per una migliore distribuzione
    main_frame.columnconfigure(1, weight=1)

    row = 0

    # === SEZIONE DATI EMAIL ===
    email_frame = ttk.LabelFrame(main_frame, text="📧 Dati Email", padding="10")
    email_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    email_frame.columnconfigure(1, weight=1)

    ttk.Label(email_frame, text="Mittente (From):").grid(row=0, column=0, sticky="e", padx=(0, 10))
    entry_from = ttk.Entry(email_frame, width=40)
    entry_from.grid(row=0, column=1, sticky="ew", pady=2)

    ttk.Label(email_frame, text="Nome Visualizzato:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    entry_nickname = ttk.Entry(email_frame, width=40)
    entry_nickname.grid(row=1, column=1, sticky="ew", pady=2)

    ttk.Label(email_frame, text="Destinatario (To):").grid(row=2, column=0, sticky="e", padx=(0, 10))
    entry_to = ttk.Entry(email_frame, width=40)
    entry_to.grid(row=2, column=1, sticky="ew", pady=2)

    ttk.Label(email_frame, text="Cc (separati da virgola):").grid(row=3, column=0, sticky="e", padx=(0, 10))
    entry_cc = ttk.Entry(email_frame, width=40)
    entry_cc.grid(row=3, column=1, sticky="ew", pady=2)

    ttk.Label(email_frame, text="Bcc (separati da virgola):").grid(row=4, column=0, sticky="e", padx=(0, 10))
    entry_bcc = ttk.Entry(email_frame, width=40)
    entry_bcc.grid(row=4, column=1, sticky="ew", pady=2)

    ttk.Label(email_frame, text="Oggetto:").grid(row=5, column=0, sticky="e", padx=(0, 10))
    entry_subject = ttk.Entry(email_frame, width=40)
    entry_subject.grid(row=5, column=1, sticky="ew", pady=2)

    # Formato corpo
    format_frame = ttk.Frame(email_frame)
    format_frame.grid(row=6, column=1, sticky="w", pady=5)
    ttk.Label(email_frame, text="Formato:").grid(row=6, column=0, sticky="e", padx=(0, 10))
    ttk.Radiobutton(format_frame, text="Testo", value="plain", variable=body_format).pack(side="left", padx=(0, 10))
    ttk.Radiobutton(format_frame, text="HTML", value="html", variable=body_format).pack(side="left")

    # Corpo email
    ttk.Label(email_frame, text="Corpo del messaggio:").grid(row=7, column=0, sticky="ne", padx=(0, 10), pady=(5, 0))
    text_frame = ttk.Frame(email_frame)
    text_frame.grid(row=7, column=1, sticky="ew", pady=5)
    text_frame.columnconfigure(0, weight=1)
    
    text_body = tk.Text(text_frame, width=50, height=8, wrap="word")
    text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_body.yview)
    text_body.configure(yscrollcommand=text_scrollbar.set)
    text_body.grid(row=0, column=0, sticky="ew")
    text_scrollbar.grid(row=0, column=1, sticky="ns")

    row += 1

    # === SEZIONE SERVER SMTP ===
    server_frame = ttk.LabelFrame(main_frame, text="🖥️ Configurazione Server", padding="10")
    server_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    server_frame.columnconfigure(1, weight=1)

    ttk.Label(server_frame, text="Server SMTP:").grid(row=0, column=0, sticky="e", padx=(0, 10))
    entry_smtp_server = ttk.Entry(server_frame, width=40)
    entry_smtp_server.grid(row=0, column=1, sticky="ew", pady=2)

    ttk.Label(server_frame, text="Porta:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    entry_port = ttk.Entry(server_frame, width=40)
    entry_port.grid(row=1, column=1, sticky="ew", pady=2)
    entry_port.insert(0, "587")  # Default

    # Protocolli
    protocol_frame = ttk.Frame(server_frame)
    protocol_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

    def update_port_and_mode():
        """Aggiorna la porta e la modalità in base alla selezione dell'utente."""
        if var_starttls_25.get():
            var_starttls_587.set(False)
            var_smtps_465.set(False)
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "25")
        elif var_starttls_587.get():
            var_starttls_25.set(False)
            var_smtps_465.set(False)
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "587")
        elif var_smtps_465.get():
            var_starttls_25.set(False)
            var_starttls_587.set(False)
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "465")

    ttk.Checkbutton(protocol_frame, text="STARTTLS (porta 25)", 
                   variable=var_starttls_25, command=update_port_and_mode).pack(anchor="w")
    ttk.Checkbutton(protocol_frame, text="STARTTLS (porta 587)", 
                   variable=var_starttls_587, command=update_port_and_mode).pack(anchor="w")
    ttk.Checkbutton(protocol_frame, text="SMTPS (porta 465)", 
                   variable=var_smtps_465, command=update_port_and_mode).pack(anchor="w")

    row += 1

    # === SEZIONE AUTENTICAZIONE ===
    auth_frame = ttk.LabelFrame(main_frame, text="🔐 Autenticazione", padding="10")
    auth_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    auth_frame.columnconfigure(1, weight=1)

    def on_auth_method_change():
        """Modifica lo stato dei campi in base al metodo di autenticazione selezionato."""
        auth_method = var_auth_method.get()
        token_required = var_token_required.get()

        # Reset stati
        widgets_smtp = [entry_username, entry_password]
        widgets_api = [entry_api_key, entry_api_secret, check_token_req]
        widgets_token = [entry_url_token]
        widgets_api_url = [entry_url_send]

        for widget in widgets_smtp + widgets_api + widgets_token + widgets_api_url:
            widget.config(state="disabled")

        if auth_method == "smtp":
            for widget in widgets_smtp:
                widget.config(state="normal")
        elif auth_method == "api":
            for widget in widgets_api:
                widget.config(state="normal")
            for widget in widgets_api_url:
                widget.config(state="normal")
            if token_required:
                for widget in widgets_token:
                    widget.config(state="normal")

    # Radio buttons per metodo autenticazione
    auth_method_frame = ttk.Frame(auth_frame)
    auth_method_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
    
    ttk.Radiobutton(auth_method_frame, text="Nessuna autenticazione", 
                   variable=var_auth_method, value="none", 
                   command=on_auth_method_change).pack(anchor="w")
    ttk.Radiobutton(auth_method_frame, text="SMTP (Username/Password)", 
                   variable=var_auth_method, value="smtp", 
                   command=on_auth_method_change).pack(anchor="w")
    ttk.Radiobutton(auth_method_frame, text="API con Token", 
                   variable=var_auth_method, value="api", 
                   command=on_auth_method_change).pack(anchor="w")

    # Credenziali SMTP
    ttk.Label(auth_frame, text="Username:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    entry_username = ttk.Entry(auth_frame, width=40)
    entry_username.grid(row=1, column=1, sticky="ew", pady=2)

    ttk.Label(auth_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=(0, 10))
    entry_password = ttk.Entry(auth_frame, width=40, show="*")
    entry_password.grid(row=2, column=1, sticky="ew", pady=2)

    # Credenziali API
    ttk.Label(auth_frame, text="API Key:").grid(row=3, column=0, sticky="e", padx=(0, 10))
    entry_api_key = ttk.Entry(auth_frame, width=40)
    entry_api_key.grid(row=3, column=1, sticky="ew", pady=2)

    ttk.Label(auth_frame, text="API Secret:").grid(row=4, column=0, sticky="e", padx=(0, 10))
    entry_api_secret = ttk.Entry(auth_frame, width=40, show="*")
    entry_api_secret.grid(row=4, column=1, sticky="ew", pady=2)

    check_token_req = ttk.Checkbutton(auth_frame, text="Richiede Token OAuth", 
                                     variable=var_token_required, command=on_auth_method_change)
    check_token_req.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

    ttk.Label(auth_frame, text="URL Token:").grid(row=6, column=0, sticky="e", padx=(0, 10))
    entry_url_token = ttk.Entry(auth_frame, width=40)
    entry_url_token.grid(row=6, column=1, sticky="ew", pady=2)

    ttk.Label(auth_frame, text="URL Send:").grid(row=7, column=0, sticky="e", padx=(0, 10))
    entry_url_send = ttk.Entry(auth_frame, width=40)
    entry_url_send.grid(row=7, column=1, sticky="ew", pady=2)

    row += 1

    # === SEZIONE ALLEGATI ===
    attachments_frame = ttk.LabelFrame(main_frame, text="📎 Allegati", padding="10")
    attachments_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    attachments_frame.columnconfigure(1, weight=1)

    def attach_file():
        """Permette all'utente di selezionare e allegare un file."""
        file_paths = filedialog.askopenfilenames(
            title="Seleziona file da allegare",
            filetypes=[("Tutti i file", "*.*"), ("Documenti", "*.pdf;*.doc;*.docx"), 
                      ("Immagini", "*.jpg;*.jpeg;*.png;*.gif"), ("Archivi", "*.zip;*.rar")]
        )
        if file_paths:
            for file_path in file_paths:
                if file_path not in attachments:
                    attachments.append(file_path)
            update_attachments_display()

    def remove_selected_attachment():
        """Rimuove l'allegato selezionato."""
        selection = listbox_attachments.curselection()
        if selection:
            index = selection[0]
            attachments.pop(index)
            update_attachments_display()
        else:
            messagebox.showwarning("Selezione", "Seleziona un allegato da rimuovere.")

    def remove_all_attachments():
        """Rimuove tutti gli allegati."""
        if attachments and messagebox.askyesno("Conferma", "Rimuovere tutti gli allegati?"):
            attachments.clear()
            update_attachments_display()

    def update_attachments_display():
        """Aggiorna la visualizzazione degli allegati."""
        listbox_attachments.delete(0, tk.END)
        total_size = 0
        for file_path in attachments:
            filename = os.path.basename(file_path)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
                listbox_attachments.insert(tk.END, f"{filename} ({size_str})")
            except:
                listbox_attachments.insert(tk.END, f"{filename} (file non trovato)")
        
        if total_size > 0:
            total_str = f"{total_size/1024:.1f} KB" if total_size < 1024*1024 else f"{total_size/(1024*1024):.1f} MB"
            lbl_total_size.config(text=f"Dimensione totale: {total_str}")
        else:
            lbl_total_size.config(text="")

    # Buttons per allegati
    attachments_buttons = ttk.Frame(attachments_frame)
    attachments_buttons.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
    
    ttk.Button(attachments_buttons, text="Aggiungi File", command=attach_file).pack(side="left", padx=(0, 5))
    ttk.Button(attachments_buttons, text="Rimuovi Selezionato", command=remove_selected_attachment).pack(side="left", padx=(0, 5))
    ttk.Button(attachments_buttons, text="Rimuovi Tutti", command=remove_all_attachments).pack(side="left")

    # Listbox per allegati
    attachments_list_frame = ttk.Frame(attachments_frame)
    attachments_list_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
    attachments_list_frame.columnconfigure(0, weight=1)

    listbox_attachments = tk.Listbox(attachments_list_frame, height=4)
    attachments_scrollbar = ttk.Scrollbar(attachments_list_frame, orient="vertical", command=listbox_attachments.yview)
    listbox_attachments.configure(yscrollcommand=attachments_scrollbar.set)
    listbox_attachments.grid(row=0, column=0, sticky="ew")
    attachments_scrollbar.grid(row=0, column=1, sticky="ns")

    lbl_total_size = ttk.Label(attachments_frame, text="", foreground="gray")
    lbl_total_size.grid(row=2, column=0, columnspan=2, sticky="w")

    row += 1

    # === SEZIONE AZIONI ===
    actions_frame = ttk.LabelFrame(main_frame, text="⚡ Azioni", padding="10")
    actions_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    multi_frame = ttk.Frame(actions_frame)
    multi_frame.pack(fill="x", pady=5)
    ttk.Label(multi_frame, text="Invii multipli:").grid(row=0, column=0, sticky="w")
    ttk.Entry(multi_frame, textvariable=var_multi_count, width=8).grid(row=0, column=1, padx=(5, 15))
    ttk.Label(multi_frame, text="Attesa (s):").grid(row=0, column=2, sticky="e")
    ttk.Entry(multi_frame, textvariable=var_multi_delay, width=8).grid(row=0, column=3, padx=(5, 0))
    ttk.Label(multi_frame, text=f"(min {MIN_DELAY_SECONDS}s)", foreground="gray").grid(row=0, column=4, padx=(8, 0))

    def test_connection():
        """Testa la connessione al server SMTP."""
        smtp_server = entry_smtp_server.get().strip()
        smtp_port = entry_port.get().strip()
        
        if not smtp_server:
            lbl_result.config(text="❌ Inserire il server SMTP", foreground="red")
            return
            
        try:
            smtp_port = int(smtp_port)
        except ValueError:
            lbl_result.config(text="❌ La porta deve essere un numero", foreground="red")
            return

        try:
            lbl_result.config(text="🔄 Test connessione in corso...", foreground="blue")
            root.update()
            
            if var_smtps_465.get():
                server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                if var_starttls_25.get() or var_starttls_587.get():
                    server.starttls()
            
            server.ehlo()
            server.quit()
            lbl_result.config(text="✅ Connessione al server riuscita!", foreground="green")
        except Exception as e:
            lbl_result.config(text=f"❌ Errore di connessione: {str(e)}", foreground="red")

    def validate_form():
        """Valida i dati del form prima dell'invio."""
        errors = []

        auth_method = var_auth_method.get()
        if not entry_from.get().strip():
            errors.append("Mittente richiesto")
        if not entry_to.get().strip():
            errors.append("Destinatario richiesto")

        valido_email, msg_email = valida_email_indirizzi(
            entry_from.get().strip(),
            entry_to.get().strip(),
            entry_cc.get().strip(),
            entry_bcc.get().strip(),
        )
        if not valido_email:
            errors.append(msg_email)

        if auth_method in ("smtp", "none"):
            if not entry_smtp_server.get().strip():
                errors.append("Server SMTP richiesto")
            if not entry_port.get().strip():
                errors.append("Porta richiesta")

        if auth_method == "smtp":
            if not entry_username.get().strip() or not entry_password.get().strip():
                errors.append("Username e password richiesti per SMTP")
        elif auth_method == "api":
            if not entry_url_send.get().strip():
                errors.append("URL Send richiesto per invio API")
            if var_token_required.get():
                if not entry_api_key.get().strip() or not entry_api_secret.get().strip():
                    errors.append("API Key e Secret richiesti quando è necessario il token")
                if not entry_url_token.get().strip():
                    errors.append("URL Token richiesto per ottenere il token")

        try:
            if var_multi_count.get() < 1:
                errors.append("Numero invii multipli deve essere almeno 1")
        except tk.TclError:
            errors.append("Numero invii multipli non valido")

        try:
            if var_multi_delay.get() < MIN_DELAY_SECONDS:
                errors.append(f"Attesa minima tra gli invii: {MIN_DELAY_SECONDS} secondi")
        except tk.TclError:
            errors.append("Tempo di attesa non valido")

        return errors

    def perform_send_once():
        return invia_email(
            sender=entry_from.get().strip(),
            recipient=entry_to.get().strip(),
            cc=entry_cc.get().strip(),
            bcc=entry_bcc.get().strip(),
            subject=entry_subject.get().strip(),
            body=text_body.get("1.0", tk.END).strip(),
            nickname=entry_nickname.get().strip(),
            smtp_server=entry_smtp_server.get().strip(),
            smtp_port=entry_port.get().strip(),
            username=entry_username.get().strip(),
            password=entry_password.get().strip(),
            url_token=entry_url_token.get().strip(),
            url_send=entry_url_send.get().strip(),
            api_key=entry_api_key.get().strip(),
            api_secret=entry_api_secret.get().strip(),
            starttls_25=var_starttls_25.get(),
            starttls_587=var_starttls_587.get(),
            smtps_465=var_smtps_465.get(),
            auth_method=var_auth_method.get(),
            token_required=var_token_required.get(),
            body_format=body_format.get(),
            attachments=attachments
        )

    def validate_before_send() -> bool:
        errors = validate_form()
        if errors:
            messagebox.showerror("Errori di validazione", "\n".join(f"• {error}" for error in errors))
            return False

        # Conferma invio se ci sono allegati pesanti
        total_size = sum(os.path.getsize(f) for f in attachments if os.path.exists(f))
        if total_size > 10 * 1024 * 1024:  # 10 MB
            if not messagebox.askyesno("Conferma", f"Gli allegati pesano {total_size/(1024*1024):.1f} MB. Continuare?"):
                return False
        return True

    def send_email():
        """Invia una singola email."""
        if not validate_before_send():
            return

        lbl_result.config(text="📤 Invio in corso...", foreground="blue")
        root.update()

        risultato = perform_send_once()

        # Visualizzazione risultato
        if "successo" in risultato.lower():
            lbl_result.config(text=f"✅ {risultato}", foreground="green")
            if messagebox.askyesno("Successo", f"{risultato}\n\nVuoi pulire il form?"):
                clear_form()
        else:
            lbl_result.config(text=f"❌ {risultato}", foreground="red")
            messagebox.showerror("Errore", risultato)

    def send_multiple():
        """Esegue invii multipli con attesa configurabile."""
        if not validate_before_send():
            return

        try:
            total = int(var_multi_count.get())
        except (ValueError, tk.TclError):
            messagebox.showerror("Errore", "Numero di invii non valido")
            return

        try:
            delay = float(var_multi_delay.get())
        except (ValueError, tk.TclError):
            messagebox.showerror("Errore", "Tempo di attesa non valido")
            return

        if total < 1:
            messagebox.showerror("Errore", "Il numero di invii deve essere almeno 1")
            return
        if delay < MIN_DELAY_SECONDS:
            messagebox.showerror("Errore", f"Il tempo di attesa minimo è {MIN_DELAY_SECONDS} secondi")
            return

        successi = 0
        falliti = []

        for index in range(total):
            lbl_result.config(text=f"📤 Invio {index + 1}/{total}...", foreground="blue")
            root.update()
            risultato = perform_send_once()
            if "successo" in risultato.lower():
                successi += 1
            else:
                falliti.append(f"#{index + 1}: {risultato}")

            if index < total - 1:
                time.sleep(delay)

        summary = f"Inviate {successi} email su {total}."
        if falliti:
            summary += "\n\nErrori:\n" + "\n".join(falliti)

        if falliti:
            lbl_result.config(text=f"⚠️ {summary}", foreground="orange")
            messagebox.showwarning("Invio multiplo", summary)
        else:
            lbl_result.config(text=f"✅ {summary}", foreground="green")
            messagebox.showinfo("Invio multiplo", summary)

    def clear_form():
        """Pulisce tutti i campi del form."""
        entry_from.delete(0, tk.END)
        entry_nickname.delete(0, tk.END)
        entry_to.delete(0, tk.END)
        entry_cc.delete(0, tk.END)
        entry_bcc.delete(0, tk.END)
        entry_subject.delete(0, tk.END)
        text_body.delete("1.0", tk.END)
        attachments.clear()
        update_attachments_display()
        lbl_result.config(text="")

    # Buttons azioni
    actions_buttons = ttk.Frame(actions_frame)
    actions_buttons.pack(pady=10)

    ttk.Button(actions_buttons, text="🔍 Test Connessione", command=test_connection).pack(side="left", padx=(0, 10))
    ttk.Button(actions_buttons, text="📧 Invia Email", command=send_email).pack(side="left", padx=(0, 10))
    ttk.Button(actions_buttons, text="📨 Invio Multiplo", command=send_multiple).pack(side="left", padx=(0, 10))
    ttk.Button(actions_buttons, text="🗑️ Pulisci Form", command=clear_form).pack(side="left")

    # Label risultato
    lbl_result = ttk.Label(actions_frame, text="", font=("TkDefaultFont", 10, "bold"))
    lbl_result.pack(pady=10)

    # Inizializzazione
    on_auth_method_change()
    update_attachments_display()

    # Focus sul primo campo
    entry_from.focus()

    root.mainloop()
