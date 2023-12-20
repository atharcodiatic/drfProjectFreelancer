def currency_converter(job_currency,bid,freelancer_currency):
            amount = None
            payment_currency = None
            if job_currency == freelancer_currency:
                amount = bid
                payment_currency = job_currency
            elif job_currency != freelancer_currency:
                if job_currency == "USD":
                    amount = bid / 83 
                    payment_currency = job_currency
                elif job_currency == "RS":
                    amount = bid * 83 
                    payment_currency = job_currency
            return [amount,payment_currency]

def calculate_total(duration, duration_type, amount):
            # working_hours = 8 
            one_week = 7
            one_month = 30
            total_amount = None 
            if duration_type == "DAY":
                total_amount =  duration * amount
            elif duration_type == 'WEEK':
                total_amount = duration  * amount
            elif duration_type == 'MONTH':
                total_amount = duration * amount
            return total_amount