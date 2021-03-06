# TwitterPlot
A small flask app to produce charts from twitter data. If you have a JSON file from Twitter (these can be gathered with the streaming API; I like the Tweepy library for Python), you can search through it and produce plots reasonably quickly.

Images are stored in static/images/userid, where userid is set via Javascript on ready. The userid is just the timestamp on first load, and it lives in localstorage. The software stores the last 10 images for a user, identified via a unique ID stored in browser storage. The number of images can be changed reasonably easily in twitterplot.py and render.js; extending and simplifying that functionality is coming later.

## Using Multiple Files

You can use multiple files. Presently this is configured at the top of twitterplot.py in the function datafiles(), which returns the appropriate list. 

```
debate_data = JsonFile('filename', 'display name')
```
The filename attribute is just the file name, and the display name is the name that appears in the 
selection box. Twitterplot expects data to be in the root; this can be changed, but it should be changed elsewhere in the
app.

## Running Locally
To run locally, simply run

```
python twitterplot.py
```

and access it via

```
http://localhost:5000
```

You can also use tweet_plot.py for your own purposes. Simply import it and do the following.

```python
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
filename = os.path.join(SITE_ROOT, 'data.json')
plot_params = tweet_plot.Parameters()
```

Take a look at the Parameters class for information on what you can pass through, and the methods for doing so (most you want to manually set). Be aware that much of the error checking is done via the Javascript on the web side, so the code here doesn't do much error checking. I am aware this is not ideal, but since I'm already checking it coming in, use at your own risk.

This object is then passed into the interface function.

## The Parameters

#### Interval
```python
interval = 15
```
Interval sets the resolution of a search over time in minutes. It should work for any interval of time, but I've only done serious testing with ints, so be aware!

#### Start Time
```python
start_time = '00:00'
```
This is for truncating a line plot over time. It takes a string in the format 'HH:MM' and starts the search from that interval of time past the beginning of the data set. It does NOT take a time, because the data sets can be variable and they are not readily accessible to the app without beginning a search; this is a direction for future work.

#### End Time
```python
end_time = '00:00'
```
This is the end time for a truncated line plot. Same as above, except that it's about where the search ends.

#### Search List
```python
search_list = []
```
The search list is an empty list. It's manipulated via a method, add_search_list(search), which takes a string as an argument. This function then converts said string to lower-case, and then splits it into a list. It eliminates duplicate terms.

#### Plot Total
```python
plot_total = False
```
This applies to a line plot. If True, the data is summed before being plotted.

#### Filename
```python
filename = ''
```
This is the source data. It's up to you to make sure the file exists (I check elsewhere).

#### Plot Type
Plot type is handled via a method to add it, plot\_typehandle(\_plot\_type). It takes a string. There are four options for plots.

1. 'bar_plot' : a bar plot of the data.
2. 'pie_plot' : a pie plot of the data.
3. 'time_lineplot' : a line plot of tweets over time (supports up to 5 search terms; needs more colors specified to go further).
4. 'time_truncate' : a line plot that truncates based on the start_time and end_time variables.

It raises a ValueError if you don't pass one of these in.

#### Image Destination
Lets you set the destination of the image. It should be safe, but since the program creates the PNG, it will throw an error if you don't have write permissions. Use the image_destination(image_dest) function, which does some safe things with OS paths. It assumes it will write to a subdirectory and is written with this behavior in mind.

## The Interface Function

If you've done everything right with the Parameters instance, you can pass to the interface function the instance, like so
```python
tweet_plot.interface(plot_params)
```
and it should take care of the rest. It will output the file silently to your image_dest, so be sure it's set properly. You can mess with the individual functions if you want. The search data being tossed around is almost entirely dictionaries. It is easy to turn it into a CSV file, so that's an easy application for the search functions.
