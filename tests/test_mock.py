import json
import pytest
from app import app
from faker import Faker

@pytest.fixture
def client():
    app.config['TESTING'] = True #Puts the application into testing mode
    with app.test_client() as client: #context manager. +> initialize client ot make requests without running server
        yield client

def test_sum(client, mocker):
    fake = Faker()
    num1 = fake.random_number(digits=3)
    num2 = fake.random_number(digits=3)
    payload = {'num1': num1, 'num2': num2}
    mocker.patch.object(client, 'post', return_value=app.response_class(
        response = json.dumps({'result': num1 + num2}),
        status = 200,
        mimetype='application/json'
    ))

    response = client.post('/sum', payload)
    data = response.get_json()
    assert data['result'] == num1 + num2

if __name__ == '__main__':
    pytest.main([__file__]) #Runs all tests
    
