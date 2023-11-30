from src.models.account_model import AccountModel
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Create Account
@router.post("/accounts/")
def create_account(account_data: dict):
    account = AccountModel.add_account(account_data)
    if account:
        return {"message": "Account created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Account with same unique hash already exists")

# Get Account by ID
@router.get("/accounts/{account_id}")
def get_account(account_id: int):
    account = AccountModel.get_account_by_id(account_id)
    if account:
        return account.__dict__['_data']
    else:
        raise HTTPException(status_code=404, detail="Account not found")

# Update Account
@router.put("/accounts/{account_id}")
def update_account(account_id: int, update_data: dict):
    updated_account = AccountModel.update_account(account_id, **update_data)
    if updated_account:
        return updated_account.__dict__['_data']
    else:
        raise HTTPException(status_code=404, detail="Account not found")

# Delete Account
@router.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    success = AccountModel.delete_account(account_id)
    if success:
        return {"message": "Account deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Account not found")
    
# Assuming you've already imported the necessary modules and created the FastAPI router

@router.post("/accounts/filter")
def filter_accounts(filter_data: dict):
    # Your filtering logic goes here
    # Make sure to return a response (e.g., a list of filtered accounts)

    # Assuming AccountModel has a method for filtering accounts
    filtered_accounts = AccountModel.filter_accounts(filter_data)
    if filtered_accounts:
        return [account.__dict__['_data'] for account in filtered_accounts]
    else:
        raise HTTPException(status_code=404, detail="No matching accounts found")