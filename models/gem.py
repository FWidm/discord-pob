class Gem:
    def __init__(self, id, name, level, quality, skill_part, enabled=''):
        self.name = self.translate_name(name)
        self.level = int(level)
        self.quality = int(quality)
        self.id = id
        self.skill_part = int(skill_part) if skill_part else None
        self.enabled = True if enabled == 'true' else False

    def __repr__(self) -> str:
        return "Gem [name={}]".format(self.name)

    def translate_name(self, name):
        if name == 'UniqueAnimateWeapon':
            name = 'Manifest Dancing Dervish'
        if name == 'ChaosDegenAuraUnique':
            name = "Death Aura"
        if name == 'IcestormUniqueStaff12':
            name = "Ice Storm"
        return name
