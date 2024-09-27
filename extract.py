import requests
import numpy as np
import pandas as pd 
import csv
from bs4 import BeautifulSoup


file = open("Mycsv.csv" , "w")
writer = csv.writer(file)


def mile_turner(str_mile) :
    if type(str_mile) == str :
        if "," in str_mile :
            str_mile = str_mile.replace("," , "")
        if "k" in str_mile :
            return int(str_mile.split("k")[0]) * 100
        else :
            return int(str_mile.split(" ")[0])
    else :
        return str_mile

url = "https://www.truecar.com/used-cars-for-sale/"

r = requests.get(url)
soup = BeautifulSoup(r.text ,"html.parser")

data_brand = []
data_price = []
data_year = []
data_usage = []
data_mileage = []
data_model = []


cars_brand = soup.find("select" , attrs={"data-test":"selectMake"})
cars_brand = cars_brand.find_all("option")

list_brands = [i.text for i in cars_brand]
list_brands.remove("All Makes")
list_brands = list(map(lambda x : x.lower() , list_brands))

for h in range(2) : # 0 is used and 1 is new
    for brand in list_brands :

        if " " in brand : # some brands have two symlols like royes rose
            brand = brand.replace(" " , "-")
            
        if h == 0 :
            url_check = "https://www.truecar.com/used-cars-for-sale/listings/" + brand + "/"
        else :
            url_check = "https://www.truecar.com/new-cars-for-sale/listings/" + brand + "/"
            
        r3 = requests.get(url_check)
        soup = BeautifulSoup(r3.text ,"html.parser")
        try :
            product_num = soup.find("span" ,attrs={"data-test":"marketplaceSrpListingsTotalCount"}).text
            product_num = int(product_num.replace("," , ""))
        except :
            product_num = 0 
            
        if product_num > 350 : # checking that brand has at least 350 products

            for page in range(1,11) :
                if h == 0 :
                    if page == 1 : # reading info of 10 pages
                        url2  = "https://www.truecar.com/used-cars-for-sale/listings/" + brand + "/"
                    else :
                        url2 = "https://www.truecar.com/used-cars-for-sale/listings/" + brand + "/" + "?page=" + str(page)
                    print(url2)
                else :
                    if page == 1 : # reading info of 10 pages
                        url2  = "https://www.truecar.com/new-cars-for-sale/listings/" + brand + "/"
                    else :
                        url2 = "https://www.truecar.com/new-cars-for-sale/listings/" + brand + "/" + "?page=" + str(page)
                    print(url2)
                    
                r2 = requests.get(url2)
                soup = BeautifulSoup(r2.text ,"html.parser")


                cars = soup.find("ul" , attrs={"class":"row mb-3 mt-1"}) # selecting the page of cars (33 cars)
                cars = cars.find_all("li") # selecting each cars

                cars_model = []
                cars_price = []
                cars_mileage = []
                cars_info = []
                cars_brands = []

                for car in cars : # getting cars info
                    try :
                        if h == 0 :
                            cars_price.append(car.find("span" , attrs={"data-test":"vehicleCardPriceLabelAmount"}).text[1:]) 
                            cars_mileage.append(car.find("div" , attrs={"data-test":"vehicleMileage"}).text)  
                            
                        else :
                            cars_price.append(car.find("div" , attrs={"class":"flex items-center text-[16px]"}).text[1:]) 
                            cars_mileage.append(0)  
                            
                        cars_model.append(car.find("div" , attrs={"data-test":"vehicleCardTrim"}).text) # getting model
                        cars_info.append(car.find("div" , attrs={"class":"w-full truncate font-bold"}).text)  
                        cars_brands.append(brand)
                        
                    except :
                        pass
                    
                # perparing the data
                cars_model = [i.split(" ")[0] for i in cars_model]
                
                cars_price = [int(i.replace("," , "")) for i in cars_price] # turning str prices to int

                cars_mileage = [mile_turner(i) for i in cars_mileage] # cleaning the miles and turning to int

                cars_year = [int(i.split(" ")[1]) if i.split(" ")[1].isnumeric() else  np.nan for i in cars_info] # extracting the year

                cars_new_used = [i.split(" ")[0] for i in cars_info] # determining if its new or used

                
                # adding to our table
                data_brand.extend(cars_brands)
                data_model.extend(cars_model)
                data_mileage.extend(cars_mileage)
                data_year.extend(cars_year)
                data_usage.extend(cars_new_used)
                data_price.extend(cars_price)
    

data = [data_brand , data_model , data_mileage , data_year , data_usage , data_price]
writer.writerow(["Brand" , "Model" , "Mileage" , "Year" , "Usage" , "Price"])
for i in range(len(data_brand)) :
    writer.writerow([data_brand[i],data_model[i], data_mileage[i],data_year[i],data_usage[i],data_price[i]])
    
file.close()
