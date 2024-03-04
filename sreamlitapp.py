import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Set page title
st.set_page_config(page_title="Online P2P lending markets App")
st.title("Welcome to our Online P2P lending markets App")

# create a checkbox to toggle between loan and ROI predictions
predict_roi_checkbox = st.checkbox("ROI Predictions", value=False)

# loading the saved models
loaded_model = pickle.load(open(r'C:\Users\Elsayedmohamedelsaye\Logistic_model.sav', 'rb'))
loaded_model_ROI = pickle.load(open(r'C:\Users\Elsayedmohamedelsaye\randomForest_model.sav', 'rb'))

# creating a function for loan status prediction
def Loanstatus_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)
    if (prediction[0] == 0):
        return 'Loan Rejected'
    else:
        return 'Loan Accepted'


# Define the ROIprediction function
def ROIprediction(input_data):
    # Convert input data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # Reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Make predictions using the loaded model
    roi_emi_prediction = loaded_model_ROI.predict(input_data_reshaped)

    # Check that the roi_emi_prediction array has two elements
    if roi_emi_prediction.shape == (1, 2):
        roi_emi_prediction = roi_emi_prediction.reshape(2,)

    # Separate the ROI and EMI predictions
    roi_prediction, emi_prediction = roi_emi_prediction[0], roi_emi_prediction[1]

    # Return the predicted ROI and EMI values
    return roi_prediction, emi_prediction

if predict_roi_checkbox:
    # display the user inputs for ROI predictions
    st.header('ROI and EMI Predictions')

    # getting the input data from the user
    LP_ServiceFees = st.text_input('LP_ServiceFees')
    LoanOriginalAmount = st.text_input('LoanOriginalAmount')
    MonthlyLoanPayment = st.text_input('MonthlyLoanPayment')
    LP_CustomerPrincipalPayments = st.text_input('LP_CustomerPrincipalPayments')
    BorrowerRate2 = st.text_input('BorrowerRate')
    LP_CustomerPayments = st.text_input('LP_CustomerPayments')
    EstimatedLoss = st.text_input('EstimatedLoss')
    EstimatedEffectiveYield = st.text_input('EstimatedEffectiveYield')
    BorrowerAPR2 = st.text_input('BorrowerAPR')
    EstimatedReturn = st.text_input('EstimatedReturn')
    LenderYield2 = st.text_input('LenderYield')
    LoanMonthsSinceOrigination = st.text_input('LoanMonthsSinceOrigination')
    


    # creating a button for ROI prediction
    if st.button('Predict ROI'):
        roi_pred, emi_pred = ROIprediction(
            [BorrowerAPR2, EstimatedReturn, EstimatedEffectiveYield, MonthlyLoanPayment, LP_CustomerPayments,
             LP_CustomerPrincipalPayments, LoanOriginalAmount, LoanMonthsSinceOrigination, LenderYield2, BorrowerRate2,EstimatedLoss,LP_ServiceFees])

        # display the predicted ROI and EMI values to the user
        st.write(f"Predicted ROI: {roi_pred}")
        st.write(f"Predicted EMI: {emi_pred}")
else:
    # display the user inputs for loan predictions
    st.header('Loan Status Predictions')

    # getting the input data from the user
    LoanCurrentDaysDelinquent = st.text_input('Number of Delinquent days')
    LP_GrossPrincipalLoss = st.text_input('The gross charged off amount of the loan')
    LP_NetPrincipalLoss = st.text_input('The principal that remains uncollected after any recoveries')
    LoanStatus_Chargedoff = st.text_input('if LoanStatus Chargedoff')
    LoanStatus_Current = st.text_input('if it is a current Loan Status')
    BorrowerAPR = st.text_input("The Borrower's Annual Percentage Rate")
    EstimatedReturn = st.text_input('The estimated Return')
    BorrowerRate = st.text_input("The Borrower's interest rate for this loan")
    LenderYield = st.text_input('The Lender yiled on the loan')
    LP_CustomerPrincipalPayments = st.text_input('Pre charge-off cumulative principal ')

    # creating a button for loan status prediction
    if st.button('Predict Loan Status'):
        pred = Loanstatus_prediction([LoanCurrentDaysDelinquent,LP_GrossPrincipalLoss,LP_NetPrincipalLoss,LoanStatus_Chargedoff,LoanStatus_Current,BorrowerAPR,EstimatedReturn,BorrowerRate,LenderYield,LP_CustomerPrincipalPayments])

        # display the prediction to the user using a radio button
        if pred:
            loan_status = st.radio('Loan Status:', ['Loan Rejected', 'Loan Accepted'],
                                   index=1 if pred == 'Loan Accepted' else 0)
