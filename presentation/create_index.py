import codecs
from datetime import date, datetime, timedelta
from jinja2 import FileSystemLoader, Template, Environment
import logging
from pprint import pprint\

month_blocks = []
class Utils:
    
    @classmethod
    def date_to_julian_day(cls, my_date):
        """Returns the Julian day number of a date."""
        a = (14 - my_date.month)//12
        y = my_date.year + 4800 - a
        m = my_date.month + 12*a - 3
        return my_date.day + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - 32045
    
    @classmethod
    def create_search_link(cls, query, start):
        stop = start + timedelta(days=7)
        start = cls.date_to_julian_day(start)
        stop = cls.date_to_julian_day(stop)
        
        return "http://www.google.pl/search?q=%%22%s%%22 daterange:%d-%d site:wykop.pl" % (query, start, stop)


def select_month_block(current_month_block, next_date):
    curr_date = current_month_block['month_date'] if current_month_block else date(year=1970, month=1, day=1)
    
    if not current_month_block:
        current_month_block = {'month_date': date(year=next_date.year, month=next_date.month, day=1), 'month_data': []}

    elif date(year=curr_date.year, month=curr_date.month, day=1) < \
                date(year=next_date.year, month=next_date.month, day=1):
       
        current_month_block = {'month_date': date(year=next_date.year, month=next_date.month, day=1), 'month_data': []}
    else:
        return current_month_block
    
    month_blocks.append(current_month_block)    
    return current_month_block

def render_template(month_blocks):
    env = Environment(loader=FileSystemLoader(''))
    tpl = env.get_template('template.html')
    html = tpl.render(months=month_blocks, utils=Utils)
    f = codecs.open('index.html', 'w', 'utf-8')
    f.write(html)
    f.close()



if __name__ == '__main__':
    f = codecs.open('output.txt', 'r', 'utf-8')

    current_month_block = None
    
    for i, line in enumerate(f):
        line = line.rstrip()
        parts = line.split(';')
        try:
            start = datetime.strptime(parts[0], "%Y-%m-%d").date()
            stop = datetime.strptime(parts[1], "%Y-%m-%d").date()
        except Exception as e:
            print e
            logging.error("Malformed output.txt in line %d" % i)
            
        try:
            memes = parts[2:]
        except IndexError:
            memes = []
            
        current_month_block = select_month_block(current_month_block, start)
        current_month_block['month_data'].append({'week_data': memes, 'week_date': start})
    render_template(month_blocks)
            