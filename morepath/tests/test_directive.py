from .fixtures import basic, nested
from morepath import setup
from morepath.config import Config
from morepath.request import Response
from morepath.view import render_html
from morepath.app import App
import morepath
import reg

from werkzeug.test import Client


def test_basic():
    setup()
    basic.app.clear()

    config = Config()
    config.scan(basic)
    config.commit()

    c = Client(basic.app, Response)

    response = c.get('/foo')

    assert response.data == 'The view for model: foo'

    response = c.get('/foo/link')
    assert response.data == 'foo'


def test_basic_json():
    setup()
    basic.app.clear()

    config = Config()
    config.scan(basic)
    config.commit()

    c = Client(basic.app, Response)

    response = c.get('/foo/json')

    assert response.data == '{"id": "foo"}'


def test_basic_root():
    setup()
    basic.app.clear()

    config = Config()
    config.scan(basic)
    config.commit()

    c = Client(basic.app, Response)

    response = c.get('/')

    assert response.data == 'The root: ROOT'

    # @@ is to make sure we get the view, not the sub-model
    response = c.get('/@@link')
    assert response.data == ''


def test_nested():
    setup()
    nested.outer_app.clear()
    nested.app.clear()

    config = Config()
    config.scan(nested)
    config.commit()

    c = Client(nested.outer_app, Response)

    response = c.get('/inner/foo')

    assert response.data == 'The view for model: foo'

    response = c.get('/inner/foo/link')
    assert response.data == 'inner/foo'


def test_imperative():
    setup()

    class Foo(object):
        pass

    @reg.generic
    def target():
        pass

    app = App()

    c = Config()
    c.action(app, app)
    foo = Foo()
    c.action(app.function(target), foo)
    c.commit()

    assert target.component(lookup=app.lookup()) is foo


def test_basic_imperative():
    setup()

    app = morepath.App()

    class Root(object):
        def __init__(self):
            self.value = 'ROOT'

    class Model(object):
        def __init__(self, id):
            self.id = id

    def get_model(id):
        return Model(id)

    def default(request, model):
        return "The view for model: %s" % model.id

    def link(request, model):
        return request.link(model)

    def json(request, model):
        return {'id': model.id}

    def root_default(request, model):
        return "The root: %s" % model.value

    def root_link(request, model):
        return request.link(model)

    c = Config()
    c.action(app, app)
    c.action(app.root(), Root)
    c.action(app.model(model=Model, path='{id}',
                       variables=lambda model: {'id': model.id}),
             get_model)
    c.action(app.view(model=Model),
             default)
    c.action(app.view(model=Model, name='link'),
             link)
    c.action(app.view(model=Model, name='json',
                          render=morepath.render_json),
             json)
    c.action(app.view(model=Root),
             root_default)
    c.action(app.view(model=Root, name='link'),
             root_link)
    c.commit()

    c = Client(app, Response)

    response = c.get('/foo')
    assert response.data == 'The view for model: foo'

    response = c.get('/foo/link')
    assert response.data == 'foo'

    response = c.get('/foo/json')
    assert response.data == '{"id": "foo"}'

    response = c.get('/')
    assert response.data == 'The root: ROOT'

    # @@ is to make sure we get the view, not the sub-model
    response = c.get('/@@link')
    assert response.data == ''

def test_json_directive():
    setup()

    app = morepath.App()

    class Model(object):
        def __init__(self, id):
            self.id = id

    def default(request, model):
        return "The view for model: %s" % model.id

    def json(request, model):
        return {'id': model.id}

    c = Config()
    c.action(app, app)
    c.action(app.model(path='{id}',
                       variables=lambda model: {'id': model.id}),
             Model)
    c.action(app.json(model=Model),
             json)
    c.commit()

    c = Client(app, Response)

    response = c.get('/foo')
    assert response.data == '{"id": "foo"}'

def test_redirect():
    setup()

    app = morepath.App()

    class Root(object):
        def __init__(self):
            pass

    def default(request, model):
        return morepath.redirect('/')

    c = Config()
    c.action(app, app)
    c.action(app.root(),
             Root)
    c.action(app.view(model=Root, render=render_html),
             default)
    c.commit()

    c = Client(app, Response)

    response = c.get('/')
    assert response.status == '302 FOUND'
