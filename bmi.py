import tkinter as tk

class Patient:
    def __init__(self, Weight=0.0, Height=0.0):
        self.weight = Weight
        self.height = Height

    def bmi(self):
        return self.weight / (self.height ** 2)

    def bmi_category(self):
        bmi_value = self.bmi()
        if bmi_value < 18.5:
            if bmi_value < 16.0:
                return "underweight: severe thinness"
            elif 16.0 <= bmi_value < 16.9:
                return "underweight: moderate thinness"
            else:
                return "underweight: mild thinness"
        elif bmi_value < 25:
            return "Normal Weight"
        elif bmi_value < 30:
            return "Overweight"
        else:
            if 30.0 <= bmi_value < 34.9:
                return "Obese: Class 1"
            elif 35 <= bmi_value < 39.9:
                return "Obese: Class 2"
            else:
                return "Obese: Class 3"
            
# Tkinter setup
root = tk.Tk()
#colors
bg_color = "#FFF3E0"
heightWeight_co = "#FFAB91"
result_co = "#d55550"

root.title("BMI Calculator")
root.geometry("400x400")
root.resizable(height =False, width=False)
root.config(bg= bg_color)

def calculate_bmi():
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        patient = Patient(weight, height)
        bmi_value = patient.bmi()
        bmi_category = patient.bmi_category()
        frame_result.config(text= f"BMI: {bmi_value: .2f}\n Category: {bmi_category}")

frame_height = tk.Frame(root, bg = heightWeight_co)
frame_height.place(x=0, y=20)

Label_height = tk.Label(frame_height, text= "Enter your Height(m)", bg= heightWeight_co, fg= "black", font= ("Garamond",14, "roman"))
Label_height.pack(side=tk.TOP, padx=10, pady=20)

entry_height= tk.Entry(frame_height)
entry_height.pack(side=tk.BOTTOM, padx=10, pady =20)

frame_weight= tk.Frame(root, bg= heightWeight_co)
frame_weight.place(x=210, y=20)

Label_weight = tk.Label(frame_weight, text= "Enter your Weight(kg)", bg= heightWeight_co, fg= "black", font= ("Garamond", 14, "roman"))
Label_weight.pack(side=tk.TOP,padx=10, pady=20)

entry_weight= tk.Entry(frame_weight)
entry_weight.pack(side=tk.BOTTOM, padx=10, pady=20)

button_calculate = tk.Button(root, text= "CALCULATE", command= calculate_bmi, width= 15, height= 2)
button_calculate.place(x= 140, y=200)

frame_result = tk.Label(root, text= "BMI", bg= result_co, fg= "black", width= 30, height= 3, font= ("Garamond", 12))
frame_result.place(x= 60,y=300)

root.mainloop()