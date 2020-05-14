# This python script is used for the intension to clean up the lending club loan data.
# It's a big dataset and will require some cleaning, to make it easier for this project,
# I will do a one stop shop cleaning here.

#import time packages to measure how long this script took
import time
start = time.time()
# Importing required packages
import pandas as pd


# For my Part 2 - Predicitng Bad Loan notebook
# Read data
df = pd.read_csv('/Users/andrewberry/Downloads/lending-club-loan-data/loan.csv', low_memory=False)
print('data mounted')
# Removing columns that represent information that is not necessary or
# information available to lender prior to lending the loan
df = df.drop(['total_pymnt_inv','total_pymnt',
              'debt_settlement_flag','out_prncp',
              'last_pymnt_d','last_pymnt_amnt',
              'out_prncp_inv','total_rec_int',
              'total_rec_late_fee','recoveries',
              'collection_recovery_fee','total_rec_prncp',
              'total_rev_hi_lim','total_rec_int']
             ,axis = 1)
print('...cleaning')
#Dropping features with 30% or more missing data
df.dropna(thresh = 0.7*(len(df)), axis = 1, inplace = True)

#New Column representing year
df['year'] = pd.to_datetime(df.issue_d).dt.year

#Modified Code Below taken from https://www.kaggle.com/janiobachmann/lending-club-risk-analysis-and-metrics/notebook
#Determining the loans that are bad from loan_status column
#I want to convert the loan status to binary
bad_loan = ["Charged Off", "Default",
            "Does not meet the credit policy. Status:Charged Off",
            "In Grace Period",
            "Late (16-30 days)",
            "Late (31-120 days)"]

def loan_condition(status):
    if status in bad_loan:
        return 0 #bad loan
    else:
        return 1 #good loan

df['loan_status'] = df['loan_status'].apply(loan_condition)
print('...cleaning')
df = df.dropna(axis =0, how = 'any')

# Remove further categorical data points that have too many unique values
# Will put a strain on the model when trying to one-hot encode.
# In addition, I don't think these categorical data points adds much values
df = df.drop(['title','earliest_cr_line',
                          'last_credit_pull_d','issue_d',
                          'zip_code','emp_title','addr_state'],
                        axis = 1)
print('...cleaning')
#Saving the cleaned data
df.to_csv('/Users/andrewberry/Downloads/lending-club-loan-data/cleaned_lending_data.csv')
#I saved outside my repository because the file is huge, and rather not waste the github storage.

#Print how long it took to run this script in the terminal when running this
print (time.time()- start)
