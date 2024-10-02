import pytest
from api import schemas
# from .conftest import client, session

# client = TestClient(main.app)

@pytest.mark.parametrize("name,identification_number,slug,video,email,gender",
                         [("Felipe Pérez","0987","felipe-p","https://www.youtube.com/watch?v=vylxZVKpung","feli@test.com","M"),
                         ("Laura Sánchez","6789","fLau-s","","lau@test.com","F")])
def test_create_user(client, name, identification_number, slug, video, email, gender):
    res = client.post("/users/", json={"name":name,"identification_number":identification_number,"slug":slug,"video":video,
                                      "email":email,"gender":gender})
    
    new_user = schemas.User(**res.json())
    assert new_user.email == email
    assert new_user.name == name
    assert res.status_code == 201