from unittest.mock import patch

import pytest
from main.services.farm_service import get_farm
from tests.fixtures import *


def test_get_farm_success():
    with patch('main.models.farm_model.farm_model.FarmModel.query') as mock_query:
        mock_query.filter_by.return_value.all.return_value = [
            FarmModel(id=1, name='Farm 1', user_id=1),
            FarmModel(id=2, name='Farm 2', user_id=1)
        ]
    result, status_code = get_farm(1)

    assert status_code == 200
    assert 'data' in result
    assert len(result['data']) > 0
    assert result['data'][0]['id']
    assert result['data'][0]['name']


def test_get_farm_no_farms_found():
    result, status_code = get_farm(9000)

    assert status_code == 404
    assert 'error' in result
    assert result['error'] == 'No Farm found'
