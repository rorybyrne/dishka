.. _cyclopts:

Cyclopts
=================================


Though it is not required, you can use *dishka-cyclopts* integration. It features automatic injection to command handlers.
The integration manages REQUEST scope automatically for each command execution.



How to use
****************

1. Import

.. code-block:: python

    from dishka.integrations.cyclopts import setup_dishka, inject

2. Create container and setup it to cyclopts app.

.. code-block:: python

    import cyclopts
    from dishka import make_container
    from dishka.integrations.cyclopts import setup_dishka

    app = cyclopts.App(name="myapp")

    # Define commands here

    container = make_container(MyProvider())
    setup_dishka(app=app, container=container)

Or configure scope.

.. code-block:: python

    import cyclopts
    from dishka import make_container, Scope
    from dishka.integrations.cyclopts import setup_dishka

    app = cyclopts.App(name="myapp")

    # Define commands here

    container = make_container(MyProvider())
    setup_dishka(
        app=app,
        container=container,
        scope=Scope.SESSION  # Default is REQUEST
    )

3. Mark those of your command handlers parameters which are to be injected with ``FromDishka[]``. Make sure you call ``setup_dishka`` after defining commands.

.. code-block:: python

    from dishka import FromDishka

    @app.command
    def hello(interactor: FromDishka[Interactor]):
        ...

     # setup_dishka call here

Notes
****************

* The integration only supports ``Container``, not async ``AsyncContainer``
* REQUEST scope is entered and exited automatically for each command execution

