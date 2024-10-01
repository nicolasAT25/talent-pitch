from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(field):
    return pwd_context.hash(str(field))

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def separator_finder(file_name):
    with open(file_name, 'r') as file:
        rows = [file.readline() for _ in range(5)]
        
    seps = {
        ',': sum(line.count(',') for line in rows),
        ';': sum(line.count(';') for line in rows),
        '\t': sum(line.count('\t') for line in rows),
        '|': sum(line.count('|') for line in rows),
    }

    separador_detectado = max(seps, key=seps.get)
    
    return separador_detectado