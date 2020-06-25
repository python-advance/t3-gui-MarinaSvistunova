import unittest

import os
import sys
import time
import os.path as op
from functools import partial
from kivy.clock import Clock

# it's not a relative import!
# test with --pythonpath "<path to main.py>"
from first import MainApp


class Test(unittest.TestCase):
    # sleep function that catches `dt` from Clock
    def pause(*args):
        time.sleep(0.000001)

    # main test function
    def run_test(self, app, *args):
        Clock.schedule_interval(self.pause, 0.000001)

        # Do something
        app.root.ids.a.text = "2"
        app.root.ids.b.text = "2"
        app.root.ids.c.text = "2"

        app.root.solve()

        self.assertEqual('D < 0', app.root.ids.d.text)
        self.assertEqual('Нет корней', app.root.ids.x.text)

        # app.my_button.dispatch('on_release')
        # self.assertEqual('Hello Test', app.my_button.text)
        #self.assertEqual('Fail Test', app.my_button.text)

        # Comment out if you are editing the test, it'll leave the
        # Window opened.
        app.stop()

    # same named function as the filename(!)
    def test_example(self):
        app = MainApp()
        p = partial(self.run_test, app)
        Clock.schedule_once(p, 0.000001)
        app.run()

if __name__ == '__main__':
    unittest.main()