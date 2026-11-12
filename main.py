import tkinter as tk
from tkinter import messagebox
import csv
import os

current_record = None

def calculate():
    global current_record

    try:
        name = name_entry.get().strip()
        roll = roll_entry.get().strip()

        if name == "" or roll == "":
            messagebox.showerror("Error", "Enter name and roll number")
            return

        marks = [
            float(dsa_entry.get()),
            float(ade_entry.get()),
            float(economics_entry.get()),
            float(co_entry.get()),
            float(dm_entry.get()),
            float(itw_entry.get())
        ]

        if any(m < 0 or m > 100 for m in marks):
            messagebox.showerror("Error", "Marks must be between 0 and 100")
            return

        total = sum(marks)
        percentage = total / 6
        average = total / 6

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"

        result = "PASS" if all(m >= 40 for m in marks) else "FAIL"
        subjects = ["Data Structures and Algorithms", "Analog and Digital Electronics", "Economics for Engineers", "Computer Organization", "Discrete Mathematics", "IT WORKSHOP"]

        highest = subjects[marks.index(max(marks))]
        lowest = subjects[marks.index(min(marks))]

        if percentage >= 80:
            feedback = "Excellent performance!"
        elif percentage >= 60:
            feedback = "Good performance. Keep improving!"
        else:
            feedback = "More practice is needed."
        current_record = [
            name, roll, *marks, total,
            round(percentage, 2), round(average, 2),
            grade, result
        ]

        output.config(
            text=f"Name: {name}\nRoll Number: {roll}\n"
                 f"Total: {total}/600\nPercentage: {percentage:.2f}%\n"
               f"Average: {average:.2f}\nGrade: {grade}\nResult: {result}\n"
f"Highest Subject: {highest}\n"
f"Lowest Subject: {lowest}\n"
f"Feedback: {feedback}"
        )
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")


def save_record():
    if current_record is None:
        messagebox.showerror("Error", "Calculate the result first")
        return

    file_exists = os.path.isfile("student_records.csv")

    with open("student_records.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name", "Roll Number", "Data Structures and Algorithms", "Analog and Digital Electronics",
                "Economics for Engineers", "Computer Organization", "Discrete Mathematics", "IT WORKSHOP", "Total",
                "Percentage", "Average", "Grade", "Result"
            ])

        writer.writerow(current_record)

    messagebox.showinfo("Saved", "Student record saved successfully!")


def search_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()

    if roll == "" and name == "":
        messagebox.showerror("Error", "Enter student name or roll number")
        return

    if not os.path.isfile("student_records.csv"):
        messagebox.showerror("Error", "No student records found")
        return

    with open("student_records.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if (record["Roll Number"].strip() == roll and roll != "") or \
               (record["Name"].strip().casefold() == name.casefold() and name != ""):
                messagebox.showinfo(
                    "Student Found",
                    f"Name: {record['Name']}\n"
                    f"Roll Number: {record['Roll Number']}\n"
                    f"Percentage: {record['Percentage']}%\n"
                    f"Grade: {record['Grade']}\n"
                    f"Result: {record['Result']}"
                )
                return

    messagebox.showinfo("Not Found", "No matching student found")

window = tk.Tk()
window.title("Student Marks Analyzer")
window.geometry("450x650")
window.configure(bg="#EAF2F8")
tk.Label(
    window,
    text="STUDENT MARKS ANALYZER",
    font=("Arial", 18, "bold"),
    bg="#EAF2F8",
    fg="#154360"
).pack(pady=15)

tk.Label(window, text="Student Name", bg="#EAF2F8", fg="#154360",
         font=("Arial", 10, "bold")).pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Roll Number", bg="#EAF2F8",
         fg="#154360", font=("Arial", 10, "bold")).pack()
roll_entry = tk.Entry(window)
roll_entry.pack()

entries = []


for subject in [
    "Data Structures and Algorithms",
    "Analog and Digital Electronics",
    "Economics for Engineers",
    "Computer Organization",
    "Discrete Mathematics",
    "IT WORKSHOP"
]:
    tk.Label(
        window,
        text=subject + " Marks (0-100)",
        bg="#EAF2F8",
        fg="#154360",
        font=("Arial", 10, "bold")
    ).pack()

    entry = tk.Entry(window)
    entry.pack()
    entries.append(entry)

dsa_entry, ade_entry, economics_entry, co_entry, dm_entry, itw_entry = entries

tk.Button(
    window, text="Calculate Result",
    command=calculate, bg="#2874A6", fg="white",
    font=("Arial", 10, "bold"), width=20
).pack(pady=10)

tk.Button(
    window, text="Save Record",
    command=save_record, bg="#239B56", fg="white",
    font=("Arial", 10, "bold"), width=20
).pack(pady=5)

tk.Button(
    window, text="Search Student",
    command=search_student, bg="#D4AC0D", fg="white",
    font=("Arial", 10, "bold"), width=20
).pack(pady=5)
output = tk.Label(window, text="", font=("Arial", 11), justify="left")
output.pack(pady=10)

window.mainloop()