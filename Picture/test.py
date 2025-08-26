import pandas as pd

# Data from the image
data = {
    "名次": [1, 2, 2, 3, 4, 4, 1, 1, 2, 2, 2, 3, 4, 4, 5, 6, 7, 7, 7, 8, 9],
    "廠牌": ["Toyota", "Honda", "Honda", "Mitsubishi", "Toyota", "Toyota",
            "Suzuki", "Suzuki", "Kia", "Kia", "Kia", "Suzuki", "Skoda", "Skoda", 
            "VW", "Mazda", "Fiat", "Fiat", "Fiat", "Toyota", "Alfa Romeo"],
    "車名": ["Vios", "Fit", "Fit", "Colt Plus", "Yaris", "Yaris", "Swift", "Swift",
            "Picanto", "Picanto", "Picanto", "Ignis", "Fabia", "Fabia", "Polo", "2", 
            "500", "500", "500", "Yaris", "Giulietta"],
    "車型": ["-", "1.5", "e:HEV", "-", "1.5", "Crossover", "1.2", "Sport", "一般", 
            "GT-Line", "X-Line", "-", "1.0", "1.5", "-", "-", "汽油", "Abarth", 
            "電動", "GR", "-"],
    "掛牌數": [404, 81, 262, 271, "-", "-", 202, 43, 9, 74, 4, 68, 50, 10, 37, 13, 
              2, 6, 0, 8, 1]
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Saving to CSV
csv_path = "C:/Users/MH/NTCUcollege/programming_language/python/spider/Picture/car_registration_data.csv"
df.to_csv(csv_path, index=False)
csv_path

