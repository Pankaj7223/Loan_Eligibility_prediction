# EligifyAI - Loan Eligibility Prediction

EligifyAI is a machine learning-powered web application designed to predict loan eligibility for users. It leverages a hybrid approach combining machine learning models with business logic to provide accurate and explainable loan approval predictions.

## Features

- **Loan Eligibility Prediction**: Predicts whether a user is eligible for a loan based on their details.
- **Hybrid Logic**: Combines ML predictions with business rules (e.g., CIBIL score checks, Income/Loan ratios).
- **User Authentication**: Secure Login and Sign-Up functionality.
- **Responsive Design**: Modern UI built with Tailwind CSS, fully responsive for mobile and desktop.
- **Interactive UI**: Real-time feedback and validation.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: version 3.12 or higher
- **Git**: for version control
- **Web Browser**: Chrome, Edge, or Firefox

## Installation & Setup

Follow these steps to set up the project locally on your machine.

### 1. Clone the Project

```bash
git clone https://github.com/Pankaj7223/Loan_Eligibility_prediction.git
cd Loan_Eligibility_prediction
```

### 2. Set Up Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Create the environment:**
```bash
python -m venv env
```

**Activate the environment:**
- **Windows:**
  ```bash
  .\env\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source env/bin/activate
  ```

### 3. Install Dependencies

Navigate to the directory containing `requirements.txt` (usually inside `Prediction` folder or root) and install the required packages.

```bash
cd Prediction
pip install -r requirements.txt
```

*(Note: Ensure you are in the directory where `requirements.txt` is located. If it's in the root, run the command from there.)*

### 4. Run the Application

Perform database migrations (if needed) and start the development server.

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Access the Website

Open your web browser and go to:

```
http://localhost:8000/
```

## Project Structure

- **Prediction/**: Main Django project folder.
- **Eloan/**: Django app containing views, models, and templates.
- **templates/**: HTML templates for the frontend.
- **static/**: Static assets (CSS, Images, JS).
- **ML_model/**: Contains the trained machine learning model (`loanprediction_model.sav`).

## Update the Project

To pull the latest changes and update your local setup:

```bash
git pull origin main
.\env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
