'''

This script defines role-checking dependencies for the FastAPI endpoints.

'''

from app.services.cognito_service import RoleChecker, CognitoAdminRole, CognitoUserRole

# to ensure that users have the appropriate roles (admin or user) before accessing certain endpoint
req_admin_role = RoleChecker(CognitoAdminRole)
req_user_role = RoleChecker(CognitoUserRole)