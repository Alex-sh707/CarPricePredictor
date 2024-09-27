import ml

print("This is a program for helping you to predict you car's price")

# getting the data from user

brand = input("Please enter the brand : ").lower()

while not brand in set(ml.df["Brand"]) :
    print("The brand is not valid, enter a brand among these brands : ")
    for i in set(ml.df["Brand"]) :
        print(i , end="_")
    brand = input("Please enter the brand : ").lower()
    
model = input("Please enter the model : ")
while not model in set(ml.df["Model"]) :
    print("The model  is not valid, enter a model among these models  : ")
    for i in set(ml.df["Model"]) :
        print(i , end="_")
    model  = input("Please enter the model  : ")

year = int(input("Please enter the year : "))

mileage = int(input("Please enter the mileage : "))

if mileage == 0 :
    usage  = "New"
else :
    usage  = "Used"

ml.prediction_price(brand , model , mileage , year , usage)