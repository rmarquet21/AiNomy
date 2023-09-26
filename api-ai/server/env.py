# pylint: skip-file
class Env:
    """
    the full canonical url of the tenant
    example: https://dev.ainomy.com
    """
    AINOMY_CANONICAL_URL = "AINOMY_CANONICAL_URL"

    """
    The answer below pertains primarily to Signed Cookies, an implementation of the concept of sessions (as used in
    web applications). Flask offers both, normal (unsigned) cookies (via request.cookies and response.set_cookie())
    and signed cookies (via flask.session).
    We are using this variable to encrypt jwt tokens inside cookies.
    see : https://stackoverflow.com/a/48596852
    """
    FLASK_SECRET = "FLASK_SECRET"

    """
    use fake data instead relying on the database. The system doesn't use the authentication as
    well
    exemple : 0 if you are using standard authentication and datastore otherwise 1
    """
    FAKE_DATA = "FAKE_DATA"

    """
    Whether debug mode is enabled. When using flask run to start the development server, an interactive debugger
    will be shown for unhandled exceptions, and the server will be reloaded when code changes.
    The debug attribute maps to this config key. This is enabled when ENV is 'development'
    and is overridden by the FLASK_DEBUG environment variable. It may not behave as expected if set in code.
    see: https://flask.palletsprojects.com/en/1.1.x/config/#DEBUG
    """
    FLASK_DEBUG = "FLASK_DEBUG"

    """
    What environment the app is running in. Flask and extensions may enable behaviors based on the environment, such as
    enabling debug mode. The env attribute maps to this config key.
    This is set by the FLASK_ENV environment variable and may not behave as expected if set in code.
    see: https://flask.palletsprojects.com/en/1.1.x/config/#DEBUG
    """
    FLASK_ENV = "FLASK_ENV"

    """
    This variable is used for IDE to load the environment configuration from local "/environment/local/.env"
    environment when running the server in debug.
    exemple : 0 don't load the variables from "/environment/local/.env" otherwise load the variables
    """
    LOCAL_DOTENV = "LOCAL_DOTENV"

    """
    the connexion string of the datastore database. Currently we are using
    mongodb.
    example: mongodb://mongodb:1234@localhost/ainomy
    """
    AINOMY_DATABASE_URL = "AINOMY_DATABASE_URL"

    """
    See swagger ui documentation
    """
    SWAGGER_UI = "SWAGGER_UI"
