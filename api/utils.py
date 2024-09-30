from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(field):
    return pwd_context.hash(field)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def separator_finder(file_name):
    with open(file_name, 'r') as file:
        # Leer las primeras líneas
        rows = [file.readline() for _ in range(5)]
        
    # Contar la ocurrencia de separadores comunes
    seps = {
        ',': sum(line.count(',') for line in rows),
        ';': sum(line.count(';') for line in rows),
        '\t': sum(line.count('\t') for line in rows),
        '|': sum(line.count('|') for line in rows),
    }

    # Encontrar el separador con más ocurrencias
    separador_detectado = max(seps, key=seps.get)
    
    return separador_detectado


# {
#   "name": "Nicolás",
#   "identification_number": "1234567890",
#   "slug": "nico-at",
#   "video": "",
#   "email": "user@example.com",
#   "gender": "M"
# }