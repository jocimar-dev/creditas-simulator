from datetime import datetime, timedelta

def generate_email_body(customer_name: str, response_json: str) -> str:
    validade = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
    email_body = f"""
    <html>
        <body>
            <h2>Olá {customer_name},</h2>
            <p>Segue abaixo a sua simulação de empréstimo:</p>
            <pre>{response_json}</pre>
            <p>Validade: {validade}</p>
            <p><a href="http://example.com">Clique aqui para prosseguir</a></p>
            <p>Atenciosamente,<br>Sua Empresa</p>
        </body>
    </html>
    """
    return email_body