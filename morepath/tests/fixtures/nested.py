import morepath

outer_app = morepath.App()
app = morepath.App('inner', parent=outer_app)


@app.root()
class Root(object):
    pass


class Model(object):
    def __init__(self, id):
        self.id = id


@app.model(model=Model, path='{id}',
           variables=lambda model: {'id': model.id})
def get_model(id):
    return Model(id)


@app.view(model=Model)
def default(request, model):
    return "The view for model: %s" % model.id


@app.view(model=Model, name='link')
def link(request, model):
    return request.link(model)
