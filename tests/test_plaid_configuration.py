import pytest
import plaid

def test_plaid_configuration_case_insensitive_dict():
    # Test case-insensitivity and underscores in dictionary keys
    config = plaid.Configuration(
        api_key={
            'client_id': 'test-client-id',
            'SECRET': 'test-secret',
            'plaid_version': '2020-09-14'
        }
    )
    
    assert config.api_key['clientId'] == 'test-client-id'
    assert config.api_key['client_id'] == 'test-client-id'
    assert config.api_key['secret'] == 'test-secret'
    assert config.api_key['plaidVersion'] == '2020-09-14'
    assert config.api_key['plaid_version'] == '2020-09-14'

    # Test get_api_key_with_prefix
    assert config.get_api_key_with_prefix('clientId') == 'test-client-id'
    assert config.get_api_key_with_prefix('client_id') == 'test-client-id'
    assert config.get_api_key_with_prefix('secret') == 'test-secret'
    assert config.get_api_key_with_prefix('plaidVersion') == '2020-09-14'
    assert config.get_api_key_with_prefix('plaid_version') == '2020-09-14'

    # Test auth_settings
    settings = config.auth_settings()
    assert settings['clientId']['value'] == 'test-client-id'
    assert settings['secret']['value'] == 'test-secret'
    assert settings['plaidVersion']['value'] == '2020-09-14'

def test_plaid_configuration_constructor_kwargs():
    # Test keyword arguments in constructor
    config = plaid.Configuration(
        client_id='test-client-id-kwargs',
        secret='test-secret-kwargs',
        plaid_version='2020-09-14-kwargs',
        environment='sandbox'
    )

    assert config.api_key['clientId'] == 'test-client-id-kwargs'
    assert config.api_key['client_id'] == 'test-client-id-kwargs'
    assert config.api_key['secret'] == 'test-secret-kwargs'
    assert config.api_key['plaidVersion'] == '2020-09-14-kwargs'
    assert config.api_key['plaid_version'] == '2020-09-14-kwargs'
    assert config.host == 'https://sandbox.plaid.com'

    # Test environment production
    config_prod = plaid.Configuration(environment='production')
    assert config_prod.host == 'https://production.plaid.com'

def test_plaid_configuration_direct_property_assign():
    config = plaid.Configuration()
    config.api_key = {
        'client_id': 'prop-client-id',
        'secret': 'prop-secret',
    }
    assert config.api_key['clientId'] == 'prop-client-id'
    assert config.api_key['client_id'] == 'prop-client-id'
    assert config.api_key['secret'] == 'prop-secret'

    # In-place modify dict directly (getter modification)
    config.api_key['client_id'] = 'modified-client-id'
    assert config.get_api_key_with_prefix('clientId') == 'modified-client-id'
    assert config.get_api_key_with_prefix('client_id') == 'modified-client-id'

def test_plaid_configuration_arbitrary_keys():
    config = plaid.Configuration()
    config.api_key['custom_auth_key'] = 'some-token'
    assert config.api_key['custom_auth_key'] == 'some-token'
    assert config.api_key['CUSTOM_AUTH_KEY'] == 'some-token'
    assert config.api_key['customauthkey'] == 'some-token'
    assert config.api_key['custom-auth-key'] == 'some-token'

    # Test update and setdefault and copy
    config.api_key.update({'another_key': 'val'})
    assert config.api_key['anotherkey'] == 'val'

    config.api_key.setdefault('yet_another_key', 'val2')
    assert config.api_key['yetanotherkey'] == 'val2'

    copied = config.api_key.copy()
    assert copied['anotherkey'] == 'val'
    assert isinstance(copied, plaid.configuration.CaseInsensitiveDict)

