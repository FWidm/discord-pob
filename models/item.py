import re

from util.logging import log


class Item:
    def __init__(self, id, raw_content, variant=None):
        self.id = id
        self.raw_content = raw_content.strip()
        self.variant = variant
        self.name = self.parse_item_name()
        self.added_supports = self.parse_item_for_support()

    def __repr__(self) -> str:
        return "Item [id={}; name={}; Supports={}]".format(self.id, self.name, self.added_supports)

    def parse_item_name(self):
        # see here for regex: https://regex101.com/r/MivGPM/1
        regex = r"\s*Rarity:.*\n\s*(.*)\n"
        matches = re.findall(regex, self.raw_content, re.IGNORECASE)
        name = "UNDEFINED"
        try:
            name = matches[0]
        except IndexError as err:
            log.warning("Name could not be retrieved. Trying string split method Err={}".format(err))
            name = self.raw_content.split('\n')[0]

        return name

    def parse_item_for_support(self):
        # Socketed Gems are Supported by level 20 Elemental Proliferation
        add_supports = []
        # see here for regex: https://regex101.com/r/CcxRuz/1
        regex = r"({variant:([0-9,]*)}|)Socketed Gems are Supported by level ([0-9]*) ([a-zA-Z ]*)"
        try:
            supports = re.findall(regex, self.raw_content, re.IGNORECASE)
            for support in supports:
                # if either no variant exists, or our variant matches the current supports variant
                if 'variant' not in support[0] or self.variant in support[0]:
                    add_supports.append({"name": support[3], "level": support[2]})
        except AttributeError as err:
            return
        return add_supports
