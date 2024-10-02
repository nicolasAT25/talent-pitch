import pytest
from api import schemas
# from .conftest import client, session

# client = TestClient(main.app)

@pytest.mark.parametrize("name,description,status,opencall_objective",
                         [("Cantantes de Reguetonland que buscan patrocinios",
                           "Buscamos jóvenes comprometidos con la justicia social, el cambio climático y los derechos humanos, listos para desafiar el sistema. Ofrecemos oportunidades de conexión con entidades políticas progresistas, ONGs y celebridades comprometidas con el cambio social.",
                           "published","Artistas")])
def test_create_post(client, name, description, status, opencall_objective):
    res = client.post("/challenges/", json={"name":name,"description":description,"status":status,"opencall_objective":opencall_objective})
    
    new_challenge = schemas.Challenge(**res.json())
    assert new_challenge.name == name
    assert new_challenge.status == status
    assert res.status_code == 201