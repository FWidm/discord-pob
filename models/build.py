import re

from models.gem import Gem
from util.logging import log
from util.pob import pob_conf


class Build:
    def __init__(self, level, version, bandit, class_name, ascendency_name, tree, skills, activeSkill, item_slots):
        self.level = int(level)
        self.version = version
        self.bandit = bandit
        self.class_name = class_name
        self.ascendency_name = ascendency_name
        self.stats = {}
        self.config = {}
        self.tree = tree
        self.skills = skills
        self.active_skill_id = int(activeSkill)
        self.item_slots = item_slots

    def append_stat(self, key, val, stat_owner):
        # remove "Stat" from the string
        stat_owner = stat_owner[:-4]
        if not stat_owner in self.stats:
            self.stats[stat_owner] = {}
        self.stats[stat_owner][key] = float(val)
        # print("owner_key={}; key={}, val={}".format(stat_owner, key, val))

    def append_conf(self, key, val):
        conf_enry = pob_conf.fetch_entry(key)
        # ignore unknown settings.
        if conf_enry:
            self.config[key] = {'value': val}
            self.config[key].update(conf_enry)

    def __repr__(self) -> str:
        return "{}".format(self.__dict__)

    def get_item(self, slot):
        if slot:
            return self.item_slots[slot].item

    def get_stat(self, owner, key, threshold=0):
        if owner in self.stats and key in self.stats[owner]:
            val = self.stats[owner][key]
            return val if val >= threshold else None
        else:
            return None

    def to_string(self):
        ret = ""
        for item in self.__dict__:
            val = self.__dict__[item]
            if isinstance(val, list):
                pass
            else:
                ret += item + ": " + val + "\n"
        return ret

    def get_active_skill(self):
        if len(self.skills) < 1 or self.active_skill_id < 1:
            return None
        return self.skills[self.active_skill_id - 1]

    def get_active_gem_name(self):
        gem_name = "Undefined"
        main_gem = self.get_active_skill().get_selected()
        if isinstance(main_gem, Gem):
            gem_name = main_gem.name
        return gem_name