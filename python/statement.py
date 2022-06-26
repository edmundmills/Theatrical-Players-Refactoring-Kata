import math

def format_as_dollars(amount):
    return f"${amount:0,.2f}"


class Performance:
    def __init__(self, name, n_audience) -> None:
        self.n_audience = n_audience
        self.name = name

    @property
    def price(self):
        raise NotImplementedError
    
    @staticmethod
    def create(play_type, **play_kwargs):
        play_classes = {
            'comedy': ComedyPerformance,
            'tragedy': TragedyPerformance
        }
        play_class = play_classes.get(play_type, None)
        if play_class is None:
            raise ValueError(f'unknown type: {play_type}')
        return play_class(**play_kwargs)

    @property
    def volume_credits(self):
        return max(self.n_audience - 30, 0)


class ComedyPerformance(Performance):
    @property
    def price(self):
        p = 30000 + 300 * self.n_audience
        if self.n_audience > 20:
            p += 10000
            p += 500 * (self.n_audience - 20)
        return p

    @property
    def volume_credits(self):
        base = super().volume_credits
        return base + math.floor(self.n_audience / 5)


class TragedyPerformance(Performance):
    @property
    def price(self):
        p = 40000
        if self.n_audience > 30:
            p += 1000 * (self.n_audience - 30)
        return p


class Statement:
    def __init__(
        self,
        customer_name,
        performances    
    ) -> None:
        self.customer_name = customer_name
        self.performances = performances
    
    @property
    def price(self):
        return sum(p.price for p in self.performances)

    @property
    def volume_credits(self):
        return sum(p.volume_credits for p in self.performances)
    
    @property
    def text(self):
        statement_text = f'Statement for {self.customer_name}\n'
        for performance in self.performances:
            statement_text += f' {performance.name}: {format_as_dollars(performance.price/100)} ({performance.n_audience} seats)\n'
        statement_text += f'Amount owed is {format_as_dollars(self.price/100)}\n'
        statement_text += f'You earned {self.volume_credits} credits\n'
        return statement_text


def statement(invoice, plays):
    collated_plays = (plays[perf['playID']] for perf in invoice['performances'])
    performances = [Performance.create(
                        play['type'],
                        name=play['name'],
                        n_audience=perf['audience'])
                    for play, perf in zip(collated_plays, invoice['performances'])]
    s = Statement(
        customer_name=invoice["customer"],
        performances=performances
    )
    return s.text

