import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class DemandForecaster:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def train(self, df):
        """Trains the Random Forest model on historical data."""
        if df.empty:
            return
            
        # Features: day of week, month, is_weekend
        X = df[['day_of_week', 'month', 'is_weekend']]
        y = df['demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        return mae
        
    def predict_next_week(self):
        """Predicts demand for the next 7 days."""
        if not self.is_trained:
            return np.zeros(7)
            
        # Create a dummy dataframe for the next 7 days
        # Assuming today is Monday (0) for simplicity in this mock
        next_days = []
        for i in range(7):
            day_of_week = i % 7
            is_weekend = 1 if day_of_week >= 5 else 0
            month = 5 # arbitrary month for prediction
            next_days.append([day_of_week, month, is_weekend])
            
        X_pred = pd.DataFrame(next_days, columns=['day_of_week', 'month', 'is_weekend'])
        predictions = self.model.predict(X_pred)
        
        return predictions
