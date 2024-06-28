from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QMessageBox
)
import sys

class CashFlowCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rental Property Cash Flow Calculator')

        grid = QGridLayout()

        fields = [
            ("Purchase Price (Pula)", "purchase_price"),
            ("Annual Interest Rate (%)", "interest_rate"),
            ("Loan Term (Years)", "loan_term"),
            ("Monthly Rental Income (Pula)", "rental_income"),
            ("Property Management Fee (Pula)", "property_management"),
            ("Maintenance and Repairs (Pula)", "maintenance_repairs"),
            ("Property Taxes (Pula)", "property_taxes"),
            ("Insurance (Pula)", "insurance"),
            ("Utilities (Pula)", "utilities"),
        ]

        self.inputs = {}
        for idx, (label_text, field_name) in enumerate(fields):
            label = QLabel(label_text)
            entry = QLineEdit()
            grid.addWidget(label, idx, 0)
            grid.addWidget(entry, idx, 1)
            self.inputs[field_name] = entry

        self.result_label = QLabel("")
        self.one_percent_rule_label = QLabel("")
        calculate_button = QPushButton('Calculate Cash Flow', self)
        calculate_button.clicked.connect(self.calculate_cash_flow)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(calculate_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.one_percent_rule_label)

        self.setLayout(vbox)

    def calculate_cash_flow(self):
        try:
            purchase_price = float(self.inputs["purchase_price"].text())
            annual_interest_rate = float(self.inputs["interest_rate"].text()) / 100
            loan_term_years = int(self.inputs["loan_term"].text())
            monthly_rental_income = float(self.inputs["rental_income"].text())
            property_management_fee = float(self.inputs["property_management"].text())
            maintenance_repairs = float(self.inputs["maintenance_repairs"].text())
            property_taxes = float(self.inputs["property_taxes"].text())
            insurance = float(self.inputs["insurance"].text())
            utilities = float(self.inputs["utilities"].text())

            loan_principal = purchase_price
            monthly_interest_rate = annual_interest_rate / 12
            number_of_payments = loan_term_years * 12

            monthly_mortgage_payment = (loan_principal * monthly_interest_rate * (1 + monthly_interest_rate)**number_of_payments) / \
                                       ((1 + monthly_interest_rate)**number_of_payments - 1)

            total_monthly_expenses = monthly_mortgage_payment + property_management_fee + maintenance_repairs + \
                                     property_taxes + insurance + utilities

            monthly_cash_flow = monthly_rental_income - total_monthly_expenses

            self.result_label.setText(
                f"Monthly Mortgage Payment: P{monthly_mortgage_payment:.2f}\n"
                f"Total Monthly Expenses: P{total_monthly_expenses:.2f}\n"
                f"Monthly Cash Flow: P{monthly_cash_flow:.2f}"
            )

            # Check if the property meets the 1% rule
            one_percent_rule = purchase_price * 0.01
            if monthly_rental_income >= one_percent_rule:
                self.one_percent_rule_label.setText(
                    f"The property meets the 1% rule.\n1% of Purchase Price: P{one_percent_rule:.2f}\n"
                    f"Monthly Rental Income: P{monthly_rental_income:.2f}"
                )
            else:
                self.one_percent_rule_label.setText(
                    f"The property does not meet the 1% rule.\n1% of Purchase Price: P{one_percent_rule:.2f}\n"
                    f"Monthly Rental Income: P{monthly_rental_income:.2f}"
                )
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values for all fields.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CashFlowCalculator()
    calc.show()
    sys.exit(app.exec_())
