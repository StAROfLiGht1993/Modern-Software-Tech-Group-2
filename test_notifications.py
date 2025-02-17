from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.auction import Auction
from app.models.profile import Profile
from app.models.notifications import Notification
from app.services.auction_service import AuctionInfo, AuctionService
from app.services.profile_service import ProfileService

# Get database session
db: Session = next(get_db())

# Create test users
user1 = Profile(UserID=1, Username='user1', Password='password', Email='user1@test.com', NumberOfRating=0, CurrentRating=0)
user2 = Profile(UserID=2, Username='user2', Password='password', Email='user2@test.com', NumberOfRating=0, CurrentRating=0)
user3 = Profile(UserID=3, Username='user3', Password='password', Email='user3@test.com', NumberOfRating=0, CurrentRating=0)

db.add(user1)
db.add(user2)
db.add(user3)
db.commit()

# Create a test auction with user1 as the highest bidder
auction = Auction(
    AuctionID=1,
    CardID=101,  # Assume some card ID
    SellerID=user1.UserID,
    MinimumIncrement=5.0,
    Status="In Progress",
    EndTime="2025-12-31 23:59:59",  # Some future date
    HighestBidderID=user2.UserID,
    HighestBid=100.0
)

db.add(auction)
db.commit()

# Simulate user3 placing a higher bid
bid_info = AuctionInfo(
    AuctionID=1,
    CardID=101,
    SellerID=user1.UserID,
    MinimumIncrement=5.0,
    Status="In Progress",
    HighestBidderID=user3.UserID,
    HighestBid=150.0
)

AuctionService.bid_auction(auction_id=1, user_id=user3.UserID, bid_info=bid_info)

# Fetch notifications for user1 (previous highest bidder)
notifications = db.query(Notification).filter(Notification.BidderID == user2.UserID).all()

# Output test results
if notifications:
    print("✅ Notification Created Successfully!")
    for n in notifications:
        print(f"Notification for User {n.BidderID}: {n.Message} at {n.TimeSent}")
else:
    print("❌ No notification was created!")

# Close database session
db.close()
