
from fastapi_skeleton.core import config

import requests
url = "http://127.0.0.1:8000/upload_file"
files = {'image': open('31_left.jpeg', 'rb')}
response = requests.post(url, files=files)
print(response.text)

# def test_prediction(test_client) -> None:
#     response = test_client.post(
#         "/api/model/predict", 
#         # API_PREFIX = "/api" in core/config.py, and
#         # api_router.include_router(prediction.router, tags=["prediction"], prefix="/model") in api/routes/router.py, and
#         # @router.post("/predict"...) in api/routes/prediction.py
#         json={
#             "median_income_in_block": 8.3252,
#             "median_house_age_in_block": 41,
#             "average_rooms": 6,
#             "average_bedrooms": 1,
#             "population_per_block": 322,
#             "average_house_occupancy": 2.55,
#             "block_latitude": 37.88,
#             "block_longitude": -122.23
#         },
#         headers={"token": str(config.API_KEY)}
#     )
#     assert response.status_code == 200
#     assert "median_house_value" in response.json()
#     assert "currency" in response.json()


def test_prediction_nopayload(test_client) -> None:
    response = test_client.post(
        "/api/model/predict",
        json={},
        headers={"token": str(config.API_KEY)}
    )
    assert response.status_code == 422
