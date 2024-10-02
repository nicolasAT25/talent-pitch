import pytest
from api import schemas
# from .conftest import client, session

# client = TestClient(main.app)

@pytest.mark.parametrize("user_id,name,type,video,views",
                         [(700,"mi primer video","pitch_video",
                           "https://media.talentpitch.co/resumes/1/akjdaksdha212312k3hka.mp4",
                           44)])
def test_create_post(client, user_id, name, type, video, views):
    res = client.post("/resumes/", json={"user_id":user_id,"name":name,"type":type,"video":video,"views":views})
    
    new_resume = schemas.Resume(**res.json())
    assert new_resume.user_id == user_id
    assert new_resume.type == type
    assert res.status_code == 201