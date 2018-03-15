from enum import Enum


class OutputThresholds(Enum):
    # Basic Defense
    LIFE_FLAT = 1000
    LIFE_PERCENT = 50
    LIFE_PERCENT_PER_LEVEL = 1.5
    LIFE_REGEN = 100

    ES_FLAT = 300
    ES_PERCENT = 50
    ES_PERCENT_PER_LEVEL = 1.5
    ES_REGEN = 100

    #Show ele res bigger than the 75 cap
    ELE_RES = 76
    #Show all positive chaos res
    CHAOS_RES = 0

    # The amount below specifies the ratio of life to ev/ar: 100 life <> 80+ AR/EV is displayed
    AR_EV_THRESHOLD_PERCENTAGE = 0.8
    ARMOUR = 5000
    EVASION = 5000

    # most shields have 25-30 base, so +10 should be easily doable, spellblock is lower
    BLOCK = 40
    SPELL_BLOCK = 20
    # 30 = Acro/Phase Acro, half of that is displayable
    DODGE = 15
    SPELL_DODGE = 15

    #Offense
    ACCURACY = 99
    CRIT_CHANCE = 5