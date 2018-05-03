from sqlalchemy import func, or_

from bot.db import setup
from bot.db.model import BuildStatistics, Stat
from models.build import Build
from util.logging import log

session = setup.init()


def add_statistics(name: str, build: Build, paste_key: str, role=None):
    """
    Add a new BuildStatistics object to the DB
    :param name: name of the author/poster of the build
    :param build: the build whose stats we want to save
    :param paste_key: pastekey to allow re-retrieval
    :return:
    """
    if not is_duplicate(paste_key):
        gem_name=build.get_active_skill().get_selected().name
        statistics = BuildStatistics(author=name, role=role, character=build.class_name,
                                     ascendency=build.ascendency_name, main_skill=gem_name,
                                     level=build.level, paste_key=paste_key)
        # statistics.stats = {
        #     'Life': Stat("a", build.get_stat("Player","Life")),
        #     'ES': Stat("b", build.get_stat("Player","EnergyShield")),
        #     'Mana': Stat("Mana", build.get_stat("Player","Mana")),
        # }
        session.add(statistics)
        session.commit()
        # print(session.query(BuildStatistics).first().stats)
    else:
        log.info("Duplicate paste_key={}".format(paste_key))


def is_duplicate(paste_key: str) -> bool:
    query = session.query(BuildStatistics).filter(BuildStatistics.paste_key == paste_key)
    return session.query(query.exists()).first()[0]


def get_overview(classes: [str], role=None):
    rowcount = session.query(BuildStatistics).count()
    str = ""
    # todo: add user role check
    result_set = None
    # print(classes, rowcount)
    result_set = get_ascendency_count(classes)
    # print(result_set)
    for asc in result_set:
        str += "{}:\t {}/{} ({:.2f}%)\n".format(asc[0], asc[1], rowcount, 100* asc[1] / rowcount)

    return "No results found." if not str else str


def get_ascendency_count(classes=None):
    query = session.query(BuildStatistics.ascendency, func.count(BuildStatistics.id)).group_by(
        BuildStatistics.ascendency)
    filters = []
    if len(classes) > 0:
        for asc in classes:
            filters.append(BuildStatistics.ascendency.ilike('%' + asc + '%'))
        if len(filters) > 0:
            query = query.filter(or_(*filters))
    return query.all()
