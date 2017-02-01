import sys
import traceback
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__author__ = 'Giulio Rossetti'
__license__ = "GPL"
__email__ = "giulio.rossetti@gmail.com"


class ExecutionNotifierDecorator(object):

    def __init__(self, username, password, destination=[]):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.username = username
        self.password = password
        self.destination = destination
        self.start = datetime.datetime.now()

    def __call__(self, f):
        """
        Catches any exception and prints a stack trace.
        """

        def wrapper(*args, **kwargs):
            try:
                f(*args, **kwargs)
                self.__send_notification(fname=(f.__name__, args, kwargs), status="OK")
            except Exception:
                tr = "".join(traceback.format_exception(*sys.exc_info()))
                self.__send_notification(fname=(f.__name__, args, kwargs), status="Failed", traceback=tr)
                traceback.print_exc()
        return wrapper

    def __send_notification(self, fname, status, traceback=None):

        end = datetime.datetime.now()
        explased_time = end - self.start

        fromaddr = self.username
        recipients = self.destination
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = "Execution status report [%s]" % fname[0]

        body = "<div><table style='border-collapse: collapse;width: 100%%;'>" \
               "<tbody>" \
               "<thead><tr><th colspan='2'>Report</th></tr></thead>" \
               "<tr style='background: rgba(0, 0, 0, 0.2);'>" \
               "<td style='width: 30%%;'><b>Function name</b></td><td> %s</td> " \
               "</tr><tr style='background: rgba(202, 232, 230, 1);'>" \
               "<td style='width: 30%%;'><b>Positional parameters</b></td><td> %s</td> " \
               "</tr><tr style='background: rgba(0, 0, 0, 0.2);'>" \
               "<td style='width: 30%%;'><b>Named parameters</b></td><td> %s</td> " \
               "</tr><tr style='background: rgba(202, 232, 230, 1);'>" \
               "<td style='width: 30%%;'><b>Started on</b></td><td> %s</td>" \
               "</tr><tr style='background: rgba(0, 0, 0, 0.2); '>" \
               "<td style='width: 30%%;'><b>Ended on</b></td><td> %s</td>" \
               "</tr><tr style='background: rgba(202, 232, 230, 1);'>" \
               "<td style='width: 30%%;'><b>Execution time</b></td><td> %s</td>" \
               "</tr><tr style='background: rgba(0, 0, 0, 0.2);'>" \
               "<td style='width: 30%%;'><b>Final status</b></td><td> %s</td>" \
               "</tr>" \
               "</tbody>" \
               "</table></div>" % (fname[0], fname[1], fname[2], self.start, end, explased_time, status)

        if traceback is not None:
            body = "%s" \
                   "<div style='margin-top:10px;'>" \
                   "<table style='border-collapse: collapse;width: 100%%;>" \
                   "<thead>" \
                   "<tr style='align:center;'><th>Traceback</th></tr>" \
                   "</thead>" \
                   "<tbody>" \
                   "<tr style='background: rgba(208, 145, 58, 0.2);'><td>" \
                   "<pre><code>%s</code></pre>" \
                   "</td></tr>" \
                   "</tbody>" \
                   "</table></div>" % (body, traceback)

        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, self.password)
        text = msg.as_string()
        for r in recipients:
            server.sendmail(fromaddr, r, text)
        server.quit()
