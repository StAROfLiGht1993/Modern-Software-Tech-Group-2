'''
This file defines the authentication endpoints for the FastAPI application.

1. User registration
2. User login
3. User confirmation

# to do:
- modify the codes to do confirmation using email instead of username
- add sso login and/or social login (e.g. google, facebook, etc.) using cognito
- add a new endpoint for password reset
- check exception handling for all endpoints (errors for multiple failed attempts)
- add a new endpoint for user logout
- add a new endpoint for user deletion
- add a new endpoint for user profile update
- add a new endpoint for user profile retrieval
- customise confirmation email template (e.g. add logo, change text, etc.)
- MFA (multi-factor authentication) for login, confirmation
'''

from fastapi import APIRouter, HTTPException, status
from app.services.cognito_service import CognitoService
from app.exceptions import ServiceException

router = APIRouter()
cognito_service = CognitoService() #create instance of CognitoService

# ------------ update registration to only accept email ----------------------------
# @router.post("/registration", status_code=status.HTTP_201_CREATED)
# def register(username: str, email: str, password: str):
#     """
#     Register a new user with a distinct username, email, and password.
#     """
#     try:
#         response = cognito_service.register_user(username, email, password)
#         return {
#             "message": "User registration successful.",
#             "user_sub": response["UserSub"],
#             "user_confirmed": response["UserConfirmed"]
#         }
#     except ServiceException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register(email: str, password: str):
    """
    Register a new user with a distinct email, and password.
    """
    try:
        response = cognito_service.register_user(email, password)
        return {
            "message": "User registration successful.",
            "user_sub": response["UserSub"],
            "user_confirmed": response["UserConfirmed"]
        }
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


# ---------------------- End of update ---------------------------------


# ---------------------- Update the login endpoint to use email instead of username ---------------------- 
# @router.post("/login")
# def login(username: str, password: str):
#     """
#     Login endpoint to authenticate users and return a JWT token.
#     """
#     try:
#         tokens = cognito_service.authenticate_user(username, password)
#         return {"message": "Login successful", "tokens": tokens}
#     except ServiceException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

#update router to use email as login parameter instead of username
@router.post("/login")
def login(email: str, password: str):
    """
    Login endpoint to authenticate users and return a JWT token.
    """
    try:
        tokens = cognito_service.authenticate_user(email, password)
        return {"message": "Login successful", "tokens": tokens}
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

#----------------------------- End of update ---------------------------------  

# ---------------------- Update the confirmation endpoint to use email instead of username ---------------------- 
# Can we improve the code quality of the following endpoint implementation?
# @router.post("/confirmation")
# def confirm(username: str, confirmation_code: str):
#     """
#     Confirm the user's email address using the code sent by Cognito.
#     """
#     try:
#         # Confirm sign-up
#         cognito_service.client.confirm_sign_up(
#             ClientId=cognito_service.client_id,
#             Username=username,
#             ConfirmationCode=confirmation_code,
#             SecretHash=cognito_service.calculate_secret_hash(username)
#         )

#         return {"message": "User confirmed successfully."}

#     except ServiceException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

#update router to use email as login parameter instead of username
@router.post("/confirmation")
def confirm(email: str, confirmation_code: str):
    """
    Confirm the user's email address using the code sent by Cognito.
    """
    try:
        # Confirm sign-up
        cognito_service.confirm_user(
            email=email,
            confirmation_code=confirmation_code,
        )

        return {"message": "User confirmed successfully."}

    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
#----------------------------- End of update ---------------------------------

# add new endpoint for resend confirmation code
@router.post("/resend-confirmation-code")
def resend_confirmation_code(email: str):
    """
    Resend the confirmation code to the user's email address.
    """
    try:
        cognito_service.resend_confirmation_code(email)
        return {"message": "Confirmation code resent successfully."}
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
# add new endpoint for list users
@router.get("/get-all-users")
def list_users():
    """
    List all users in the user pool.
    """
    try:
        users = cognito_service.list_users()
        return {"users": users}
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)