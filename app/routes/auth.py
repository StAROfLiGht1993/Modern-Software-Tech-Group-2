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

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.services.cognito_service import CognitoService, CognitoAdminRole, RoleChecker
from app.exceptions import ServiceException
from app.models.profile import Profile
from app.db.db import get_db
import bcrypt

router = APIRouter()
cognito_service = CognitoService() #create instance of CognitoService

@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register(email: str, password: str, db: Session = Depends(get_db)):
    """
    Register a new user with a distinct email, and password.
    """
    try:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        response = cognito_service.register_user(email, password)
        user_sub = response["UserSub"]

        '''
        Create a new profile entry in the profiles table
        '''

        profile = Profile(
            Username=email,
            Password=hashed_password.decode('utf-8'),  # Store the hashed password
            Email=email,
            NumberOfRating=0, # Default 0 upon creation
            CurrentRating=0.0, # Default 0 upon creation
            PhoneNumber=None,
            CognitoUserID=user_sub
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        return {
            "message": "User registration successful.",
            "user_sub": response["UserSub"],
            "user_confirmed": response["UserConfirmed"]
        }
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

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

@router.delete("/profiles/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(username: str, service: CognitoService = Depends(), db: Session = Depends(get_db), claims: dict = Depends(RoleChecker(CognitoAdminRole))):
    """
    Delete a profile by Username - Admin only
    """
    if not service.delete_profile(username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return {"detail": "Profile deleted successfully"}

