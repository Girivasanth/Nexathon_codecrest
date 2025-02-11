from flask import Flask, render_template
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load models
iqr_model = joblib.load("student_priority_model.pkl")
std_model = joblib.load("student_priority_sd_model.pkl")

CSV_FILE = "mark_list.csv"

# Function to calculate IQR
def calculate_iqr(marks):
    q1 = np.percentile(marks, 25)
    q3 = np.percentile(marks, 75)
    return q3 - q1

def process_data():
    """Process data for both IQR and Std tables."""
    df = pd.read_csv(CSV_FILE)

    # IQR-based Priority Table
    df_iqr = df.copy()
    subject_columns = df.columns[1:]

    # Compute IQR
    df_iqr["IQR"] = df_iqr[subject_columns].apply(lambda row: calculate_iqr(row.values), axis=1)

    # Count failed subjects (assuming pass mark is 40)
    PASS_MARK = 40
    df_iqr["Failed_Subjects"] = df_iqr[subject_columns].apply(lambda row: (row < PASS_MARK).sum(), axis=1)

    # Ensure both features are passed
    df_iqr["Predicted Priority"] = iqr_model.predict(df_iqr[["IQR", "Failed_Subjects"]])
    df_iqr["Predicted Priority"] = df_iqr["Predicted Priority"].map({0: "Low", 1: "Medium", 2: "High"})
    iqr_table_html = df_iqr.to_html(classes="table table-bordered", index=False)

    # Mean & Std Dev Attention Table
    df_std = df.copy()
    df_std["Mean"] = df_std.iloc[:, 1:].mean(axis=1)
    df_std["StdDev"] = df_std.iloc[:, 1:].std(axis=1)
    df_std["Attention"] = std_model.predict(df_std[["Mean", "StdDev"]])
    df_std["Attention"] = df_std["Attention"].apply(lambda x: "Needs Attention" if x == 1 else "No Attention Needed")
    std_table_html = df_std.to_html(classes="table table-bordered", index=False)

    return iqr_table_html, std_table_html

@app.route("/")
def index():
    iqr_table, std_table = process_data()
    return render_template("ind.html", iqr_table=iqr_table, std_table=std_table)

if __name__ == "__main__":
    app.run(debug=True)
