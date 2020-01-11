from flask_assets import Environment, Bundle

def compile_main_assets(app):
    """Configure main asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
    # Stylesheets Bundle
    css_bundle = Bundle('src/css/main.css',
                         filters='cssmin',
                         output='dist/css/main.min.css',
                         extra={'rel': 'stylesheet/css'})
    # JavaScript Bundle
    js_bundle = Bundle('src/js/main.js',
                       filters='jsmin',
                       output='dist/js/main.min.js')
    # Register assets
    assets.register('css_all', css_bundle)
    assets.register('js_all', js_bundle)
    # Build assets in development mode
    if app.config['FLASK_ENV'] == 'development':
        css_bundle.build(force=True)
        js_bundle.build()

def compile_assets(app):
  """Compile all asset bundles."""
  compile_main_assets(app)