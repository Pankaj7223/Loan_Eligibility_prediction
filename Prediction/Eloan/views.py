from django.shortcuts import render ,  redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from Eloan.models import *
from Eloan.models import NewUser
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import LoanPredictionForm
import joblib
import numpy as np
import pandas as pd
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create your views here.
def wellcome(request):
    return render(request, 'index.html')

def signin(request):
    value = None

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Hash the user's password
        hashed_password = make_password(password)

        try:
            newuser = NewUser.objects.create(username=username, email=email, password=hashed_password)
            newuser.save()
            value = 3  # User created successfully
            request.session['username']=newuser.username
        except IntegrityError as e:
            if 'UNIQUE constraint failed: carapp_newuser.email' in str(e):
                value = 2  # Email already exists
            else:
                value = 1
                
    else:
        return render(request, 'signin.html')

    context = {'value': value}
    return render(request, 'signin.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = NewUser.objects.get(username=username)
            if check_password(password, user.password):
                # Password matches
                request.session['username'] = user.username
                res = render(request, 'home.html')
            else:
                # Password doesn't match
                LoginError = "Invalid Username or Password.."
                res = render(request, 'login.html', {'LoginError': LoginError})
        except NewUser.DoesNotExist:
            # User not found
            LoginError = "Invalid Username or Password.."
            res = render(request, 'login.html', {'LoginError': LoginError})
    else:
        if 'username' in request.session.keys():
            res = render(request, 'home.html')
        else:
            res = render(request, 'login.html')
    return res


def home(request):
    if 'username'  in  request.session.keys():
        return render(request,'home.html')
    else:
        return HttpResponseRedirect('/login')

def about(request):
    if 'username' in request.session.keys():
        return render(request, 'about.html')
    else:
        return HttpResponseRedirect('/login')

def contact(request):
    if 'username' in request.session.keys():
        return render(request, 'contact.html')
    else:
        return HttpResponseRedirect('/login')

def faq(request):
    if 'username' in request.session.keys():
        return render(request, 'faq.html')
    else:
        return HttpResponseRedirect('/login')


import os
from django.conf import settings

# Load model safely
model_path = os.path.join(settings.BASE_DIR, 'ML_model', 'loanprediction_model.sav')
try:
    model = joblib.load(model_path)
    logger.info(f"Model loaded successfully from {model_path}")
except Exception as e:
    model = None
    logger.error(f"Failed to load model from {model_path}: {e}")

# Create your views here.
def prediction(request):
    if request.method == 'POST':
        form = LoanPredictionForm(request.POST)
        if form.is_valid():
            try:
                # Extract cleaned data
                data = form.cleaned_data
                
                # Create DataFrame with raw values (pipeline handles encoding)
                df_data = {
                    'no_of_dependents': [data['no_of_dependents']],
                    'education': [data['education']],
                    'self_employed': [data['self_employed']],
                    'income_annum': [data['income_annum']],
                    'loan_amount': [data['loan_amount']],
                    'loan_term': [data['loan_term']],
                    'cibil_score': [data['cibil_score']],
                    'residential_assets_value': [data['residential_assets_value']],
                    'luxury_assets_value': [data['luxury_assets_value']],
                    'bank_asset_value': [data['bank_asset_value']],
                }
                
                df = pd.DataFrame(df_data)
                
                # --- Business Logic / Heuristic Rules (Hybrid Approach) ---
                # Real-world banking rules to override or supplement ML model
                
                cibil = data['cibil_score']
                income = data['income_annum']
                loan = data['loan_amount']
                assets = data['residential_assets_value'] + data['luxury_assets_value'] + data['bank_asset_value']
                
                rejection_reason = None
                
                # Rule 1: Minimum CIBIL Score
                if cibil < 600:
                    rejection_reason = "CIBIL Score is too low (Minimum 600 required)."
                    
                # Rule 2: Loan to Income Ratio (Max 20x income is generous, usually it's less)
                elif loan > (income * 20):
                    rejection_reason = "Loan amount is too high compared to annual income."
                    
                # Rule 3: Asset Coverage (Loan shouldn't exceed Income*10 + Assets significantly)
                elif loan > (income * 10 + assets):
                    rejection_reason = "Insufficient income and assets to cover the loan amount."

                if rejection_reason:
                    # Force Rejection based on Business Rules
                    result = "Not Eligible"
                    status = 'success'
                    # Pass the reason to the template if needed (optional)
                    logger.info(f"Loan Rejected by Business Rule: {rejection_reason}")
                
                elif model:
                    pred = model.predict(df)[0]
                    # Prediction is 1 (Eligible) or 0 (Not Eligible)
                    result = 'Eligible' if pred == 1 else "Not Eligible"
                    status = 'success'
                    if result == "Not Eligible":
                        rejection_reason = "AI Model determined high risk based on historical data."
                else:
                    result = "Model not loaded. Please contact support."
                    status = 'error'
                    logger.error("Prediction attempted but model is not loaded.")

                # Check if AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    response_data = {
                        'status': status, 
                        'prediction': result
                    }
                    if rejection_reason:
                        response_data['reason'] = rejection_reason
                    return JsonResponse(response_data)
                
                return render(request, 'prediction.html', {'prediction': result, 'form': form, 'reason': rejection_reason})

            except Exception as e:
                logger.error(f"Prediction error: {e}")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': str(e)})
                return render(request, 'prediction.html', {'prediction': f"Error: {str(e)}", 'form': form})
        else:
            # Form invalid
            logger.warning(f"Invalid form submission: {form.errors}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                 return JsonResponse({'status': 'error', 'errors': form.errors})
            return render(request, 'prediction.html', {'form': form})

    else:
        form = LoanPredictionForm()
    
    return render(request, 'prediction.html', {'form': form})


    
def team(request):
    if 'username'  in  request.session.keys():
        return render(request,'team.html')
    else:
        return HttpResponseRedirect('/login')

def logout(request):
    if 'username'  in  request.session.keys():
        request.session.pop('username')
    return HttpResponseRedirect('login')