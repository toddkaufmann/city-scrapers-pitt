from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class AlleAirportAuthoritySpider(CityScrapersSpider):
    name = "alle_airport_authority"
    agency = "Allegheny County Airport Authority"
#// check tz
    timezone = "America/New_York"
    allowed_domains = ["www.flypittsburgh.com"]
    start_urls = ["http://www.flypittsburgh.com/about-us/leadership"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        # get def time
        #  ".. unless otherwise"
        # def location

        # text doesn't really have any structure..
        lines = response.select().extract().split('\n')
    # ['<p>\r',
        lines.pop()
    #  '            <strong>Allegheny County Airport Authority 2019 Board Meetings</strong><br>\r',
        lines.pop()
    #  '            <em>*Board Meetings will be held\xa0on the 3rd Friday of the month at 11:30 a.m. in Conference Room A, 4th Flr Mezzanine, Landside Terminal, Pittsburgh International Airport, unless otherwise noted below.</em><br><br>\r',
        clean:  \xa0 -> space
        if lines[0].match("meetings will be held on (.+) of the month at (.+) in (.+), unless otherwise noted below"):
            rDay, rTime, rLocation = 1,2,3
        else:
            throw error
    #  '            <strong>\r',
        lines.pop()
    #  '              <u>2019 Board Meeting Dates</u><br>\r',
        year = lines[0][3:7]
        if int(year) < 2010:
            throw error
        # Now, month day lines
        for line in lines:
            clean \xa0+ -> ' ', <br> \r
    #  'January 18<br>\r',
    #  'February 15<br>\r',
    #  'March 15\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0<br>\r',
    #  'April 19<br>\r',
    #  'May 17\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0<br>\r',
    #  'June 21\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0<br>\r',
    #  'July 19<br>\r',
    #  '*August – NO BOARD MEETING<br>\r',
    #  '*September 20 – (Allegheny County Airport, West Mifflin)<br>\r',
    #  'October 18<br>\r',
    #  'November 15<br>\r',
    #  'December 20</strong><br><br>\r',
    #  'For information, call (412) 472-3500.</p>']

        for item in response.css(".meetings"):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        # eg, title = item.css(".title::text").extract_first()
        # return title
        return ""

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
