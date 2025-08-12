from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .Routes import Forgot_password,Auth,Book,User
import os
from .databases import Base,engine


app=FastAPI()

Base.metadata.create_all(engine)
port = int(os.environ.get("PORT","8000"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://libra-connect-app.vercel.app",
                    "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def index():
    return {"message":"Library management system api"}

app.include_router(Forgot_password.forgot_password)
app.include_router(Auth.Auth)
app.include_router(Book.Book)
app.include_router(User.user)

#Starting the app only when the script is run directly
if "__name__"=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=port)