import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load preprocessed data
df = pd.read_csv('dataset/data_preprocessed.csv')

# Feature and label selection
features = ['id'] + [f'data[{i}]' for i in range(8)]
X = df[features]
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'can_ids_model.pkl')
print("Model saved as can_ids_model.pkl")