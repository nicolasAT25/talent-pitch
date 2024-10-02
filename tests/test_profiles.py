import pytest
from api import schemas
# from .conftest import client, session

# client = TestClient(main.app)

@pytest.mark.parametrize("user_id,onboarding_goal,views",
                         [(200,"be_discovered-[hire]",30),
                         (100,"be_discovered-[hire]",54)])
def test_create_post(client, user_id, onboarding_goal,views):
    res = client.post("/profiles/", json={"user_id":user_id,"onboarding_goal":onboarding_goal,"views":views})
    
    new_profile = schemas.Profile(**res.json())
    assert new_profile.user_id == user_id
    assert new_profile.onboarding_goal == onboarding_goal
    assert res.status_code == 201