# Twitter #HashTag map and analysis

### Visualize all the tweets worldwide with this quickstart guide

Quickstart
----------

Run the following commands to bootstrap your environment

    git clone https://github.com/michaeldao/vicSafe
    cd vicSafe
    pip install -r requirements/dev.txt
    cp .env.example .env
    npm install
    npm start  # run the webpack dev server and flask server using concurrently
    
You will see a pretty welcome screen on http://localhost:5000

Deployment
----------

Do not deploy with the quickstart, instead do this for cloud hosting.
Deployment
----------

To deploy::

    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export DATABASE_URL="<YOUR DATABASE URL>"
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``.


We used ec2 in our example

To deploy::

    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export DATABASE_URL="<YOUR DATABASE URL>"
    npm run build   # build assets with webpack
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``.

