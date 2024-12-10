from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.config.database import get_db
from app.config.oauth import oauth
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.database import Account
from app.models.schemas import (Token, UserRegister, AccountResponse, 
                              AccountUpdate, AccountDelete)
from app.api.dependencies import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token."""
    db_user = db.query(Account).filter(Account.username == form_data.username).first()
    if not db_user or not db_user.hashed_password or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/login/google')
async def google_login(request: Request):
    """Initialize Google login flow."""
    try:
        redirect_uri = f"{request.url.scheme}://{request.url.netloc}/callback/google"
        request.session['oauth_redirect_uri'] = redirect_uri
        return await oauth.create_client('google').authorize_redirect(
            request,
            redirect_uri,
            access_type='offline',
            prompt='consent'
        )
    except Exception as e:
        print(f"Error in google_login: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get('/callback/{provider}')
async def social_callback_get(provider: str, request: Request, db: Session = Depends(get_db)):
    """Handle social media callback (OAuth flow)."""
    try:
        if provider != 'google':
            raise HTTPException(
                status_code=400,
                detail="Only Google authentication is supported"
            )

        oauth_client = oauth.create_client(provider)
        token = await oauth_client.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        social_id = user_info['sub']
        email = user_info['email']
        name = user_info['name']
        
        account = db.query(Account).filter(
            (Account.social_id == social_id) & 
            (Account.social_provider == provider)
        ).first()
        
        if not account:
            existing_email = db.query(Account).filter(Account.email == email).first()
            if existing_email:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered with different method"
                )
            
            username = f"{name.lower().replace(' ', '')}_{social_id[:8]}"
            account = Account(
                email=email,
                username=username,
                social_id=social_id,
                social_provider=provider
            )
            db.add(account)
            db.commit()
        
        access_token = create_access_token(data={"sub": account.username})
        
        return JSONResponse({
            "access_token": access_token,
            "token_type": "bearer"
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post('/callback/{provider}')
async def social_callback_post(provider: str, request: Request, db: Session = Depends(get_db)):
    """Handle social media token verification."""
    try:
        body = await request.json()
        token = body.get('token')
        email = body.get('email')
        name = body.get('name')

        if not token or not email:
            raise HTTPException(
                status_code=400,
                detail="Token and email are required"
            )

        account = db.query(Account).filter(Account.email == email).first()

        if not account:
            username = f"{name.lower().replace(' ', '_')}_{datetime.now().timestamp()}"
            account = Account(
                email=email,
                username=username,
                social_id=token,
                social_provider='google'
            )
            db.add(account)
            db.commit()

        access_token = create_access_token(data={"sub": account.username})
        
        return JSONResponse({
            "access_token": access_token,
            "token_type": "bearer"
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/register", response_model=Token)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(Account).filter(Account.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = db.query(Account).filter(Account.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    hashed_password = get_password_hash(user.password)
    new_user = Account(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/account/details", response_model=AccountResponse)
async def get_account_details(current_user: Account = Depends(get_current_user)):
    """Get current user's account details."""
    return AccountResponse(
        username=current_user.username,
        email=current_user.email,
        social_provider=current_user.social_provider
    )

@router.post("/account/update", response_model=Token)
async def update_account(
    update_data: AccountUpdate,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update account credentials."""
    if current_user.social_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Social login accounts cannot be updated through this endpoint"
        )

    if not verify_password(update_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    if update_data.new_username:
        existing_user = db.query(Account).filter(
            Account.username == update_data.new_username,
            Account.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = update_data.new_username

    if update_data.new_email:
        existing_user = db.query(Account).filter(
            Account.email == update_data.new_email,
            Account.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = update_data.new_email

    if update_data.new_password:
        current_user.hashed_password = get_password_hash(update_data.new_password)

    try:
        db.commit()
        access_token = create_access_token(data={"sub": current_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/account/delete")
async def delete_account(
    delete_data: AccountDelete,
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account."""
    if not current_user.social_provider:
        if not verify_password(delete_data.password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

    try:
        db.delete(current_user)
        db.commit()
        return {"message": "Account successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/test-auth")
async def test_auth(current_user: Account = Depends(get_current_user)):
    """Test authentication endpoint."""
    return {
        "message": "Authentication successful",
        "username": current_user.username,
        "social_provider": current_user.social_provider
    }
