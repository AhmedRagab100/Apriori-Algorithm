import pandas 
from itertools import combinations
from collections import Counter
# Load data from Excel file
dataset= pandas.read_excel("CoffeeShopTransactions.xlsx")   #loading the coffe dataset

data = dataset.iloc[:, [3,4,5]]

# Convert the dataframe into a list of lists
transactions = []
for i in range(data.shape[0]):
    transaction = list(data.iloc[i]) #loop on number of rows and store in list of lists
    # convert to lowercase and remove spaces in words
    transaction = [word.lower().replace(' ', '') for word in transaction]
    transactions.append(transaction)



unique_items = []
#make list of unique items
for i in transactions:
    for q in i:
        if(q not in unique_items):
            unique_items.append(q)

#take input from user 
minimum_support = int(input("Please Enter the Minimum Support "))
minimum_confidence = float(input("Please Enter the Minimum_confidence "))

#get support count of each unique item 
item_sets = Counter()
for i in unique_items:
    for j in transactions:
        if(i in j):
            item_sets[i]+=1
            
print("1-itemset:")
print("****************************************")
for i in item_sets:
    print(str([i])+": "+str(item_sets[i])) #print each item and its support 
    

frequent_set = Counter()
for i in item_sets:
    if(item_sets[i] >= minimum_support):
        frequent_set[frozenset([i])]+=item_sets[i]
        print(frequent_set)
        
print("items_supported_1:")
print("****************************************") 
for i in frequent_set:
    print(str(list(i))+": "+str(frequent_set[i])) #print each item that support minimum support
    
    
prev_list = frequent_set
position = 1
#loop and get larger than 1-itemset
for count in range (2,1000):
    combination_set = set()
    temp = list(frequent_set)
    for i in range(0,len(temp)):
        for j in range(i+1,len(temp)):
            items_compinations = temp[i].union(temp[j])
            
            if(len(items_compinations) == count):
                combination_set.add(temp[i].union(temp[j]))
                
    item_sets = Counter()
    for i in combination_set:
        item_sets[i] = 0
        
        for q in transactions:
            temp = set(q)
            
            if(i.issubset(temp)):
                item_sets[i]+=1
    print(str(count)+"-"+"itemset")
    print("****************************************")
    for i in item_sets:
        print(str(list(i))+": "+str(item_sets[i]))
    
    frequent_set = Counter()
    for i in item_sets:
        if(item_sets[i] >= minimum_support):
            frequent_set[i]+=item_sets[i]
    print("items_supported"+"_"+str(count)+":")
    print("****************************************")
    for i in frequent_set:
        print(str(list(i))+": "+str(frequent_set[i]))
    
    if(len(frequent_set) == 0):
        break  
    
    prev_list = frequent_set
    position = count
    
    
print("Frequent-Sets: ")
print("items_supported"+"_"+str(position)+":")
print("****************************************")
for i in prev_list:
    print(str(list(i))+": "+str(prev_list[i]))
    
print("--------------------------------------")
print("generate Accossiation rules")
print("--------------------------------------")
    
def find_accossiations(prev_list, transactions):
    rules=set()
    for i in prev_list:
        c = [frozenset(q) for q in combinations(i,len(i)-1)]
        for item_1 in c:
            item_2 = i-item_1
            ab = i
            sab = 0
            sa = 0
            sb = 0
            
            for q in transactions:
                temp = set(q)
                if(item_1.issubset(temp)):
                    sa+=1
                if(item_2.issubset(temp)):
                    sb+=1
                if(ab.issubset(temp)):
                    sab+=1
            confidence_a = sab/sa*100
            confidence_b = sab/sb*100    
            
            if(confidence_a>minimum_confidence):
                    rule= str(list(item_1))+" -> "+str(list(item_2))+" = "+str(confidence_a)+"%"
                    rules.add(rule)
            
            if(confidence_b>minimum_confidence):
                    rule= str(list(item_2))+" -> "+str(list(item_1))+" = "+str(confidence_b)+"%"
                    rules.add(rule)
                
                
    for i in rules:
        print(i)

find_accossiations(prev_list,transactions)


