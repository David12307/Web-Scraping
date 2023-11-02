import searchCars

import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from CTkListbox import *

car_brands = [
    "Mercedes Benz",
    "BMW",
    "Volkswagen"
]

car_models = {
    "Mercedes Benz": ["A Classe", "C Classe", "CLA Classe", "GLE Coupe", "M Classe", "CLS Classe", "E Classe", "S Classe", "G Classe", "GLA Classe", "GLB Classe", "GLC Classe", "GLE Classe", "GLS Classe", "B Classe", "Sprinter"],
    "BMW": ["Seria 1", "Seria 2", "Seria 4", "Seria 5", "Seria 6", "Seria 7", "i7", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "XM", "iX", "iX1"],
    "Volkswagen": ["Arteon", "Caddy", "Golf", "iD3", "iD4", "iD5", "Jetta", "Passat", "Polo", "Sharan", "Tiguan", "Touareg", "Touran", "Transporter"]
}

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def showModels():
            if brands_listbox.get():
                models_listbox.delete("all")
                for car in car_models[brands_listbox.get()]:
                    models_listbox.insert("END", car)
            else:
                messagebox.showerror("Error", "You need to select a brand.")

        def searchForCar(brand, cModel, c):
            if (brands_listbox.get() and models_listbox.get() or c == "s"):
                cars_list, avg_price, sortedCars = searchCars.getCars(brand, cModel)

                top = CTkToplevel(main_frame)
                top.geometry("1350x250")
                top.title("Results")

                found_cars = CTkLabel(top, text=f"Au fost gasite {len(cars_list)} masini.", font=('Mistral 18 bold', 30))
                found_cars.grid(row=0, column=1, pady=10, padx=10)
                avg_price_label = CTkLabel(top, text=f"Pretul mediu este {avg_price} EUR.")
                avg_price_label.grid(row=0, column=2, pady=10, padx=10)

                underCar_price = CTkLabel(top, text=f"Pretul sub medie: {sortedCars[0]['name']} din anul {str(sortedCars[0]['year'])} cu {sortedCars[0]['kilometers']} km la pretul {str(sortedCars[0]['price'])} si motorizarea: {sortedCars[0]['fuelType']}")
                underCar_price.grid(row=1, column=1, pady=10, padx=10)

                avgCar_price = CTkLabel(top, text=f"Pretul mediu: {sortedCars[1]['name']} din anul {str(sortedCars[1]['year'])} cu {sortedCars[1]['kilometers']} km la pretul {str(sortedCars[1]['price'])} si motorizarea: {sortedCars[1]['fuelType']}")
                avgCar_price.grid(row=2, column=1, pady=10, padx=10)

                overCar_price = CTkLabel(top, text=f"Pretul peste medie: {sortedCars[2]['name']} din anul {str(sortedCars[2]['year'])} cu {sortedCars[2]['kilometers']} km la pretul {str(sortedCars[2]['price'])} si motorizarea: {sortedCars[2]['fuelType']}")
                overCar_price.grid(row=3, column=1, pady=10, padx=10)

                cheapCar = CTkLabel(top, text=f"{cars_list[0]['name']} din anul {cars_list[0]['year']} cu {cars_list[0]['kilometers']} km la pretul {cars_list[0]['price']} EUR si motorizarea: {cars_list[0]['fuelType']} este cel mai ieftin model.")
                cheapCar.grid(row=1, column=2, pady=10, padx=10)

                expCar = CTkLabel(top, text=f"{cars_list[-1]['name']} din anul {cars_list[-1]['year']} cu {cars_list[-1]['kilometers']} km la pretul {cars_list[-1]['price']} EUR si motorizarea: {cars_list[-1]['fuelType']} este cel mai scump model.")
                expCar.grid(row=2, column=2, pady=10, padx=10)
            else:
                messagebox.showerror("Error", message="You need to select a car.")

        def searchSpecificCar():
            searchFrame = CTkToplevel(main_frame)
            searchFrame.geometry("250x250")
            searchFrame.title("Search")

            brand_entry = CTkEntry(searchFrame, placeholder_text="Brand name")
            brand_entry.place(x=54, y=20)
            
            model_entry = CTkEntry(searchFrame, placeholder_text="Model name")
            model_entry.place(x=54, y=70)

            sSpecificButton = CTkButton(searchFrame, command=lambda: searchForCar(brand_entry.get(), model_entry.get(), "s"), text="Cauta",  fg_color="#59bd52", hover_color="#4ba245")
            sSpecificButton.place(x=54, y=120)


        main_frame = CTkFrame(self, fg_color=self.cget("bg"))
        main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Title
        title = CTkLabel(main_frame, text="Cauta o masina pe autovit.ro")
        title.grid(row=0, column=0, pady=(0, 20))

        # Listbox with all the car brands
        brands_listbox = CTkListbox(main_frame, 100, 200)
        brands_listbox.grid(row=1, column=0, pady=10, padx=10)
        for car in car_brands:
            brands_listbox.insert("END", car)
        show_models = CTkButton(main_frame, text="Arata modelele", command=showModels, fg_color="#d11a2a", hover_color="#b21616")
        show_models.grid(row=2, column=0, pady=10, padx=10)

        # Listbox with all the models of the selected car brand
        models_listbox = CTkListbox(main_frame, 100, 200)
        models_listbox.grid(row=1, column=2, pady=10, padx=10)

        specific_model = CTkButton(main_frame, text="Cauta un model de masina specific", command=searchSpecificCar)
        specific_model.place(x=260, y=0) #

        search_button = CTkButton(main_frame, text="Cauta", fg_color="#59bd52", hover_color="#4ba245", command=lambda: searchForCar(brands_listbox.get(), models_listbox.get(), "l"))
        search_button.place(x=295, y=300)

app = App()
app.title("Cauta masini pe autovit.ro")
app.mainloop()