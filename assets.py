from flask_assets import Environment, Bundle

jquery = Bundle('jquery/jquery.min.js')
popper = Bundle('Popper/popper.min.js')
bootstrap_js = Bundle('bootstrap/js/bootstrap.min.js')
bootstrap_css = Bundle('bootstrap/css/bootstrap.min.css')
main_css = Bundle('scss/main.scss', filters='libsass', depends='scss/*.scss', output='gen/main.css')
paho = Bundle('paho/paho-mqtt-min.js')


assets = Environment()
assets.register('jq_js', jquery)
assets.register('popper_js', popper)
assets.register('bs_js', bootstrap_js)
assets.register('bs_css', bootstrap_css)
assets.register('main_css', main_css)
assets.register('paho', paho)
