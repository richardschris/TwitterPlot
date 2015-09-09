from flask import Flask, render_template, request, jsonify
import tweet_plot
import os

twitterplot = Flask(__name__)
IMAGE_URL = 'static/images/'
# twitterplot.debug = True
# For the love of all that is holy, keep debug off unless you want disaster


@twitterplot.route('/')
def home():

    return render_template('main-template.html', image_url=IMAGE_URL)


# here is the little REST API
@twitterplot.route('/plot', methods=['POST', 'GET'])
def plot_data():
    """
    We grab the data from JQuery and pass it to the
    plotting function, which generates a new image for JQuery to reload.
    """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

    # here goes code to take the 'data_list' argument from the incoming JSON

    filename = os.path.join(SITE_ROOT, 'testdata.json')
    plot_params = tweet_plot.Parameters()

    plot_params.plot_typehandle(request.args.get('plot_type'))
    plot_params.add_search_list(request.args.get('search_list'))

    if request.args.get('plottotal') == 'true':
        plot_params.plot_total = True
    else:
        plot_params.plot_total = False
    interval = request.args.get('interval')

    if interval == '':
        plot_params.interval = 15
    else:
        plot_params.interval = int(interval)

    plot_params.start_time = request.args.get('start_time')
    plot_params.end_time = request.args.get('end_time')
    plot_params.filename = filename

    # we use this code to deal with images indexed for a userid
    # most of it is platform-independent
    # it checks if the userid directory exists
    userid = str(request.args.get('userid'))
    user_images = os.path.join(SITE_ROOT, IMAGE_URL, userid)
    if os.path.exists(user_images):
        plot_params.image_destination(os.path.join(user_images, 'image.png'))
    else:
        os.mkdir(user_images)
        plot_params.image_destination(os.path.join(user_images, 'image.png'))

    tweet_plot.interface(plot_params)
    print(os.path.join(user_images, str(1) + '.png'))

    # the following is kind of ugly, but it's platform-independent
    # the number of images saved can be adjusted, but I've just hard-coded it
    # to 10 for the sake of simplicity.
    if os.path.exists(os.path.join(user_images, '1.png')):
        for i in range(10, 0, -1):
            if i == 10 and os.path.exists(os.path.join(user_images,
                                          str(i) + '.png')):
                os.remove(os.path.join(user_images, '10.png'))

            elif os.path.exists(os.path.join(user_images, str(i) + '.png')):
                os.rename(os.path.join(user_images, str(i) + '.png'),
                          os.path.join(user_images, str(i + 1) + '.png'))

    os.rename(os.path.join(user_images, 'image.png'),
              os.path.join(user_images, '1.png'))

    # necessary for it to work! Browsers expect a browsable URL, so the path
    # must be relative to the root of the web server.
    return jsonify({'image_url': str(IMAGE_URL + userid + '/')})


@twitterplot.after_request
def add_header(response):
    """
    Old function for making sure new images loaded when /plot was POSTed to
    by sending an HTML header giving a max cache age of 0. Since the
    current version uses JQuery to do things, this largely serves to make sure
    the HTML, JS, and CSS files load whenever changed. It should probably be
    removed on a prodution server, but it doesn't change much.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    # DO NOT EVER RUN THIS AS A MAIN APP ON A SERVER. EVEN COMMENT OUT THE
    # DEBUG LINE JUST TO BE SAFE
    twitterplot.debug = True
    twitterplot.run()
