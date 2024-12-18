# import all library
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib # for saving algorithm and preprocessing objects

# Load the preprocessed dataset
df = pd.read_csv("autism_data.csv")

# Identify categorical columns that were label encoded
label_cols = ['gender', 'jundice', 'austim', 'used_app_before', 'age_desc']

# Fit LabelEncoders on the entire dataset for these cols
label_encoder = {}
for col in label_cols:
    # Initialize LabelEncoder
    le = LabelEncoder()

    df[col] = le.fit_transform(df[col])

    label_encoder[col] = le

# Identify categorical columns that need one-hot encoding
onehot_cols = ['ethnicity', 'country_of_res', 'relation']

# Initialize OneHotEncoder
onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Apply OneHot Encoding to onehot columns
encoded_array = onehot_encoder.fit_transform(df[onehot_cols])
encoded_df = pd.DataFrame(encoded_array, columns=onehot_encoder.get_feature_names_out(onehot_cols))

# Drop original onehot columns and concat encoded features
df = df.drop(onehot_cols, axis=1)
df = pd.concat([df, encoded_df], axis=1)

# Add interaction features if they were originally added
df['age_total_product'] = df['age'] * df['total_score']
df['age_total_ratio'] = df['total_score'] / (df['age'] + 1e-6)

# Select numerical features for scaling
numerical_features = ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score',
                      'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score',
                      'total_score', 'age', 'age_total_product', 'age_total_ratio']

# Initialize StandardScaler
scaler = StandardScaler()

# Fit and transform the numerical features
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Define features and target
X = df.drop(['ASD'], axis=1)
y = df['ASD']

# Keep track of feature names for ordering new inputs
features = X.columns.tolist()

# Split into training and test sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM
model = SVC(kernel='linear', random_state=42)
model.fit(X_train, y_train)

# Save model and preprocessing objects
joblib.dump(model, "./support_vector_classifier.joblib", compress=True)
joblib.dump(label_encoder, "./label_encoder.joblib", compress=True)
joblib.dump(onehot_encoder, "./onehot_encoder.joblib", compress=True)
joblib.dump(scaler, "./standard_scaler.joblib", compress=True)
joblib.dump(features, "./features.joblib", compress=True)
