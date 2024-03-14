## Flask + Multiple Vite (SolidJS, TailwindCSS)

This repo is an example of matching multiple Vite projects to Flask Blueprints.

This project is set up with one Flask app and two Vite apps. Each Vite app is set up with SolidJS and TailwindCSS.

## Vite to Flask Blueprint Structure

| Vite App      | -> | Flask Blueprint    |
|---------------|----|--------------------|
| vite_frontend | -> | flask_app/frontend |
| vite_backend  | -> | flask_app/backend  |

## How it works

The pyproject.toml file is used by the `dev` package to find the Vite apps and Flask blueprints.

The `dev` package has a few commands to build and run the Vite apps, and to run the Flask server.

When the Vite apps are built, they compile into a dist folder, which is then moved to the Flask
blueprint and served by the Flask server.

The library pyhead is used to inject the Vite files into the Flask template.


## Setup

### Set up the Python environment

Linux/Darwin:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Set up all Vite apps

```bash
python3 dev vite-install
```

### Build the Vite apps, then run the Flask server

```bash
python3 dev vite-build-run
```

### Only build the Vite apps

```bash
python3 dev vite-build
```

### Run a Vite app in development mode (runs on port 3000)

```bash
python3 dev vite-run <app-name>
# example
python3 dev vite-run vite_frontend
```

## Things to note

### Vite static files

Vite has a couple of ways of handling static files.
You can import them using `import image_var from './image.png'`, using this method
will hash the file name and place it in the `dist/assets` folder.

Currently, the `dev` package will move these over, but if the Flask blueprint's static folder is
not set up correctly, the files will not be served. For example, the static route will be compiled
as `/assets/image.123456.png` but the Flask blueprint will be looking for
`/your_bp/static/assets/image.123456.png`. You will need to set up the static folder in the blueprint
to match the Vite output.

#### Recommended approach

It's recommended to place all static files in the folder called `static`
in the Vite app. This will be moved over to the Flask app's global static folder (and not cached).
You can then use images in the vite app without importing them, like so:

```html
<img src="/static/image.png" alt="image"/>
```

### Vite, with the SolidJS Router

This project is using the SolidJS Router. This looks at the current URL to render the SolidJS route.
This means when building the Vite app, you must start at the base URL of the Flask blueprint.

For example, if you have a route in the Flask blueprint called `/backend`, you must set the base URL
in the Vite app to `/backend`.

`vite_backend/__router__.jsx`

```javascript
...
<Router>
    <Routes>
        <Route path="/backend">
            <Route path="/" component={Index}/>
        </Route>
    </Routes>
</Router>
...
```

Now when you visit the Flask route `/backend`, the Vite app will render the `Index` component.
