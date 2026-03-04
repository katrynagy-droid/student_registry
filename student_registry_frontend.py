#frontend
import tkinter as tk              # Import the toolkit to create windows and buttons
from tkinter import messagebox    # Import the toolkit to show pop-up alert messages
import json                       # Import tools to save/load data in text format
import os                         # Import tools to check if the file exists on your PC

# --- THE DATA TEMPLATE ---
class Student:
    def __init__(self, sid, name, major, gpa):
        self.sid = sid            # Set the student's ID number
        self.name = name          # Set the student's full name
        self.major = major        # Set the student's field of study
        self.gpa = gpa            # Set the student's grade point average

# --- THE FRONT END & LOGIC ---
class StudentApp:
    def __init__(self, root):
        self.root = root                         # Connect the app to the main window
        self.root.title("Student Registry")      # Put a title at the top of the window
        self.root.geometry("450x600")            # Set the window size (Width x Height)
        
        # --- THE LILAC THEME COLORS ---
        self.lilac = "#C8A2C8"                   # Define the main Lilac color code
        self.light_hue = "#F9F4F9"               # Define a very light purple for the background
        
        self.root.configure(bg=self.light_hue)   # Paint the window background light purple
        self.students = []                       # Create a list to hold student records in memory
        self.load_data()                         # Run the 'load' function to get saved data

        # --- BUILDING THE INTERFACE ---
        # Create a header bar at the top
        self.header = tk.Label(root, text="STUDENT SYSTEM", bg=self.lilac, fg="white", 
                               font=("Helvetica", 16, "bold"), pady=15)
        self.header.pack(fill="x")               # Make the header stretch across the top

        # Create input boxes using a helper function (defined below)
        self.create_input_field("Student ID:", "entry_id")      # Box for ID
        self.create_input_field("Full Name:", "entry_name")     # Box for Name
        self.create_input_field("Major:", "entry_major")        # Box for Major
        self.create_input_field("GPA:", "entry_gpa")            # Box for GPA

        # Create a "container" (Frame) to hold our buttons side-by-side
        self.btn_frame = tk.Frame(root, bg=self.light_hue)
        self.btn_frame.pack(pady=20)             # Add some space around the buttons

        # Add the 'ADD' button - calls self.add_student when clicked
        tk.Button(self.btn_frame, text="ADD", command=self.add_student, bg=self.lilac, width=12).grid(row=0, column=0, padx=5)
        # Add the 'SEARCH' button - calls self.search_student when clicked
        tk.Button(self.btn_frame, text="SEARCH", command=self.search_student, bg="#B19CD9", width=12).grid(row=0, column=1, padx=5)
        # Add the 'DELETE' button - calls self.delete_student when clicked
        tk.Button(self.btn_frame, text="DELETE", command=self.delete_student, bg="#DDA0DD", width=12).grid(row=1, column=0, pady=10)
        # Add the 'SHOW ALL' button - calls self.show_all when clicked
        tk.Button(self.btn_frame, text="LIST ALL", command=self.show_all, bg="#E6E6FA", width=12).grid(row=1, column=1, pady=10)

        # Create a text display area at the bottom to show lists of students
        self.display = tk.Text(root, height=8, width=45, bg="white", font=("Arial", 10))
        self.display.pack(padx=20, pady=10)      # Add padding so it doesn't touch the edges

    def create_input_field(self, label_text, var_name):
        # Create a text label (e.g., "Student ID:")
        tk.Label(self.root, text=label_text, bg=self.light_hue, font=("Arial", 10)).pack(anchor="w", padx=50, pady=(10,0))
        # Create an empty box for the user to type in
        entry = tk.Entry(self.root, highlightbackground=self.lilac, highlightthickness=1)
        entry.pack(fill="x", padx=50)            # Stretch the box to look nice
        setattr(self, var_name, entry)           # Give the box a name so we can read it later

    # --- THE ENGINE (LOGIC) ---
    def add_student(self):
        # Read the text currently typed into the boxes
        sid, name, maj, gpa = self.entry_id.get(), self.entry_name.get(), self.entry_major.get(), self.entry_gpa.get()
        if sid and name:                         # Make sure ID and Name aren't empty
            self.students.append(Student(sid, name, maj, gpa)) # Add new student to our list
            self.save_data()                     # Save the updated list to the file
            messagebox.showinfo("Success", f"{name} added!") # Show a happy pop-up
            self.clear_entries()                 # Clear the boxes for the next entry
        else:
            messagebox.showwarning("Empty Fields", "Please fill in ID and Name.") # Warn if empty

    def search_student(self):
        target_id = self.entry_id.get()          # Get the ID the user is looking for
        for s in self.students:                  # Loop through every student we have
            if s.sid == target_id:               # If the ID matches...
                messagebox.showinfo("Result", f"Found: {s.name}\nMajor: {s.major}\nGPA: {s.gpa}")
                return                           # Stop searching once found
        messagebox.showerror("Not Found", "No student with that ID.") # Show error if loop finishes

    def delete_student(self):
        target_id = self.entry_id.get()          # Get the ID to delete
        # Create a new list excluding the student with that ID
        self.students = [s for s in self.students if s.sid != target_id]
        self.save_data()                         # Save the new, shorter list to the file
        messagebox.showinfo("Update", "Student record removed.")
        self.show_all()                          # Refresh the display list

    def show_all(self):
        self.display.delete('1.0', tk.END)       # Clear the bottom text box
        for s in self.students:                  # For every student in our list...
            self.display.insert(tk.END, f"[{s.sid}] {s.name} - {s.major}\n") # ...write their info

    def save_data(self):
        # Open 'database.json' and write all student info as text
        with open("database.json", "w") as f:
            json.dump([s.__dict__ for s in self.students], f, indent=4)

    def load_data(self):
        # If the file exists, read it and fill our list
        if os.path.exists("database.json"):
            with open("database.json", "r") as f:
                data = json.load(f)              # Convert text file back to data
                # Re-create student objects from the saved data
                self.students = [Student(d['sid'], d['name'], d['major'], d['gpa']) for d in data]

    def clear_entries(self):
        # Delete everything inside the input boxes from start (0) to end
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_major.delete(0, tk.END)
        self.entry_gpa.delete(0, tk.END)

# --- START THE APP ---
if __name__ == "__main__":
    window = tk.Tk()                             # Create the actual window object
    app = StudentApp(window)                     # Load our code into that window
    window.mainloop()                            # Keep the window open until we click 'X'