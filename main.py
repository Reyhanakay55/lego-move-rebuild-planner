import tkinter as tk
from tkinter import ttk, messagebox

from database import DatabaseManager


class LegoPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEGO Move & Rebuild Planner")
        self.root.geometry("1000x650")

        self.database = DatabaseManager()
        self.database.create_tables()

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(
            self.root,
            text="LEGO Move & Rebuild Planner",
            font=("Arial", 20)
        )
        title_label.pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(
            form_frame,
            text="Set Name:"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(
            form_frame,
            text="Set Number:"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.set_number_entry = ttk.Entry(form_frame, width=30)
        self.set_number_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(
            form_frame,
            text="Status:"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.status_combo = ttk.Combobox(
            form_frame,
            values=[
                "Complete",
                "Disassembled",
                "Damaged",
                "Rebuilding"
            ],
            state="readonly",
            width=27
        )
        self.status_combo.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(
            form_frame,
            text="Box Number:"
        ).grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.box_entry = ttk.Entry(form_frame, width=30)
        self.box_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(
            form_frame,
            text="Missing Pieces:"
        ).grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.missing_pieces_entry = ttk.Entry(form_frame, width=30)
        self.missing_pieces_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(
            form_frame,
            text="Rebuild Progress (%):"
        ).grid(row=5, column=0, padx=5, pady=5, sticky="e")

        self.progress_entry = ttk.Entry(form_frame, width=30)
        self.progress_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(
            form_frame,
            text="Notes:"
        ).grid(row=6, column=0, padx=5, pady=5, sticky="ne")

        self.notes_text = tk.Text(
            form_frame,
            width=30,
            height=4
        )
        self.notes_text.grid(row=6, column=1, padx=5, pady=5)
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = ttk.Button(
            button_frame,
            text="Add",
            command=self.add_lego_set
        )
        add_button.grid(row=0, column=0, padx=5)

        update_button = ttk.Button(
            button_frame,
            text="Update",
            command=self.update_selected_set
        )
        update_button.grid(row=0, column=1, padx=5)

        delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_selected_set
        )
        delete_button.grid(row=0, column=2, padx=5)

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_table
        )
        refresh_button.grid(row=0, column=3, padx=5)
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)

        ttk.Label(
            filter_frame,
            text="Filter by Status:"
        ).grid(row=0, column=0, padx=5)

        self.filter_combo = ttk.Combobox(
            filter_frame,
            values=[
                "All",
                "Complete",
                "Disassembled",
                "Damaged",
                "Rebuilding"
            ],
            state="readonly",
            width=20
        )
        self.filter_combo.grid(row=0, column=1, padx=5)
        self.filter_combo.set("All")

        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        ) 
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        

        columns = (
            "id",
            "name",
            "set_number",
            "status",
            "box_number",
            "missing_pieces",
            "rebuild_progress"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Set Name")
        self.tree.heading("set_number", text="Set Number")
        self.tree.heading("status", text="Status")
        self.tree.heading("box_number", text="Box")
        self.tree.heading("missing_pieces", text="Missing Pieces")
        self.tree.heading("rebuild_progress", text="Progress %")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.refresh_table()
    def on_tree_select(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")

        self.selected_set_id = values[0]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.set_number_entry.delete(0, tk.END)
        self.set_number_entry.insert(0, values[2])

        self.status_combo.set(values[3])

        self.box_entry.delete(0, tk.END)
        self.box_entry.insert(0, values[4])

        self.missing_pieces_entry.delete(0, tk.END)
        self.missing_pieces_entry.insert(0, values[5])

        self.progress_entry.delete(0, tk.END)
        self.progress_entry.insert(0, values[6])
        full_data = self.database.get_lego_set_by_id(
        self.selected_set_id
        )

        if full_data:
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert("1.0", full_data[7])
    def update_selected_set(self):
        if not hasattr(self, "selected_set_id"):
            messagebox.showerror(
                "No Selection",
                "Please select a LEGO set first."
            )
            return

        name = self.name_entry.get().strip()
        set_number = self.set_number_entry.get().strip()
        status = self.status_combo.get().strip()
        box_number = self.box_entry.get().strip()
        missing_pieces = self.missing_pieces_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        try:
            rebuild_progress = int(self.progress_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Rebuild progress must be a number between 0 and 100."
            )
            return

        if not name:
            messagebox.showerror(
                "Missing Information",
                "Set name is required."
            )
            return

        if rebuild_progress < 0 or rebuild_progress > 100:
            messagebox.showerror(
                "Invalid Input",
                "Rebuild progress must be between 0 and 100."
            )
            return

        box_id = self.database.get_or_create_box(box_number)

        self.database.update_lego_set(
            self.selected_set_id,
            name,
            set_number,
            status,
            box_id,
            missing_pieces,
            rebuild_progress,
            notes
        )

        messagebox.showinfo(
            "Success",
            "LEGO set updated successfully."
        )

        self.clear_form()
        self.refresh_table() 
    def delete_selected_set(self):
        if not hasattr(self, "selected_set_id"):
            messagebox.showerror(
                "No Selection",
                "Please select a LEGO set first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this LEGO set?"
        )

        if not confirm:
            return

        self.database.delete_lego_set(self.selected_set_id)

        messagebox.showinfo(
            "Deleted",
            "LEGO set deleted successfully."
        )

        del self.selected_set_id
        self.clear_form()
        self.refresh_table()       
    def add_lego_set(self):
        name = self.name_entry.get().strip()
        set_number = self.set_number_entry.get().strip()
        status = self.status_combo.get().strip()
        box_number = self.box_entry.get().strip()
        missing_pieces = self.missing_pieces_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        try:
            rebuild_progress = int(self.progress_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Rebuild progress must be a number between 0 and 100."
            )
            return

        if not name:
            messagebox.showerror(
                "Missing Information",
                "Set name is required."
            )
            return

        if not box_number:
            messagebox.showerror(
                "Missing Information",
                "Box number is required."
            )
            return

        if rebuild_progress < 0 or rebuild_progress > 100:
            messagebox.showerror(
                "Invalid Input",
                "Rebuild progress must be between 0 and 100."
            )
            return

        box_id = self.database.get_or_create_box(box_number)

        self.database.add_lego_set(
            name,
            set_number,
            status,
            box_id,
            missing_pieces,
            rebuild_progress,
            notes
        )

        messagebox.showinfo(
            "Success",
            "LEGO set added successfully."
        )

        self.clear_form()
        self.refresh_table()
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.set_number_entry.delete(0, tk.END)
        self.status_combo.set("")
        self.box_entry.delete(0, tk.END)
        self.missing_pieces_entry.delete(0, tk.END)
        self.progress_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.database.get_all_lego_sets()
        selected_filter = self.filter_combo.get().strip()

        for row in rows:
            status = str(row[3]).strip()

            if selected_filter != "All" and status != selected_filter:
                continue

            self.tree.insert("", tk.END, values=row[:7])
root = tk.Tk()
app = LegoPlannerApp(root)
root.mainloop()