from django.shortcuts import render
import pandas as pd
import joblib
from example.models import AutismFormInput

# Load the model and preprocessing objects once at startup
model = joblib.load("notebook/support_vector_classifier.joblib")
label_encoder = joblib.load("notebook/label_encoder.joblib")
onehot_encoder = joblib.load("notebook/onehot_encoder.joblib")
scaler = joblib.load("notebook/standard_scaler.joblib")
features = joblib.load("notebook/features.joblib")

# Identify columns that were label encoded and onehot encoded
label_cols = ['gender', 'jundice', 'austim', 'used_app_before', 'age_desc']
onehot_cols = ['ethnicity', 'country_of_res', 'relation']


def predict(request):
    """
    Handles a two-step form submission:
    Step 1: Ask for age_desc, age, and demographics
    Step 2: Show the appropriate AQ-10 questionnaire based on age
    """
    step = request.GET.get('step', '1')

    if step == '1':
        # Step 1: Show form to get age_desc and age
        return render(request, "predict.html", {"step": "1"})
    elif step == '2':
        # Step 2: User has provided age_desc and age, now show the appropriate AQ-10 form
        age_desc = request.GET.get('age_desc')
        age = int(request.GET.get('age'))

        if 1 <= age <= 11:
            form_type = 'child_1_11'
        elif 12 <= age <= 17:
            form_type = 'child_12_17'
        else:
            form_type = 'adult_18'

        return render(request, "predict.html", {
            "step": "2",
            "form_type": form_type,
            "age_desc": age_desc,
            "age": age
        })


def result(request):
    # Retrieve user inputs
    a1_score = int(request.GET.get('a1_score', 0))
    a2_score = int(request.GET.get('a2_score', 0))
    a3_score = int(request.GET.get('a3_score', 0))
    a4_score = int(request.GET.get('a4_score', 0))
    a5_score = int(request.GET.get('a5_score', 0))
    a6_score = int(request.GET.get('a6_score', 0))
    a7_score = int(request.GET.get('a7_score', 0))
    a8_score = int(request.GET.get('a8_score', 0))
    a9_score = int(request.GET.get('a9_score', 0))
    a10_score = int(request.GET.get('a10_score', 0))

    total_score = sum([a1_score, a2_score, a3_score, a4_score, a5_score,
                       a6_score, a7_score, a8_score, a9_score, a10_score])

    age_desc = request.GET.get('age_desc')
    age = int(request.GET.get('age'))

    gender = request.GET.get('gender')
    ethnicity = request.GET.get('ethnicity')
    jundice = request.GET.get('jundice')
    austim = request.GET.get('austim')
    country_of_res = request.GET.get('country_of_res')
    used_app_before = request.GET.get('used_app_before')
    relation = request.GET.get('relation')

    # Construct a DataFrame from user input
    input_data = pd.DataFrame([[
        a1_score, a2_score, a3_score, a4_score, a5_score,
        a6_score, a7_score, a8_score, a9_score, a10_score,
        total_score, age_desc, age, gender, ethnicity,
        jundice, austim, country_of_res, used_app_before, relation
    ]], columns=['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score',
                 'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score',
                 'total_score', 'age_desc', 'age', 'gender', 'ethnicity',
                 'jundice', 'austim', 'country_of_res', 'used_app_before', 'relation']
    )

    # Apply stored LabelEncoders
    for col in label_cols:
        le = label_encoder[col]
        input_data[col] = le.transform(input_data[col])

    # One-hot encode columns
    onehot_input = onehot_encoder.transform(input_data[onehot_cols])
    onehot_df = pd.DataFrame(onehot_input, columns=onehot_encoder.get_feature_names_out(onehot_cols))

    # Drop original onehot columns and concatenate
    input_data = input_data.drop(onehot_cols, axis=1)
    input_data = pd.concat([input_data, onehot_df], axis=1)

    # Add interaction features
    input_data['age_total_product'] = input_data['age'] * input_data['total_score']
    input_data['age_total_ratio'] = input_data['total_score'] / (input_data['age'] + 1e-6)

    # Identify numerical features
    numerical_features = ['A1_Score', 'A2_Score', 'A3_Score', 'A4_Score', 'A5_Score',
                          'A6_Score', 'A7_Score', 'A8_Score', 'A9_Score', 'A10_Score',
                          'total_score', 'age', 'age_total_product', 'age_total_ratio']

    # Apply scaler
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])

    # Reorder columns
    input_data = input_data[features]

    # Predict
    y_pred = model.predict(input_data)

    # Determine final_result
    if y_pred[0] == 0:
        final_result = "Case of autism: No"
    else:
        final_result = "Case of autism: Yes"

    # Save the user input and predicted asd to the database in one go
    AutismFormInput.objects.create(
        a1_score=a1_score,
        a2_score=a2_score,
        a3_score=a3_score,
        a4_score=a4_score,
        a5_score=a5_score,
        a6_score=a6_score,
        a7_score=a7_score,
        a8_score=a8_score,
        a9_score=a9_score,
        a10_score=a10_score,
        total_score=total_score,
        age_desc=age_desc,
        age=age,
        gender=gender,
        ethnicity=ethnicity,
        jundice=jundice,
        austim=austim,
        country_of_res=country_of_res,
        used_app_before=used_app_before,
        relation=relation,
        asd=y_pred[0]
    )

    return render(request, "predict.html",
                  {"final_result": final_result,
                   "total_score": "Sum of scores from the 10 questions: " + str(total_score)})
