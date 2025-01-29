from rest_framework.exceptions import APIException

class InvalidLoanParametersError(APIException):
    status_code = 400
    default_detail = 'Invalid loan parameters provided.'
    default_code = 'invalid_loan_parameters'

class LoanCalculationError(APIException):
    status_code = 400
    default_detail = 'Error calculating loan details.'
    default_code = 'loan_calculation_error'

