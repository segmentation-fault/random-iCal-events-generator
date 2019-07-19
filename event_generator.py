__author__ = 'antonio franco'

'''
Copyright (C) 2019  Antonio Franco (antonio_franco@live.it)
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random
from ics import Calendar, Event
import arrow
from datetime import datetime, timedelta
from faker import Faker
from markov_text_gen import MarkovTextGen
from types import LambdaType
import sys


class RandomEvents(object):
    def __init__(self, date_start: str, date_end: str, date_format: str, f_duration: LambdaType,
                 markov_gen_titles: MarkovTextGen,
                 markov_gen_description: MarkovTextGen, my_locale: str = 'sv_SE',
                 max_words_description: int = 200) -> object:
        """
        This object creates a series of random events, with random start times, names, locations, urls, and descriptions.
        :param date_start: string representing the start date of all the events, formatted according to the date_format provided
        :param date_end: string representing the end date of all the events, formatted according to the date_format provided
        :param date_format: format of the dates provided, compatible with datetime.strptime; e.g. '%m/%d/%Y %I:%M %p %z'.
        :param f_duration: function giving the duration of the event in seconds, when called. no arguments needed; e.g. lambda: int(2 * 3600 * random.random())
        :param markov_gen_titles: MarkovTextGen object, used to generate titles for the events
        :param markov_gen_description: MarkovTextGen object, used to generate descritption for the events
        :param my_locale: locale, compatible with faker (https://faker.readthedocs.io/en/master/index.html#localization)
        :param max_words_description: maximum number of words per description
        """
        super().__init__()
        self.date_format = date_format
        self.date_start = datetime.strptime(date_start, date_format)
        self.date_end = datetime.strptime(date_end, date_format)
        self.f_duration = f_duration
        self.fake = Faker(my_locale)
        self.markov_gen_titles = markov_gen_titles
        self.markov_gen_descriptions = markov_gen_description
        self.max_words = max_words_description

    def __get_rnd_date__(self) -> datetime:
        time_delta = self.date_end - self.date_start

        return self.date_start + random.random() * time_delta

    def get_rnd_start(self) -> datetime:
        return self.__get_rnd_date__()

    def get_duration(self) -> timedelta:
        return timedelta(seconds=self.f_duration())

    def get_rnd_end(self, my_start, duration) -> datetime:
        return my_start + duration

    def get_rnd_event_time(self) -> tuple:
        start = self.get_rnd_start()
        duration = self.get_duration()
        end = self.get_rnd_end(start, duration)
        created = self.get_rnd_created(start)

        return arrow.get(start), arrow.get(end), \
               duration, arrow.get(created)

    def get_rnd_address(self) -> str:
        return self.fake.address()

    def get_rnd_created(self, my_start) -> datetime:
        # A time between the day before and 30 days prior
        my_before = timedelta(seconds=int(24 * 3600 * random.randint(1, 30)))

        return my_start - my_before

    def get_rnd_url(self) -> str:
        return self.fake.uri()

    def get_rnd_title(self) -> str:
        return self.markov_gen_titles.get_rnd_text_until('.')

    def get_rnd_description(self) -> str:
        return self.markov_gen_descriptions.get_rnd_text(random.randint(1, self.max_words))

    def save_ics_file(self, ics_file: str, n_events: int = 50) -> None:
        """
        Saves n_events random events in the ics file with path ics_file
        :param ics_file (str): path of the ics file
        :param n_events (int): number of events to generate
        """
        c = Calendar()
        for i in range(0, n_events):

            sys.stdout.write("\rCreating event %i of %i" % (i, n_events))
            sys.stdout.flush()

            e = Event()
            e.name = self.get_rnd_title()
            (start, end, duration, created) = self.get_rnd_event_time()
            e.begin = start
            e.end = end
            e.duration = duration
            e.created = created
            e.description = self.get_rnd_description()
            e.url = self.get_rnd_url()
            e.location = self.get_rnd_address()
            c.events.add(e)

        with open(ics_file, 'w') as f:
            f.writelines(c)

        sys.stdout.write("\rDone")
        sys.stdout.flush()


if __name__ == "__main__":
    # Duration uniformly distributed between 0 and 2 hours
    f_duration = lambda: int(2 * 3600 * random.random())

    # Markov text generators preloaded from pickle
    M_titles = MarkovTextGen()
    M_titles.load_dictionary("my_titles.pickle")

    M_descriptions = MarkovTextGen()
    M_descriptions.load_dictionary("my_descriptions.pickle")

    R = RandomEvents("1/1/2015 1:30 PM +0200", "1/1/2022 4:50 AM +0200", '%m/%d/%Y %I:%M %p %z', f_duration, M_titles,
                     M_descriptions)

    R.save_ics_file("example.ics", 25)
