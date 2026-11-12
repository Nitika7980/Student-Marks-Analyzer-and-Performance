import streamlit as st
import pandas as pd
import os
import csv
st.set_page_config(
    page_title="Student Marks and Performance Analyzer",
    page_icon="📊",
    layout="centered"
)
password = st.text_input("Enter password:", type="password")
if password == "12345":
    st.title("🎓 Student Marks and Performance Analyzer")
    
    st.write("Calculate, save and search student academic records.") 
    
    st.subheader("Welcome!")
    st.write("Use the options below to manage student performance.")
    
    option = st.selectbox(
        "Choose an option",
        ["Search Existing Student", "Calculate New Result"]
    )
    
    if option == "Search Existing Student":
    
        st.subheader("Search Student")
    
        search_value = st.text_input("Enter Student Name or Roll Number")
    
        if st.button("Search Student"):
    
            import csv
    
            found = False
    
            if os.path.isfile("student_records.csv"):
                with open("student_records.csv", "r", newline="") as file:
                    reader = csv.DictReader(file)
    
                    for record in reader:
                        if (
                            record["Roll Number"].strip() == search_value.strip()
                            or record["Name"].strip().casefold() == search_value.strip().casefold()
                        ):
                            st.success("Student Found!")
                            st.write("Name:", record["Name"])
                            st.write("Roll Number:", record["Roll Number"])
                            st.write("Percentage:", record["Percentage"], "%")
                            st.write("Grade:", record["Grade"])
                            st.write("Result:", record["Result"])
                            found = True
                            break
    
            if not found:
                st.warning("No matching student found.")
                
        
    
    elif option == "Calculate New Result":
    
        st.subheader("Calculate Student Result")
    
        name = st.text_input("Student Name")
        roll = st.text_input("Roll Number")
    
        st.write("Enter marks (out of 100)")
    
        dsa = st.number_input("Data Structures and Algorithms", 0, 100, 0)
        ade = st.number_input("Analog and Digital Electronics", 0, 100, 0)
        economics = st.number_input("Economics for Engineers", 0, 100, 0)
        co = st.number_input("Computer Organization", 0, 100, 0)
        dm = st.number_input("Discrete Mathematics", 0, 100, 0)
        itw = st.number_input("IT WORKSHOP", 0, 100, 0)
    
        if st.button("Calculate Result"):
    
            if name.strip() == "" or roll.strip() == "":
                st.error("Enter student name and roll number")
    
            else:
                marks = [dsa, ade, economics, co, dm, itw]
    
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
    
                st.session_state["new_record"] = {
                    "Name": name,
                    "Roll Number": roll,
                    "Data Structures and Algorithms": dsa,
                    "Analog and Digital Electronics": ade,
                    "Economics for Engineers": economics,
                    "Computer Organization": co,
                    "Discrete Mathematics": dm,
                    "IT WORKSHOP": itw,
                    "Total": total,
                    "Percentage": round(percentage, 2),
                    "Average": round(average, 2),
                    "Grade": grade,
                    "Result": result
                }
                st.session_state["record_saved"] = False
    
        record = st.session_state.get("new_record")
    
        if record:
            st.success("Result Calculated!")
            st.write("Name:", record["Name"])
            st.write("Roll Number:", record["Roll Number"])
            st.write("Total:", record["Total"], "/ 600")
            st.write("Percentage:", record["Percentage"], "%")
            st.write("Average:", record["Average"])
            st.write("Grade:", record["Grade"])
            st.write("Result:", record["Result"])
    
            if not st.session_state.get("record_saved", False):
                if st.button("Save Record"):
                    file_exists = os.path.isfile("student_records.csv")
    
                    with open("student_records.csv", "a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=list(record.keys()))
    
                        if not file_exists or os.path.getsize("student_records.csv") == 0:
                            writer.writeheader()
    
                        writer.writerow(record)
    
                    st.session_state["record_saved"] = True
                    st.success("Student record saved successfully!")
            else:
                st.success("Student record already saved!")
