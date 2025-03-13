# Business Rules, Architecture, and Technical Decisions

## Business Rules

### Interest Rate Based on Age
The interest rate for loan simulations is determined based on the applicant's age. Younger applicants typically receive lower interest rates, while older applicants may receive higher rates. This is to account for the varying risk profiles associated with different age groups.

### Income Dependency
To ensure that applicants can afford the loan, the system enforces a rule where the monthly payment must not exceed 70% of the applicant's monthly income. This helps in maintaining financial stability for the applicant and reduces the risk of default.

### Currency Conversion
The loan amount can be specified in different currencies. The system converts the loan amount to BRL (Brazilian Real) using the current exchange rate. For faster processing, the system can use simulated conversion rates by setting the `USE_SIMULATED_CONVERSION` configuration to `true`.

### Fixed and Variable Interest Rates
The system supports both fixed and variable interest rates:
- **Fixed Rates**: These remain constant throughout the loan term.
- **Variable Rates**: These may change based on market conditions.

### Simulation Queue and Email Sending
Loan simulation results are sent to the applicant via email. The email sending process is handled asynchronously to ensure a smooth user experience. The system uses SMTP for sending emails.

### Batch Simulation
The system supports batch processing of loan simulations. Multiple loan simulation requests can be processed simultaneously, and the results are returned as a batch. This is useful for scenarios where bulk simulations are required.

### SMTP for Email Sending
The system uses SMTP to send emails. The SMTP server details are configured using environment variables. The email sending process is handled asynchronously to avoid blocking the main application flow.

### AWS SQS with LocalStack
The system uses AWS SQS for message queuing. LocalStack is used to emulate AWS SQS locally for development and testing. This setup can be easily adapted to use real AWS SQS by updating the configuration.

### Simulation Configurations
The system supports various simulation configurations to improve performance and flexibility. These configurations can be set using environment variables:

- `USE_SIMULATED_RATE=true`
- `SIMULATED_INTEREST_RATE=0.015`
- `USE_SIMULATED_CONVERSION=true`

These configurations allow the system to use simulated interest rates and currency conversion rates, reducing the need for external API calls.

### Scheduler for Currency Conversion Updates
In a real-world scenario, a scheduler would be used to periodically update currency conversion rates. This ensures that the system always uses the latest exchange rates. The following code snippet demonstrates how to set up a scheduler using `apscheduler`:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def fetch_currency_conversion_rates():
    # Logic to fetch and update currency conversion rates
    print(f"Fetching currency conversion rates at {datetime.now()}")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_currency_conversion_rates, 'interval', minutes=360)
scheduler.start()
```

This can be adapted to fetch and update currency conversion rates in the application.

---

## Architecture and Design Patterns

### FastAPI
FastAPI was chosen for its high performance and ease of use. It provides a modern web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Poetry
Poetry is used for dependency management to ensure consistent environments. It simplifies the process of managing dependencies and packaging the application.

### Docker & Docker Compose
Docker and Docker Compose are used for containerization and easy setup of development environments. This ensures that the application can be easily deployed and run in any environment.

### LocalStack
LocalStack is used to emulate AWS services locally for development and testing. This allows developers to test their code against a local instance of AWS services without incurring costs.

### Asynchronous Programming
Asynchronous programming is used to handle I/O-bound operations efficiently. This improves the performance of the application by allowing multiple operations to run concurrently.

### Factory Design Pattern
The Factory Design Pattern is used to create simulation classes. This ensures a clean and maintainable codebase by encapsulating the creation logic of complex objects.

---

## Technical Decisions

### Email Sending
Emails are sent asynchronously to ensure that the user experience is not impacted by the time taken to send an email. The email sending logic is encapsulated in the `EmailService` class.

### SQS Integration
AWS SQS is used for message queuing. The `SQSService` class encapsulates the logic for interacting with SQS. LocalStack is used to emulate SQS locally, and the configuration can be easily switched to use real AWS SQS.

### Simulation Configurations
The system supports various configurations to improve performance and flexibility. These configurations can be set using environment variables, allowing for easy customization without changing the code.

---

For more details, refer to the [README.md](../README.md).