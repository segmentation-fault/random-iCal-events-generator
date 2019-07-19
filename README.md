# random-iCal-events-generator
Generates random events in iCal ics format. It generates a specified number of events with a random duration, start date and end date between the provided bounds, creation date, url and location according to the provided locale, and name and description according to a random Markov Chain generator. Data for titles and descriptions were obtained from:

- https://data.opendatasoft.com/explore/dataset/new_reservations%40townofchapelhill/table/
- https://bouldercolorado.gov/open-data/library-events-and-programs/
- https://catalog.data.gov/dataset?tags=events

All the data was cleaned, removing telephone numbers and emails.

Examples of usage are provided in the main of every py file. 
