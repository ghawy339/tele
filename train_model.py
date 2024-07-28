import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import joblib

def train_model(df):
    X = df[['rsi', 'sma', 'ema', 'macd', 'macd_signal', 'macd_hist', 'bb_upper', 'bb_middle', 'bb_lower', 'adx', 'stoch_k', 'stoch_d', 'atr', 'cci']]
    y = (df['close'].shift(-1) > df['close']).astype(int)
    
    # توازن البيانات
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X, y)
    
    # تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestClassifier()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    
    return best_model, X_test, y_test

if __name__ == "__main__":
    df = pd.read_csv('../data/ohlcv_data_with_features.csv', index_col='timestamp', parse_dates=True)
    best_model, X_test, y_test = train_model(df)
    joblib.dump(best_model, '../models/best_model.pkl')
    pd.DataFrame(X_test).to_csv('../data/X_test.csv', index=False)
    pd.DataFrame(y_test).to_csv('../data/y_test.csv', index=False)
