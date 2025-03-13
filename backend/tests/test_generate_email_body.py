from backend.app.service.util.generate_email_body import generate_email_body

def test_generate_email_body():
    customer_name = "John"
    response_json = '{"loan_amount": 10000, "interest_rate": 0.05}'
    email_body = generate_email_body(customer_name, response_json)

    assert "Olá John" in email_body
    assert "loan_amount" in email_body
    assert "interest_rate" in email_body
    assert "Clique aqui para prosseguir" in email_body