import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

class Student:
    def __init__(self, code, name, marks):
        self.code = code
        self.name = name
        self.coursework = marks[:3]
        self.exam = marks[3]
        self.total = sum(self.coursework) + self.exam
        self.percentage = (self.total / 160) * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Number: {self.code}\n"
                f"Total Coursework: {sum(self.coursework)}\n"
                f"Exam Mark: {self.exam}\n"
                f"Overall Percentage: {self.percentage:.2f}%\n"
                f"Grade: {self.grade}\n")

class StudentManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Management System")
        self.master.geometry("600x500")
        self.master.configure(bg="#E6E6FA")  

        self.students = []
        self.load_data()

        # Create a frame for buttons
        button_frame = tk.Frame(master, bg="#E6E6FA")
        button_frame.pack(pady=10)

        button_style = {"bg": "#6A5ACD", "fg": "white", "font": ("Arial", 10), "width": 20, "height": 2}
        
        tk.Button(button_frame, text="All Student Records", command=self.view_all_records, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Student with Highest Score", command=self.show_highest_score, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Student with Lowest Score", command=self.show_lowest_score, **button_style).pack(side=tk.LEFT, padx=5)

        # Search bar
        search_label = tk.Label(master, text="Search by Code or Name:", bg="#E6E6FA", font=("Arial", 10))
        search_label.pack(pady=(10, 0))

        self.search_entry = tk.Entry(master, width=30)
        self.search_entry.pack(pady=(0, 10))

        search_button = tk.Button(master, text="Search", command=self.view_individual_record, bg="#6A5ACD", fg="white", font=("Arial", 10))
        search_button.pack(pady=(0, 10))

        # Display area for results
        self.result_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20, bg="#FFFFFF", fg="#000000")
        self.result_area.pack(padx=10, pady=10)

    def load_data(self):
        try:
            with open('resources/studentMarks.txt', 'r') as file:
                num_students = int(file.readline().strip())
                for _ in range(num_students):
                    line = file.readline().strip().split(',')
                    code = int(line[0])
                    name = line[1].strip()
                    marks = [int(mark) for mark in line[2:]]
                    self.students.append(Student(code, name, marks))
        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt file not found in resources folder.")

    def view_all_records(self):
        result = "All Student Records:\n\n"
        total_percentage = 0
        for student in self.students:
            result += str(student) + "\n"
            total_percentage += student.percentage
        
        avg_percentage = total_percentage / len(self.students) if self.students else 0
        result += f"\nNumber of students: {len(self.students)}\n"
        result += f"Average percentage: {avg_percentage:.2f}%"
        
        self.display_result(result)

    def view_individual_record(self):
        choice = self.search_entry.get().strip()
        
        if choice:
            for student in self.students:
                if str(student.code) == choice or student.name.lower() == choice.lower():
                    self.display_result(str(student))
                    return
            messagebox.showerror("Error", "Student not found.")
            self.result_area.delete(1.0, tk.END) 

    def show_highest_score(self):
        if self.students:
            highest_student = max(self.students, key=lambda s: s.total)
            self.display_result(f"Student with Highest Score:\n\n{highest_student}")
        else:
            messagebox.showinfo("Info", "No students in the system.")
            self.result_area.delete(1.0, tk.END)  

    def show_lowest_score(self):
        if self.students:
            lowest_student = min(self.students, key=lambda s: s.total)
            self.display_result(f"Student with Lowest Score:\n\n{lowest_student}")
        else:
            messagebox.showinfo("Info", "No students in the system.")
            self.result_area.delete(1.0, tk.END)  
    def display_result(self, result):
        self.result_area.delete(1.0, tk.END)  
        self.result_area.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()