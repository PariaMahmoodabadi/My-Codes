from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve
import tkinter as tk
from tkinter import ttk

# fetch dataset 
bank_marketing = fetch_ucirepo(id=222) 

# data (as pandas dataframes) 
X = bank_marketing.data.features 
y = bank_marketing.data.targets 

# metadata 
print(bank_marketing.metadata) 

# loading / reading Data
df = pd.DataFrame(bank_marketing.data.features)
# variable information 
print(bank_marketing.variables) 
print(df.info())  
print(df.describe())  
print(df.head())  
print(df.isnull().sum())

# clearing Data
df['job'] = df['job'].fillna('Unknown')
df['education'] = df['education'].fillna('Unknown')
df['contact'] = df['contact'].fillna('Unknown')
df['poutcome'] = df['poutcome'].fillna('Unknown')
df['age'] = df['age'].fillna(df['age'].mean())
df['balance'] = df['balance'].fillna(df['balance'].mean())

# Encoding categorical variables into numerical variables
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])

# Scaling numerical features
scaler = StandardScaler()
df[['age', 'balance', 'duration', 'campaign', 'previous']] = scaler.fit_transform(df[['age', 'balance', 'duration', 'campaign', 'previous']])
print(df.head())

# checking repeating Data
print("number of repeating ones: ", df.duplicated().sum())

# deleting repeating Data
df = df.drop_duplicates()

print(df.info())
print(df.describe())

# Splitting Data
X = df  # Features
y = bank_marketing.data.targets  # Target variable

# If y is a DataFrame, convert it to a Series
if isinstance(y, pd.DataFrame):
    y = y.iloc[:, 0]

encoder = LabelEncoder()
y = encoder.fit_transform(y)

#finding K with Ellbow method for kmeans
inertia = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

# draawing Elbow Method chart
plt.plot(K_range, inertia, marker='o')
plt.xlabel('number of clustrs (k)')
plt.ylabel('Inertia')
plt.title('finding K with Elbow Method')
plt.show()

#clustering with new K from Ellbow method
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)
print(df['cluster'].value_counts())

#duration from last call (changing into days)
df['last_contact_days'] = df['duration'].apply(lambda x: x / (24 * 60))  

# average of calls during last 6 moths
df['avg_contacts_last_6_months'] = df['previous'] / 6

print(df.head())

# Now you can split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check the shapes of the resulting datasets
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

#training RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# forcasting
y_pred = model.predict(X_test)

# analysing Model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# counting ROC-AUC
y_pred_proba = model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred_proba)
print("ROC-AUC Score:", roc_auc)

# drawing ROC chart
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

#predicting which customer will come back again
probabilities = model.predict_proba(X)  
df['Probability_Yes'] = probabilities[:, 1]  
sorted_data = df.sort_values(by='Probability_Yes', ascending=False)

#showing 10 customers with highest probabilities
print("10 customers with the highest probabilities")
print(sorted_data[['Probability_Yes']].head(10))

top_10_customers = sorted_data[['Probability_Yes']].head(10)
top_10_customers['customer_id'] = top_10_customers.index
top_10_customers = top_10_customers[['customer_id', 'Probability_Yes']]

# saving data in csv file
sorted_data.to_csv('existing_customers_predictions.csv', index_label='customer_id')

# Function to display the top 10 customers in a GUI window
def show_top_customers(df):
    root = tk.Tk()
    root.title("Top 10 Customers with Highest Probability of Returning")
    root.geometry("700x500")
    
    # Create a Treeview widget
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)
    
    tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
    tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    tree_scroll_y.pack(side="right", fill="y")
    tree_scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("Treeview", rowheight=30)

    # Add columns to the Treeview
    for col in df.columns:
        tree.heading(col, text=col)  
        tree.column(col, width=150, anchor="center")  
    
    # Add rows to the Treeview
    for i, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

    root.mainloop()

# Display the top 10 customers in a GUI window
show_top_customers(top_10_customers)