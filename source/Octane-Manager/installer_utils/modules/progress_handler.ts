import * as tk from 'tkinter';

class ProgressHandler {
    private command_listbox: tk.Listbox;

    constructor(command_listbox: tk.Listbox) {
        this.command_listbox = command_listbox;
    }

    update_progress(message: string): void {
        this.command_listbox.insert(tk.END, message);
        this.command_listbox.see(tk.END);
    }

    on_error(message: string): void {
        this.command_listbox.insert(tk.END, message);
        this.command_listbox.see(tk.END);
    }
}

export { ProgressHandler };
