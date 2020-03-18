from unittest.mock import MagicMock, patch

import doorpi

from . import EVENT_ID, EVENT_EXTRA
from ..mocks import DoorPi, DoorPiTestCase


class TestActionInstantiation(DoorPiTestCase):

    @patch("doorpi.actions.log.instantiate")
    def test_nocolon(self, instantiate):
        doorpi.actions.from_string("log")
        instantiate.assert_called_once_with()

    @patch("doorpi.actions.log.instantiate")
    def test_colon(self, instantiate):
        doorpi.actions.from_string("log:")
        instantiate.assert_called_once_with()

    @patch("doorpi.actions.log.instantiate")
    def test_args(self, instantiate):
        doorpi.actions.from_string("log:foo,bar,baz")
        instantiate.assert_called_once_with("foo", "bar", "baz")

    def test_emptystring(self):
        ac = doorpi.actions.from_string("")
        self.assertIsNone(ac)

    def test_underscore(self):
        with self.assertRaises(ValueError):
            doorpi.actions.from_string("_test")


class TestCallbackAction(DoorPiTestCase):

    def test_callback(self):
        mock = MagicMock()
        ac = doorpi.actions.CallbackAction(
            mock, "some arg", kw="some keyword arg", args=["foo", "bar"])
        ac(EVENT_ID, EVENT_EXTRA)
        mock.assert_called_once_with("some arg", kw="some keyword arg", args=["foo", "bar"])

    def test_callback_uncallable(self):
        with self.assertRaises(ValueError):
            doorpi.actions.CallbackAction(None)


class TestCheckAction(DoorPiTestCase):

    def test_check_passing(self):
        mock = MagicMock()
        ac = doorpi.actions.CheckAction(mock)
        ac(EVENT_ID, EVENT_EXTRA)
        mock.assert_called_with()

    @patch("doorpi.DoorPi", DoorPi)
    def test_check_failing(self):
        mock = MagicMock(side_effect=Exception)
        ac = doorpi.actions.CheckAction(mock)

        with self.assertLogs("doorpi.actions", "ERROR"):
            ac(EVENT_ID, EVENT_EXTRA)
        DoorPi().doorpi_shutdown.assert_called_once_with()
