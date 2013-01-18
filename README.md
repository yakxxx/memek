# Memek - discussion monitoring tool

##What is it?

Memek is tool to automatically monitor subjects of discussion in the Internet over time.
It's implementation gets data to analysis from Polish site [Wykop](http://wykop.pl) (it's Polish clone of reddit).
It consists of two packages: crawler and miner. Crawler gets data of articles and comments from WykopAPI.
Miner is responsible for extraction of main discussion subjects.

##Algorithm outline

`split_into_weeks.py` gets all the data from DB, splits it in 7 days long periods and puts it in files.
`iterative_finder.py` iterates through weeks and selects collocations (bigrams and trigrams).
Selection is based of chi-square ranking of collocations with support above some threshold.
All selected collocations are compared to set of collocations from previous 4 weeks to remove common language collocations and subjects which where present in discussion for a while.
Remaining collocations are filtered to remove bigrams which are parts of trigrams. After filtering collocations are treated as emerging subjects of discussion in currently processed week.

##Requirements

* Python 2.7
* MongoDB
* Virtualenv
* internet connection ;)
* Linux preferably Ubuntu. (maybe you can run it on Windows but i didn't test it)

##Installation

Before running `update_articles.py`, `update_comments.py` or `split_into_weeks.py` you have to have MongoDB running on your localhost. If you work on prepared `weeks` data you can omit installation of mongo.
Installation guide of MongoDB is [here](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-linux/)

* sudo apt-get install python-virtualenv
* git clone https://github.com/yakxxx/memek.git (or you can dl it and upnack manually [https://github.com/yakxxx/memek/archive/master.zip](https://github.com/yakxxx/memek/archive/master.zip) )
* cd memek
* virtualenv env
* source env/bin/activate
* pip install -r requirements.txt

From now on you are ready to run `memek`. Remember to `source` to your virtualenv every time you start playing with memek. ( `source env/bin/activate`, when finished just type `deactivate`)

##Configuration

To run crawler on wykop you have to get app_key and app_secret from wykopAPI site.

Put it in main directory in secret_config.py

```python
APP_KEY = 'xxx'
APP_SECRET = 'xxx'
```
 
##Running 

### Crawling articles
To crawl articles run `python update_articles.py`. It will crawl wykopAPI and put articles in your `MongoDB`.
After a while You will probably hit daily request limit on wykop, but to that moment You probably have crawled about 2 years of articles.
Currently it is impossible to crawl rest of articles next day, however `update_articles.py` runs in incremental mode so running it next day will update your db with new data from that day.

###Crawling comments
**WARNING**: crawling comments will produce enorumous ammount of data and will slow your later processing.
Mining modules can be used without comments crawled, just omit invocation of `update_comments.py` script. 

To crawl comments for articles run `python update_comments.py`. 
It runs in incremental mode and every run will update database with comments for crawled articles which doesn't have comments for them crawled yet.
It won't update new comments for articles which were crawled once. It checks in DB for articles without any comments and crawls them.

###Creating text corpora
To generate corpora for weeks run 
`python split_into_weeks.py 2011 1 1` where arguments are year month and day of starting date.
It will get data from your database from starting date, split it into week long chunks, filter it and save to files in weeks directory. 

###Mining discussion themes

**WARNING**: If you already have weeks files in `weeks` You can start from this point and omit previous steps and instalation of MongoDB

To get collocations out of our corpora run:

`python iterative_finder 108 weeks` where 108 is number of last week in your weeks dir and `weeks` is subdirectory to get corpus files. 
This command outputs found collocations to file `output.txt`

### Generating timeline

You can generate html/js/css site to present mined data on timeline. To generate this file copy your `output.txt` into presentation directory.

```bash
cp output.txt presentation
cd presentation
python create_index.py
```

You've just generated `index.html`. Now see it with your browser. If You want to put it on webserver remember to copy js, css images and inc directories with your index.html.


### Testing

Application comes with unittests. You can run them by typing

```bash
nosetests -s -vv
```

