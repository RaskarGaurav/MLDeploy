import joblib
from math import radians, cos, sin, sqrt, atan2
import pandas as pd
from scipy.sparse import hstack,csr_matrix
import numpy

transFormer = joblib.load(open('Models/PowerTransform_StdScaling_model.pkl', 'rb'))
enCoder = joblib.load(open('Models/oneHotEncoder_model.pkl', 'rb'))
selectFeatures = joblib.load(open('Models/feature_selection_model.pkl', 'rb'))
predmodel = joblib.load(open('Models/xgBoost_model.pkl', 'rb'))

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def outRemove(x):
    if x>3: return 3
    elif x<-3: return -3
    else: return x

def transForm(df):
    df = df.copy()
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['amt'] = df['amt'].astype("float64")
    df['zip'] = df['zip'].astype("int64")
    df['lat'] = df['lat'].astype("float64")
    df['long'] = df['long'].astype("float64")
    df['city_pop'] = df['city_pop'].astype("int64")
    df['dob'] = pd.to_datetime(df['dob'])
    df['merch_lat'] = df['merch_lat'].astype("float64")
    df['merch_long'] = df['merch_long'].astype("float64")
    df['merch_zipcode'] = df['merch_zipcode'].astype("int64")
    df['trans_count_per_day'] = df['trans_count_per_day'].astype("int64")
    buff = df['trans_count_per_day']
    df.drop("trans_count_per_day",axis=1,inplace=True)
    
    #Converting DoB to Age
    df['age'] = df['trans_date_trans_time'].dt.year - df['dob'].dt.year 
    df.drop("dob",axis=1,inplace=True)
    
    #Calculating Distance Between Customer & Merchant
    df['transaction_distance'] = df.apply(lambda x: haversine(x['lat'], x['long'], x['merch_lat'], x['merch_long']), axis=1)
    
    #Transaction Seconds from Mid-Night
    df['sec_from_midnight'] = df['trans_date_trans_time'].dt.hour * 3600 + df['trans_date_trans_time'].dt.minute * 60 + df['trans_date_trans_time'].dt.second
    
    #Transaction Frequency
    df['trans_count_per_day'] = buff
    
    #Dropping unwanted cols
    df.drop("trans_date_trans_time",axis=1,inplace=True)
    
    
    
    
    #PowerTransform
    numericCols = df.select_dtypes(exclude="object").columns
    nonNumericCols = df.select_dtypes("object").columns
    
    df[numericCols] = transFormer.transform(df[numericCols])
    
    #OutLiers Handling
    df[numericCols] = df[numericCols].applymap(outRemove)
    
    #Remove Corelated cols
    colsRemove= ['merch_long','merch_lat','merch_zipcode','long']
    df.drop(colsRemove,axis=1,inplace=True)
    
    #Encoding
    numericCols = df.select_dtypes(exclude="object").columns
    nonNumericCols = df.select_dtypes("object").columns
    df_NonNumeric = df[nonNumericCols]
    df_Numeric = df[numericCols]
    
    df_NonNumeric_np = enCoder.transform(df_NonNumeric)
    df_Numeric_np = csr_matrix(df_Numeric.values)
    
    df = hstack([df_Numeric_np, df_NonNumeric_np])
    
    #Feature Selection
    df = selectFeatures.transform(df)
    
    prob = predmodel.predict_proba(df)[0][1]
    
    return float(prob)