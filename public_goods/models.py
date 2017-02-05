from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a one-period public goods game with 3 players.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 3
    num_rounds = 2

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

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    is_Punished = models.BooleanField(default=False)

class Group(BaseGroup):
    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()
    max_contributor = None
    max_contribution = models.CurrencyField()
    numbers = models.IntegerField(
        widget=widgets.RadioSelect()
    )

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share

    #def find_min_max(self):
        self.max_contributor = max(self.get_players(), key=lambda p: p.contribution)
        #print("max found is", max(self.get_players(), key=lambda p: p.contribution))
        #print(self.max_contributor.contribution,self.max_contributor.participant)
        self.max_contribution = self.max_contributor.contribution




    def group_fields(self):
        self.max_contributor = max(self.get_players(), key=lambda p: p.contribution)
        self.lowest_contributor = self.max_contributor.get_others_in_group()
        list3 = []
        for p in self.lowest_contributor:
            list3.append(p.id_in_group)
        print("group fields", list3)
        return list3
