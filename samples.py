from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pickle

df= pickle.load(open("sample.pkl", 'rb'))
def calculate_score(row,inputset):
    intersection=len(row['set'].intersection(inputset))
    union = len(row['set'].union(inputset))
    return intersection/union

def Find_recommendation(name):
    if name in df['name'].tolist():
        inputset=df.loc[df['name'] == name, 'set'].iloc[0]
        temp=df[df['name']!=name]
        temp['score']=temp.apply(lambda row: calculate_score(row, inputset), axis=1)
        temp=temp.sort_values(by='score', ascending=False)
        top_5_rows = temp.iloc[:5, :]
        top_5_recommendation = top_5_rows['name'].tolist()
        return top_5_recommendation
    matches = process.extract(name, df['name'].tolist(), limit=1)
    if matches and matches[0][1] >= 80:  
        similar_name = matches[0][0]
        return f"Did you mean '{similar_name}'?"
    return f"'{name}' does not exist in the dataset."

v=input("enter the anime name:  ")
c= Find_recommendation(v)

print("---------------------------------")
for i in c:
    print(i)
print("---------------------------------")
