from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.database import get_db
from app.schemas.user import UserDTO

router = APIRouter()

@router.get("/users/login", status_code=200)
async def login():
    return HTMLResponse(content="""
    <body>
    <form action="http://localhost:8000/users/login" method="post" style="width: 400px; margin: 50 auto">
    
        <div class="imgcontainer">
          <img src="img_avatar2.png" alt="Avatar" class="avatar">
        </div>
      
        <div class="container">
          <label for="user_email"><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="user_email" required>
            </br>
      
          <label for="password"><b>Password</b></label>
          <input type="text" placeholder="Enter Password" name="password" required>
            </br>
          <button type="submit">Login</button>
        </div>
    </form>
    </body>
    """)