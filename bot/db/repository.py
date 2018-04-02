from sqlalchemy import func

from bot.db import setup
from bot.db.model import BuildStatistics
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
        statistics = BuildStatistics(author=name, role=role, character=build.class_name,
                                     ascendency=build.ascendency_name, main_skill=build.get_active_gem_name(),
                                     level=build.level, paste_key=paste_key)
        session.add(statistics)
        session.commit()
    else:
        log.info("Duplicate paste_key={}".format(paste_key))


def is_duplicate(paste_key: str) -> bool:
    query = session.query(BuildStatistics).filter(BuildStatistics.paste_key == paste_key)
    return session.query(query.exists()).first()[0]


def get_overview(classes: [str], role=None):
    rowcount = session.query(BuildStatistics).count()
    str = ""
    # todo: add user role check
    if len(classes) == 0:
        asc_count = session.query(BuildStatistics.ascendency, func.count(BuildStatistics.id)). \
            group_by(BuildStatistics.ascendency).all()
        for asc in asc_count:
            str += "{}:\t {}/{} ({:.2f}%)\n".format(asc[0], asc[1], rowcount, asc[1] / rowcount)
    else:
        for arg in classes:
            asc_count = session.query(BuildStatistics.ascendency, func.count(BuildStatistics.id)). \
                group_by(BuildStatistics.ascendency).filter(
                func.lower(BuildStatistics.ascendency).contains(arg.lower())).all()
            for asc in asc_count:
                str += "{}:\t {}/{} ({:.2f}%)\n".format(asc[0], asc[1], rowcount, asc[1] / rowcount)
        if not str:
            str = "No entry found. Input was: '{}'".format(','.join(classes))
    return str
