from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a 6 round public goods game with 5 players.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 5
    num_rounds = 6

    instructions_template = 'public_goods/Instructions.html'

    # """Amount allocated to each player"""
    endowment = c(10)
    efficiency_factor = 3


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution is not None]
        return {
            'avg_contribution': sum(contributions)/len(contributions),
            'min_contribution': min(contributions),
            'max_contribution': max(contributions),
        }


class Group(BaseGroup):
    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share



class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
