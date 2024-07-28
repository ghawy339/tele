import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)
    
    # حساب عدد الإشارات الخاطئة
    FP = matrix[0][1]
    FN = matrix[1][0]
    false_signals = FP + FN
    true_signals = matrix[0][0] + matrix[1][1]
    
    return report, matrix, false_signals, true_signals

if __name__ == "__main__":
    best_model = joblib.load('../models/best_model.pkl')
    X_test = pd.read_csv('../data/X_test.csv')
    y_test = pd.read_csv('../data/y_test.csv').values.ravel()
    report, matrix, false_signals, true_signals = evaluate_model(best_model, X_test, y_test)
    
    print("Classification Report:\n", report)
    print("Confusion Matrix:\n", matrix)
    print("Number of false signals:", false_signals)
    print("Number of true signals:", true_signals)
