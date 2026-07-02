def calculate_compound_growth(principal: float, monthly_contribution: float,
                              annual_rate: float, years: int) -> dict:
    """Projects investment growth over time with monthly contributions and compounding.

    Args:
        principal: Starting amount invested, in dollars.
        monthly_contribution: Amount added every month, in dollars.
        annual_rate: Annual return rate as a decimal, e.g. 0.07 for 7%. Must be
            between 0 and 1, never a whole number like 7.
        years: Number of years to project.
    """
    months = years * 12
    monthly_rate = annual_rate / 12
    balance = principal
    history = []
    for m in range(1, months + 1):
        balance = balance * (1 + monthly_rate) + monthly_contribution
        if m % 12 == 0:
            history.append({"year": m // 12, "balance": round(balance, 2)})
    return {"final_balance": round(balance, 2), "yearly_breakdown": history}


def calculate_debt_payoff(balance: float, apr: float, monthly_payment: float) -> dict:
    """Calculates how long it takes to pay off a debt and total interest paid.

    Args:
        balance: Current debt balance, in dollars.
        apr: Annual percentage rate as a decimal, e.g. 0.19 for 19%. Must be
            between 0 and 1, never a whole number like 19.
        monthly_payment: Fixed amount paid toward the debt each month, in dollars.
    """
    monthly_rate = apr / 12
    months = 0
    total_interest = 0
    while balance > 0 and months < 600:
        interest = balance * monthly_rate
        principal_paid = monthly_payment - interest
        if principal_paid <= 0:
            return {"error": "Payment too low to ever pay off this debt"}
        balance -= principal_paid
        total_interest += interest
        months += 1
    return {"months_to_payoff": months, "total_interest_paid": round(total_interest, 2)}


def calculate_savings_rate(income: float, expenses: float) -> dict:
    """Calculates monthly savings amount and savings rate as a percentage.

    Args:
        income: Monthly income, in dollars.
        expenses: Total monthly expenses, in dollars.
    """
    saved = income - expenses
    rate = (saved / income) * 100 if income > 0 else 0
    return {"monthly_savings": round(saved, 2), "savings_rate_pct": round(rate, 1)}
def calculate_required_payment(balance: float, apr: float, months: int) -> dict:
    """Calculates the fixed monthly payment needed to fully pay off a debt within
    a specific number of months, using standard loan amortization.

    Args:
        balance: Current debt balance, in dollars or rupees.
        apr: Annual percentage rate as a decimal, e.g. 0.36 for 36%. Must be
            between 0 and 1, never a whole number like 36.
        months: The exact number of months to pay it off within.
    """
    monthly_rate = apr / 12
    if monthly_rate == 0:
        payment = balance / months
    else:
        payment = balance * (monthly_rate * (1 + monthly_rate) ** months) / \
                  ((1 + monthly_rate) ** months - 1)

    total_paid = payment * months
    total_interest = total_paid - balance

    return {
        "monthly_payment": round(payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_interest, 2)
    }