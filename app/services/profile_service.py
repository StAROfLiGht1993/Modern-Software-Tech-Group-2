#!/usr/bin/env python3

"""
Profile DB Services, run database queries for specific manipulations
"""

from sqlalchemy.orm import Session
from app.models.profile import Profile, ProfileInfo
from app.dependencies.auth import req_admin_role


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_profile(self):
        """
        Retrieve All Profiles
        """
        return self.db.query(Profile).all()

    def get_profile_username(self, username: str):
        """
        Retrieve Profile by Username
        """
        return self.db.query(Profile).filter(Profile.Username == username)
    
    def get_profile_id(self, email: str):
        """
        Retrieve Profile by Username
        """
        return self.db.query(Profile.UserID).filter(Profile.Email == email).first()

    def add_profile(self, profile_data: ProfileInfo):
        """
        Add a new profile
        """
        new_profile = Profile(**profile_data.model_dump())
        self.db.add(new_profile)
        self.db.commit()
        self.db.refresh(new_profile)

        return new_profile

    def update_profile(self, username: str, updated_data: ProfileInfo):
        """
        Update profile information
        """
        
        profile = self.get_profile_username(username)
        if not profile:
            return None
        for key, value in updated_data.model_dump().items():
            setattr(profile, key, value)
        self.db.commit()
        self.db.refresh(profile)

        return profile
    
    def delete_profile(self, username: str):
        """
        Delete a profile by Username - Admin Only
        """

        profile = self.get_profile_username(username)
        if not profile:
            return False
        self.db.delete(profile)
        self.db.commit()
        return True
