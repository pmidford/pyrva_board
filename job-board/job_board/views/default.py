from pyramid.response import Response
from pyramid.view import view_config

import logging

from sqlalchemy.exc import DBAPIError

from ..models import (
    Post,
    Submitter,
    )


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_view(request):
    session = request.dbsession
    try:
        posts = session.query(Post)
        post_list = []
        for post in posts:
            s_query = session.query(Submitter.name)
            s_name = s_query.filter(Submitter.id == post.submitter).scalar()
            post_list.append({'title': post.title,
                             'company': post.company,
                             'posted': post.post_date,
                             'description': post.description,
                             'submitter': s_name})
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    logging.info("Post_list: {0}".format(repr(post_list)))
    return {'posts': post_list}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyrva_jobs_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
