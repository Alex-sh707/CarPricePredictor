import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

from sklearn import preprocessing
brand_encoder = preprocessing.LabelEncoder()
model_encoder = preprocessing.LabelEncoder()
usage_encoder = preprocessing.LabelEncoder()

df = pd.read_csv("Mycsv.csv")

def get_label(brand_label , model_label , use_label) :
    brand = brand_encoder.transform([brand_label])[0]
    model = model_encoder.transform([model_label])[0]
    use = usage_encoder.transform([use_label])[0]
    return brand , model , use 

# print(df.describe())
# print(df.head())

"""
print(df.isna().sum()) 

Brand       0
Model       0
Mileage      0
Year      137
Usage       0
Price         0

only the Year coulm has missing values and its not much comparing to our df size so its better to 
delete rows with missing values.

"""

df.dropna(axis=0 ,inplace=True, how="any") # deleting all the rows which has at least one NaN

# splitting x and y

def prediction_price(brand , model , mileage , year , usage) :
    
    df= pd.read_csv("Mycsv.csv")
    df.dropna(axis=0 ,inplace=True, how="any") # deleting all the rows which has at least one NaN
    df = df.drop_duplicates(subset=None, keep="first", inplace=False) # deleting all repeated rows

    x_data = df[["Brand" ,"Model", "Mileage" , "Year" , "Usage"]]

    # x_data = df[["Brand" , "Model" , "Mileage" , "Year" , "Usage"]]
    y_data = df["Price"]

    # turning string types into int 

    x_data["Brand"] = brand_encoder.fit_transform(x_data["Brand"])
    x_data["Model"] = model_encoder.fit_transform(x_data["Model"])
    x_data["Usage"] = usage_encoder.fit_transform(x_data["Usage"])

    
    # converting our pandas data frame into numpy array
    X = np.asanyarray(x_data[["Brand" ,"Model" ,  "Mileage", "Year" , "Usage"]] , dtype="int")
    # X = x_data.to_numpy(dtype="int")
    Y = y_data.to_numpy(dtype="int")


    # normalizing the data

    from sklearn import preprocessing
    # scaler = preprocessing.StandardScaler().fit(X)
    scaler = preprocessing.Normalizer().fit(X)
    X = scaler.transform(X)

    # To avoid overfitting we split the data into two part  
    # We will also test our model to see how accurate is that 

    from sklearn.model_selection import train_test_split

    X_train , X_test , Y_train , Y_test = train_test_split(X, Y ,test_size=.05 , random_state=1 , shuffle=True)
    # the data is very limited so test_size cant be more than this

    # Making the model with linear reg

    """
    from sklearn import linear_model

    reg = linear_model.LinearRegression()
    reg.fit(X_train , Y_train)

    predict = reg.predict(X_test)

    from sklearn.metrics import r2_score
    print(r2_score(Y_test , predict)) --> 0.222404043873498

    The linear model is not suitable for our data

    """

    # Making the model with ploy

    from sklearn import linear_model
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.metrics import r2_score
    
    
    reg = linear_model.LinearRegression()
    reg_best = linear_model.LinearRegression()
    max_score = 0.0
    max_degree = 0

    for k in range(2,10) :
        
        poly = PolynomialFeatures(degree=k)
        X_poly = poly.fit_transform(X_train)
        reg.fit(X_poly , Y_train)
        
        
        X_test_poly = poly.fit_transform(X_test)
        prediction = reg.predict(X_test_poly)


        score = float(r2_score(Y_test , prediction))
        if score > max_score : # finding the best degree for our Poly model
            max_score = score
            max_degree = k
    
    
    # print(f"The best result is {max_score}% with {max_degree} degree")


    # making final model
    # The best result is 0.72% with 8 degree
    # The result that we've got from polynomial model was almost satisfying 
    # so we are keeping it as our main model !!!


    poly_best = PolynomialFeatures(degree=max_degree)
    X_poly = poly_best.fit_transform(X_train)
    reg_best.fit(X_poly , Y_train)
    
    
    
    
    brand , model , usage = get_label(brand , model , usage)

    X_pre = np.array([[brand , model , mileage , year , usage]])
    X_pre = scaler.transform(X_pre)
    X_linear = poly_best.fit_transform(X_pre)
    Prediction_price = reg_best.predict(X_linear)
    
    print(f"Your cars price is estimated around ${int(Prediction_price[0])} dollars")
    
# for example : prediction_price("lamborghini" , "Aventador" , 2018 , 600 , "Used")