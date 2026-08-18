import plaid

def test_environment_urls():
    assert plaid.Environment.Production == "https://production.plaid.com"
    assert plaid.Environment.Development == "https://development.plaid.com"
    assert plaid.Environment.Sandbox == "https://sandbox.plaid.com"

def test_configuration_with_development_host():
    configuration = plaid.Configuration(host=plaid.Environment.Development)
    assert configuration.host == "https://development.plaid.com"

def test_get_host_settings():
    configuration = plaid.Configuration()
    host_settings = configuration.get_host_settings()
    assert len(host_settings) == 3
    
    assert host_settings[0]['url'] == "https://production.plaid.com"
    assert host_settings[0]['description'] == "Production"
    
    assert host_settings[1]['url'] == "https://development.plaid.com"
    assert host_settings[1]['description'] == "Development"
    
    assert host_settings[2]['url'] == "https://sandbox.plaid.com"
    assert host_settings[2]['description'] == "Sandbox"
