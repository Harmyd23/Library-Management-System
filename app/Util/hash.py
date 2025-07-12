from passlib.context  import CryptContext

password_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

class Hash:
    def Hash_pas(self,password):
        return password_context.hash(password)

    def verify_pas(self,plain_password,hashed_password):
        return password_context.verify(plain_password,hashed_password)
    


