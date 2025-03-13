# Documentação de Arquitetura e Regras de Negócio

## Regras de Negócio

### Taxa de Juros com Base na Idade
A taxa de juros para simulações de empréstimo é determinada com base na idade do solicitante. Solicitantes mais jovens geralmente recebem taxas de juros mais baixas, enquanto solicitantes mais velhos podem receber taxas mais altas. Isso leva em consideração os diferentes perfis de risco associados a cada faixa etária.

### Dependência da Renda
Para garantir que o solicitante possa arcar com o empréstimo, o sistema aplica uma regra onde o valor da parcela mensal não pode ultrapassar 70% da renda mensal do solicitante. Isso ajuda a manter a estabilidade financeira do cliente e reduz o risco de inadimplência.

### Conversão de Moeda
O valor do empréstimo pode ser especificado em diferentes moedas. O sistema converte o valor para BRL (Real Brasileiro) utilizando a taxa de câmbio atual. Para processamento mais rápido, o sistema pode usar taxas de câmbio simuladas ativando a configuração `USE_SIMULATED_CONVERSION=true`.

### Taxas de Juros Fixas e Variáveis
O sistema suporta tanto taxas de juros fixas quanto variáveis:
- **Taxas Fixas**: Permanecem constantes durante todo o prazo do empréstimo.
- **Taxas Variáveis**: Podem mudar de acordo com as condições de mercado.

### Fila de Simulação e Envio de E-mails
Os resultados das simulações de empréstimos são enviados por e-mail ao solicitante. O envio dos e-mails é feito de forma assíncrona para garantir uma melhor experiência de uso. O sistema utiliza SMTP para envio dos e-mails.

### Simulação em Lote
O sistema suporta o processamento em lote de simulações de empréstimos. Diversas solicitações podem ser processadas simultaneamente, e os resultados retornam em lote. Isso é útil para cenários que exigem simulações em massa.

### SMTP para Envio de E-mails
O sistema utiliza SMTP para envio de e-mails. Os detalhes do servidor SMTP são configurados via variáveis de ambiente. O envio é feito de forma assíncrona para não bloquear o fluxo principal da aplicação.

### AWS SQS com LocalStack
O sistema utiliza AWS SQS para enfileiramento de mensagens. O LocalStack é usado para simular o SQS localmente durante o desenvolvimento e testes. Essa configuração pode ser facilmente ajustada para usar o SQS real da AWS modificando as configurações.

### Configurações de Simulação
O sistema permite diversas configurações de simulação para melhorar desempenho e flexibilidade. Estas configurações são feitas via variáveis de ambiente:
- `USE_SIMULATED_RATE=true`
- `SIMULATED_INTEREST_RATE=0.015`
- `USE_SIMULATED_CONVERSION=true`

Essas configurações permitem o uso de taxas de juros e câmbio simuladas, reduzindo a necessidade de chamadas a APIs externas.

### Agendador para Atualizar Taxas de Câmbio
Um agendador é utilizado para atualizar periodicamente as taxas de câmbio. Isso garante que o sistema utilize sempre os valores mais recentes. A biblioteca `apscheduler` é utilizada para configurar esse agendamento automático.

#### Exemplo de código com lógica real:
```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests

EXTERNAL_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

conversion_rates = {}

def fetch_currency_conversion_rates():
    try:
        response = requests.get(EXTERNAL_API_URL)
        if response.status_code == 200:
            data = response.json()
            conversion_rates.update(data.get("rates", {}))
            print(f"Taxas de câmbio atualizadas: {conversion_rates}")
        else:
            print(f"Erro ao buscar taxas: {response.status_code}")
    except Exception as e:
        print(f"Falha ao atualizar taxas de câmbio: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_currency_conversion_rates, 'interval', minutes=360)
scheduler.start()
```

## Arquitetura e Padrões de Projeto

### FastAPI
FastAPI foi escolhido pela sua alta performance e facilidade de uso. É um framework moderno para construção de APIs com Python 3.12+, baseado em type hints nativos.

### Poetry
Poetry é utilizado para gerenciamento de dependências, garantindo ambientes consistentes. Ele simplifica o gerenciamento de pacotes e empacotamento da aplicação.

### Docker & Docker Compose
Docker e Docker Compose são usados para containerização e configuração do ambiente de desenvolvimento. Isso facilita a implantação e execução da aplicação em qualquer ambiente.

### LocalStack
LocalStack é utilizado para simular os serviços da AWS localmente, como SQS, durante o desenvolvimento e testes, sem custos adicionais.

### Programação Assíncrona
A aplicação utiliza programação assíncrona para lidar com operações I/O-bound de forma eficiente. Isso melhora a performance permitindo múltiplas tarefas rodando simultaneamente.

### Padrão de Projeto Factory
O padrão Factory (Fábrica) é utilizado para criação das classes de simulação. Isso garante um código limpo e de fácil manutenção, encapsulando a lógica de construção de objetos complexos.

## Decisões Técnicas

### Envio de E-mails
Os e-mails são enviados de forma assíncrona para não impactar a experiência do usuário. A lógica de envio está encapsulada na classe `EmailService`.

### Integração com SQS
A AWS SQS é usada para enfileiramento de mensagens. A classe `SQSService` encapsula toda a lógica de interação com a fila. O uso do LocalStack permite testar localmente, e a configuração pode ser facilmente alterada para usar o ambiente da AWS real.

### Configurações de Simulação
O sistema suporta diversas configurações via variáveis de ambiente, permitindo ajustes rápidos sem necessidade de alterar o código.

---

Para mais detalhes, consulte [README.md](../README.md).