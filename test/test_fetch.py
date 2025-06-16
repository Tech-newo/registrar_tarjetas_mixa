from infrastructure.executables import create_empresas

def test_get_empresas():
    empresas = create_empresas("123", "123", "123", "123", True)
    print(empresas)
    assert True