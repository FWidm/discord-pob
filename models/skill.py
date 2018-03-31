class Skill:
    def __init__(self, gems, main_active_skill, slot=None):
        self.slot = slot
        self.gems = gems
        try:
            self.main_active_skill = int(main_active_skill)
        except:
            self.main_active_skill = None
        self.links = len(gems)

    def __repr__(self) -> str:
        return "Skill [slot={}; gems={}; links={}; selected={}]".format(self.slot, self.gems, self.links,
                                                                        self.main_active_skill)

    def get_selected(self):
        if self.main_active_skill:
            active_skills = [gem for gem in self.gems if "support" not in gem.id.lower()]
            # print(active_skills)
            return active_skills[self.main_active_skill - 1]
        return None

    def get_links(self, item=None, join_str=" + "):
        # Join the gem names, if they are in the slected skill group and if they are enabled. Show quality and level if level is >20 or quality is set.
        ret = join_str.join(
            [gem.name + " ({}/{})".format(gem.level, gem.quality) if (gem.level > 20 or gem.quality > 0)
             else gem.name for gem in self.gems if gem.enabled == True])
        if item:
            supports = item.added_supports
            if supports and isinstance(supports, list):
                ret += "\n(+ " + join_str.join([gem['name'] + " (" + gem['level'] + ")" for gem in supports])
                ret += " from: *{}*)".format(item.name)
        return ret
