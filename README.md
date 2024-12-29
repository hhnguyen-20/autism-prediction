# Django + Render

A machine learning model that predicts whether a person has autism spectrum disorder (ASD) based on their demographic
information and responses to a questionnaire. The model is deployed using Django and Render.

## Live Demo

https://autism-earlycheck.onrender.com

## Google Colab Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1WW-IxgT9LA3Nf52Tiu29kcGeC-Du8jew?usp=sharing)

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/hhnguyen-20/autism-prediction.git
cd autism-prediction
```

2. Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project and add the following environment variables:

`
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
`

4. Run the app:

```bash
python manage.py runserver
```

Your Django application is now available at `http://127.0.0.1:8000`.

