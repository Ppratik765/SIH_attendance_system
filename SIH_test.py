import tkinter as tk
from tkinter import ttk
import os

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance")
        self.root.geometry("1280x720")  # Fixed size

        # Roll numbers
        self.roll_numbers = [f"24AI{str(i).zfill(3)}" for i in range(1, 59)]
        self.total_students = len(self.roll_numbers)

        # Track states
        self.button_states = {roll: False for roll in self.roll_numbers}  # False=absent, True=present
        self.roll_buttons = {}

        # --- Top Frame for counts ---
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=20)

        self.total_label = tk.Label(self.top_frame, text=f"Total Students: {self.total_students}",
                                    font=("Arial", 22, "bold"), fg="black")
        self.total_label.grid(row=0, column=0, padx=40)

        self.present_label = tk.Label(self.top_frame, text=f"Present: 0",
                                      font=("Arial", 22, "bold"), fg="green")
        self.present_label.grid(row=0, column=1, padx=40)

        self.absent_label = tk.Label(self.top_frame, text=f"Absent: {self.total_students}",
                                     font=("Arial", 22, "bold"), fg="red")
        self.absent_label.grid(row=0, column=2, padx=40)

        # --- Scrollable frame for roll numbers ---
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        # Create roll number buttons
        self.create_buttons_fixed()

        # Start auto-refresh loop
        self.refresh_attendance()

    def create_buttons_fixed(self):
        """Create roll number buttons in fixed rows/columns for 1280px width."""
        buttons_per_row = 8  # Fits nicely in 1280px width
        for idx, roll in enumerate(self.roll_numbers):
            btn = tk.Button(self.scroll_frame, text=roll, width=12, height=2,
                            bg="red", fg="white", font=("Arial", 12, "bold"))
            row = idx // buttons_per_row
            col = idx % buttons_per_row
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.roll_buttons[roll] = btn

    def refresh_attendance(self):
        """Read Present.txt, update colors, counts, and Absent.txt."""
        present_rolls = set()

        if os.path.exists("Present.txt"):
            with open("Present.txt", "r") as f:
                present_rolls = set(line.strip() for line in f if line.strip())

        # Update states
        for roll in self.roll_numbers:
            if roll in present_rolls:
                self.button_states[roll] = True
                self.roll_buttons[roll].config(bg="green")
            else:
                self.button_states[roll] = False
                self.roll_buttons[roll].config(bg="red")

        # Update counts
        present_count = sum(self.button_states.values())
        absent_count = self.total_students - present_count
        self.present_label.config(text=f"Present: {present_count}")
        self.absent_label.config(text=f"Absent: {absent_count}")

        # Write Absent.txt
        with open("Absent.txt", "w") as f:
            for roll in self.roll_numbers:
                if not self.button_states[roll]:
                    f.write(roll + "\n")

        # Schedule next refresh (every 0.1 sec)
        self.root.after(100, self.refresh_attendance)


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
