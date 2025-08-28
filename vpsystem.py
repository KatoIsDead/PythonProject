import tkinter as tk
from tkinter import messagebox

keyCourses = []
studentGradesValues = []
arrCourses = {}
firstNameInp =  ""
lastNameInp = ""
ageInp = 0
gradeInp = 0
sectionInp = ""
studentInfo = {}
allStudent = []

#root refers to window
def home(previousWindow):
    previousWindow.destroy()
    root = tk.Tk()
    root.title("VP System")
    root.geometry("280x500")
    label = tk.Label(root, text="Welcome user!")
    label.pack()
    # c = tk.Button(root,text="Course", command = storingCourses )
    # c.pack()
    s = tk.Button(root, text="Start", command = lambda: students(root))
    s.pack()
    print("Ps: C = Courses, it includes storing values to the grades. H = Home. S = Students, storing the name and infos of the student.")
    root.mainloop()

def students(previousWindow):
    previousWindow.destroy()
    root = tk.Tk()
    root.title("Students")
    root.geometry("720x600")
    label = tk.Label(root, text="Add the students here!")
    label.pack()
    firstNameTxt = tk.Label(root, text="First name: ")
    firstNameInp = tk.Entry(root, width=20)
    lastNameTxt = tk.Label(root, text="Last name: ")
    lastNameInp = tk.Entry(root, width=20)
    ageTxt = tk.Label(root, text="Age: ")
    ageInp = tk.Entry(root, width=20)
    gradeTxt = tk.Label(root, text="Grade: ")
    gradeInp = tk.Entry(root, width=20)
    sectionTxt = tk.Label(root, text="Section: ")
    sectionInp = tk.Entry(root,width=20)
    studentsListBox = tk.Listbox(root, width=100)
    studentsListBox.pack()

    def clearInputs():
        firstNameInp.delete(0, tk.END)
        lastNameInp.delete(0, tk.END)
        ageInp.delete(0, tk.END)
        gradeInp.delete(0, tk.END)
        sectionInp.delete(0, tk.END)

    def submitInputs():
        first = firstNameInp.get().strip()
        last = lastNameInp.get().strip()
        age = ageInp.get().strip()
        grade = gradeInp.get().strip()
        section = sectionInp.get().strip()


        if not (first and last and age and grade and section):
            messagebox.showerror("Error!", "Please fill the values correctly!")
            return
        try:
            ageError = int(age)
        except ValueError:
            messagebox.showerror("Error!", "Age must be an integer.")
            return
        try:
            gradeError = int(grade)
        except ValueError:
            messagebox.showerror("Error!", "Grade must be a float.")
            return
        studentInfo = {
            "firstName":first,
            "lastName": last,
            "age": ageError,
            "grade": gradeError,
            "section": section,
        }
        allStudent.append(studentInfo)
        displayList = f" First Name: {first} Last Name:{last} Age: {age} Grade: {grade} Section: {section}"
        studentsListBox.insert(tk.END, displayList)
        clearInputs()
        messagebox.showinfo("Success", "All have been submitted successfully!")
        print(allStudent)

    def deleteStudentInList():
        selectedIndex = studentsListBox.curselection()
        if not selectedIndex:
            messagebox.showwarning("Woops!", "Please select a student in the list.")
            return

        index = selectedIndex[0]

        confirm = messagebox.askyesno("Please confirm!", "Are you sure you want to delete this student?")
        if confirm:
            del allStudent[index]
            studentsListBox.delete(index)
            messagebox.showinfo("Success!", "Student has been deleted!")

    #Grading System
    def selectGrading():
        selectedStudent = studentsListBox.curselection()
        if not selectedStudent:
            messagebox.showwarning("Woops!", "You need to select a student in the list first.")
            return

        selectedIndex = selectedStudent[0]
        student = allStudent[selectedIndex]
        gradingWindow = tk.Toplevel(root) #this acts like tk.Tk() but with a parameter inside
        gradingWindow.geometry("720x600")
        gradingWindow.title("Grading")

        tk.Label(gradingWindow, text=f"Student: {student['firstName']} {student['lastName']}").pack()
        tk.Label(gradingWindow, text=f"Grade: {student['grade']}").pack()

        scoresDict = {
            "minor": [],
            "major": []
        }
        gradesDict = {
            "prelim": None,
            "midterm": None,
            "final": None,
            "midtermStanding": None,
            "total": None
        }

        scoresListBox = tk.Listbox(gradingWindow, width=100)
        scoresListBox.pack()
        minorInp = tk.Entry(gradingWindow, width=20)
        majorInp = tk.Entry(gradingWindow, width=20)

        result = tk.Label(gradingWindow, text="Results!")
        result.pack()

        def addScores(entry, scoreType):
            score = entry.get().strip()
            try:
                score = float(score)
                scoresDict[scoreType].append(score)
                scoresListBox.insert(tk.END, f"{scoreType.capitalize()} Score: {score}")
                entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("ERROR!", "Please enter a number.")

        def calculateAvg(scoresLists):
            return sum(scoresLists) / len(scoresLists)

        def prelim():
            newMinor = minorInp.get().strip()
            newMajor = majorInp.get().strip()
            if newMinor:
                try:
                    score = float(newMinor)
                    scoresDict["minor"].append(score)
                    scoresListBox.insert(tk.END, f"Minor Score: {score}")
                    minorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Minor score")
            if newMajor:
                try:
                    score = float(newMajor)
                    scoresDict["major"].append(score)
                    scoresListBox.insert(tk.END, f"Major Score: {score}")
                    majorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Major score")

            if not scoresDict["minor"] or not scoresDict["major"]:
                messagebox.showerror("MISSING SCORES!", "Add minor and major scores!")
                return

            minorAvg = calculateAvg(scoresDict["minor"])
            majorAvg = calculateAvg(scoresDict["major"])
            grade = (minorAvg * 0.3) + (majorAvg * 0.4)
            gradesDict["prelim"] = grade

            scoresListBox.insert(tk.END, f"Prelim Grade: Minor Average: {minorAvg: .2f}, Major Average: {majorAvg: .2f}, Grade:{grade: .2f}")

            scoresDict["minor"].clear()
            scoresDict["major"].clear()


        def midterm():
            newMinor = minorInp.get().strip()
            newMajor = majorInp.get().strip()
            if newMinor:
                try:
                    score = float(newMinor)
                    scoresDict["minor"].append(score)
                    scoresListBox.insert(tk.END, f"Minor Score: {score}")
                    minorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Minor score")
            if newMajor:
                try:
                    score = float(newMajor)
                    scoresDict["major"].append(score)
                    scoresListBox.insert(tk.END, f"Major Score: {score}")
                    majorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Major score")
            if not scoresDict["minor"] or not scoresDict["major"]:
                messagebox.showerror("MISSING SCORES!", "Add minor and major scores!")
                return

            minorAvg = calculateAvg(scoresDict["minor"])
            majorAvg = calculateAvg(scoresDict["major"])
            grade = (minorAvg * 0.3) + (majorAvg * 0.4)
            gradesDict["midterm"] = grade

            scoresListBox.insert(tk.END, f"Midterm Grade: Minor Average: {minorAvg: .2f}, Major Average: {majorAvg: .2f}, Grade:{grade: .2f}")

            scoresDict["minor"].clear()
            scoresDict["major"].clear()

        def final():
            newMinor = minorInp.get().strip()
            newMajor = majorInp.get().strip()
            if newMinor:
                try:
                    score = float(newMinor)
                    scoresDict["minor"].append(score)
                    scoresListBox.insert(tk.END, f"Minor Score: {score}")
                    minorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Minor score")
            if newMajor:
                try:
                    score = float(newMajor)
                    scoresDict["major"].append(score)
                    scoresListBox.insert(tk.END, f"Major Score: {score}")
                    majorInp.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid Major score")
            if not scoresDict["minor"] or not scoresDict["major"]:
                messagebox.showerror("MISSING SCORES!", "Add minor and major scores!")
                return

            minorAvg = calculateAvg(scoresDict["minor"])
            majorAvg = calculateAvg(scoresDict["major"])
            grade = (minorAvg * 0.3) + (majorAvg * 0.4)
            gradesDict["final"] = grade

            scoresListBox.insert(tk.END, f"Final Grade: Minor Average: {minorAvg: .2f}, Major Average: {majorAvg: .2f}, Grade:{grade: .2f}")

            scoresDict["minor"].clear()
            scoresDict["major"].clear()

        def midtermStanding():
            try:
                prelimGrade = gradesDict["prelim"]
                midtermGrade = gradesDict["midterm"]
                if prelimGrade is None or midtermGrade is None:
                    messagebox.showerror("Missing Grades!", "Please compute for both of the Prelim and Midterm grades!")
                    return
                computeAvg = (prelimGrade * 0.3) + (midtermGrade * 0.3)
                gradesDict["midtermStanding"] = computeAvg
                scoresListBox.insert(tk.END, f"Midterm Standing: {computeAvg: .2f}")
            except ValueError:
                messagebox.showerror("Error!", "Please try again")



        def deleteGrade():
            selected = scoresListBox.curselection()
            if not selected:
                messagebox.showwarning("ERROR!", "You must select a grade first")
                return

            selectedIndex = scoresListBox.get(selected[0])
            scoresListBox.delete(selected[0])

            if "Minor Score:" in selectedIndex:
                try:
                    value = float(selectedIndex.split("Minor Score:")[1].strip())
                    if value in scoresDict["minor"]:
                        scoresDict["minor"].remove(value)
                except:
                    pass

            elif "Major Score:" in selectedIndex:
                try:
                    value = float(selectedIndex.split("Major Score:")[1].strip())
                    if value in scoresDict["major"]:
                        scoresDict["major"].remove(value)
                except:
                    pass
            elif "Prelim Grade" in selectedIndex:
                gradesDict["prelim"] = None
            elif "Midterm Grade" in selectedIndex:
                gradesDict["midterm"] = None
            elif "Final Grade" in selectedIndex:
                gradesDict["final"] = None
            elif "Midterm Standing" in selectedIndex:
                gradesDict["midtermStanding"] = None
            elif "Computed All Grades:" in selectedIndex:
                gradesDict["total"] = None

        def computeAllGrade():
            try:
                prelimGrade = gradesDict["prelim"]
                midtermGrade = gradesDict["midterm"]
                finalGrade = gradesDict["final"]

                if prelimGrade is None or midtermGrade is None or finalGrade is None:
                    messagebox.showerror("ERROR!", "The Prelim, Midterm, and Final Grades were not computed. Please compute them first before you proceed here.")

                computeAvg = (prelimGrade * 0.3) + (midtermGrade * 0.3) + (finalGrade * 0.4)
                gradesDict["total"] = computeAvg
                scoresListBox.insert(tk.END,f"Computed All Grades: Prelim Grade: {prelimGrade:.2f}, Midterm Grade: {midtermGrade:.2f}, Final Grade: {finalGrade:.2f}, Average Grade: {computeAvg:.2f}")

            except ValueError:
                messagebox.showerror("ERROR!", "Grades not found in dictionary.")

        tk.Label(gradingWindow, text=f"Minor:").pack()
        minorInp.pack()
        tk.Button(gradingWindow, text="Submit", command= lambda: addScores(minorInp, "minor")).pack()
        tk.Label(gradingWindow, text=f"Major:").pack()
        majorInp.pack()
        tk.Button(gradingWindow, text="Submit", command= lambda: addScores(majorInp, "major")).pack()

        tk.Button(gradingWindow, text="Prelim", command=prelim).pack()
        tk.Button(gradingWindow, text="Midterm", command=midterm).pack()
        tk.Button(gradingWindow, text="Midterm Standing", command=midtermStanding).pack()
        tk.Button(gradingWindow, text="Final", command=final).pack()
        tk.Button(gradingWindow, text="Compute All", command=computeAllGrade).pack()
        tk.Button(gradingWindow, text="Delete", command=deleteGrade).pack()

    firstNameTxt.pack()
    firstNameInp.pack()
    lastNameTxt.pack()
    lastNameInp.pack()
    ageTxt.pack()
    ageInp.pack()
    gradeTxt.pack()
    gradeInp.pack()
    sectionTxt.pack()
    sectionInp.pack()

    deleteButton = tk.Button(root, text="Delete", command=deleteStudentInList)
    back = tk.Button(root, text="Back", command= lambda: home(root))
    submit = tk.Button(root, text="Submit", command=submitInputs)
    back.pack()
    submit.pack()
    tk.Button(root, text="Grading", command=selectGrading).pack()
    deleteButton.pack()

    root.mainloop()

home(tk.Tk())