# coding: utf-8
from jinja2 import Markup


class MomentJS(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, date_format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (
        self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), date_format))

    def format(self, date_format):
        return self.render("format(\"%s\")" % date_format)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
