import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models.models import (
    Post,
    Submitter
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        submitter = Submitter(name='tester')
        dbsession.add(submitter)
        transaction.commit()
        sub_id = dbsession.query(Submitter.id). \
                 filter(Submitter.name == 'tester').scalar()
        post = Post(title="job title",
                    company="the testing company",
                    post_date="13-Apr-2016Z201530",
                    description="this is a really short description",
                    submitter=sub_id)
        dbsession.add(post)
