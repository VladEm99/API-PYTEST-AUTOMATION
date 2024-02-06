from faker import Faker
from faker.providers import internet
import requests
import random

'''
Я закомментировал assert на проверку status code почти в каждом тесте, так как абсолютно все методы API 
по факту возвращают 200 код, поэтому тесты не проходят. 
Я не мог определиться правильно ли было бы оставить эти проверки или нет, поэтому оставил их в
виде комментариев. 
Надеюсь на понимание! :)'''

ENDPOINT = " https://automationexercise.com/api"

# Function to generate user data.
def generate_user_data(num_of_users):
   # Create a Faker instance.
   fake = Faker()
   fake.add_provider(internet)
   user_data = []

   for _ in range(num_of_users):
       # Create a dictionary representing a user with various attributes.
       user = {
            "name": fake.name(), 
            "email": fake.free_email(), 
            "password": fake.password(), 
            "title": "Mr", 
            "birth_date": random.randint(1,31), 
            "birth_month": random.randint(1,12), 
            "birth_year": random.randint(1920,2024), 
            "firstname": fake.name(), 
            "lastname": fake.name(), 
            "company": fake.company(), 
            "address1": fake.address(), 
            "address2": fake.address(), 
            "country": fake.country(), 
            "zipcode": fake.zipcode(), 
            "state": fake.name(), 
            "city": fake.city(), 
            "mobile_number": fake.phone_number()
       }
       # Append the user data dictionary to the user_data list.
       user_data.append(user)
   # Return generated user data.
   return user_data[0]

#API 1: Get all products list
def test_can_get_productList():
    get_productList_response = requests.get(ENDPOINT + "/productsList")
    assert get_productList_response.status_code == 200

#API 2: POST to all products List
def test_can_not_get_productList():
    post_productList_response = requests.post(ENDPOINT + "/productsList")
    assert '{"responseCode": 405, "message": "This request method is not supported."}' in post_productList_response.text
    #assert post_productList_response.status_code == 405

#API 3: Get all brands list
def test_can_get_brandList():
    get_brandList_response = requests.get(ENDPOINT + "/brandsList")
    assert get_brandList_response.status_code == 200

#API 4: PUT to all brands list
def test_can_not_get_brandList():
    put_productList_response = requests.put(ENDPOINT + "/productsList")
    assert '{"responseCode": 405, "message": "This request method is not supported."}' in put_productList_response.text
    #assert put_productList_response.status_code == 405

#API 5: POST to search product
def test_can_search_product():
    data = {"search_product": "tshirt"}
    post_search_product_response = requests.post(ENDPOINT + "/searchProduct", data=data)
    assert post_search_product_response.status_code == 200

#API 6: POST to search product without search_product parametr
def test_can_not_search_product():
    post_search_product_response = requests.post(ENDPOINT + "/searchProduct")
    assert '{"responseCode": 400, "message": "Bad request, search_product parameter is missing in POST request."}' in post_search_product_response.text
    #assert post_search_product_response.status_code == 400

#API 11: POST to create/register user account
def test_can_create_user():
    data = generate_user_data(1)
    post_create_user_response = requests.post(ENDPOINT + "/createAccount", data=data)
    assert '{"responseCode": 201, "message": "User created!"}' in post_create_user_response.text
    #assert post_create_user_response.status_code == 201

#API 7: POST to verify login with valid details
def test_can_verify_login():
    data = generate_user_data(1)
    login_data = {
        "email": data["email"],
        "password": data["password"]
    }
    #Creating new account with random generated data
    requests.post(ENDPOINT + "/createAccount", data=data)
    post_to_verify_login_response = requests.post(ENDPOINT + "/verifyLogin", data=login_data)
    assert '{"responseCode": 200, "message": "User exists!"}' in post_to_verify_login_response.text
    assert post_to_verify_login_response.status_code == 200

#API 8: POST to verify login without email parametr
def test_can_not_verify():
    data = {"password": "123"}
    post_to_verify_response = requests.post(ENDPOINT + "/verifyLogin", data=data)
    assert '{"responseCode": 400, "message": "Bad request, email or password parameter is missing in POST request."}' in post_to_verify_response.text
    #assert post_to_verify_response.status_code == 400

#API 9: DELETE to verify login
def test_delete_to_verify_login():
    delete_to_verify_login_response = requests.delete(ENDPOINT + "/verifyLogin")
    assert '{"responseCode": 405, "message": "This request method is not supported."}' in delete_to_verify_login_response.text
    #assert delete_to_verify_login_response.status_code == 405
    
#API 10: POST to verify login with invlaid details
def test_post_to_verify_with_ivalid_details():
    data = generate_user_data(1)
    invalid_data = {
        "email": data["email"],
        "password": data["password"]
    }
    post_to_verify_with_ivalid_details_response = requests.post(ENDPOINT + "/verifyLogin", data=invalid_data)
    assert '{"responseCode": 404, "message": "User not found!"}' in post_to_verify_with_ivalid_details_response.text
    #assert post_to_verify_with_ivalid_details_response.status_code == 404

#API 13: PUT to update user account
def test_can_update_account():
    data = generate_user_data(1)
    data_for_update = {
            "name": data["name"], 
            "email": data["email"], 
            "password": data["password"], 
            "title": "Mr", 
            "birth_date": 5, 
            "birth_month": 10, 
            "birth_year": 1999, 
            "firstname": "Vlad", 
            "lastname": "VL", 
            "company": "test", 
            "address1": "test", 
            "address2": "test", 
            "country": "test", 
            "zipcode": 1555, 
            "state": "test", 
            "city": "test", 
            "mobile_number": 777777
    }
    #request for creating new user with random data
    requests.post(ENDPOINT + "/createAccount", data=data)
    #request for updating created user
    put_update_user_response = requests.put(ENDPOINT + "/updateAccount", data=data_for_update)
    assert '{"responseCode": 200, "message": "User updated!"}' in put_update_user_response.text
    #assert put_update_user_response.status_code == 200

#API 14: GET user account detail by email
def test_can_get_user_info_by_email():
    data = generate_user_data(1)
    email_data = {"email": data["email"]}
    #request for creating new user with random data
    requests.post(ENDPOINT + "/createAccount", data=data)
    #request for getting user data by email
    get_user_info_by_email_response = requests.get(ENDPOINT + "/getUserDetailByEmail", data=data) 
    assert get_user_info_by_email_response.status_code == 200

#API 12: DELETE to delete user account
def test_can_delete_account():
    data = generate_user_data(1)
    data_to_delete = {
        "email": data["email"],
        "password": data["password"]
    }
    #request for creating new user
    requests.post(ENDPOINT + "/createAccount", data=data)
    #request for deleting user using email and password
    delete_user_account_response = requests.delete(ENDPOINT + "/deleteAccount", data=data_to_delete)
    assert '{"responseCode": 200, "message": "Account deleted!"}' in delete_user_account_response.text
    assert delete_user_account_response.status_code == 200