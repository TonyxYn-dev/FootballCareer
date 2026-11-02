import tempfile
import unittest
from engine.clock import WorldClock
from engine.events import EventBus, DomainEvent
from persistence.save_manager import SaveManager

class StageOneTests(unittest.TestCase):
    def test_clock_advances(self):
        clock = WorldClock("2026-01-01")
        clock.advance_days(7)
        self.assertEqual(clock.current_date, "2026-01-08")

    def test_clock_rejects_negative(self):
        with self.assertRaises(ValueError):
            WorldClock("2026-01-01").advance_days(-1)

    def test_event_bus(self):
        received = []
        bus = EventBus()
        bus.subscribe("test", received.append)
        event = DomainEvent("test", {"value": 3})
        bus.publish(event)
        self.assertEqual(received, [event])

    def test_save_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = SaveManager(tmp)
            manager.save("slot1", {"career_name": "Test"})
            loaded = manager.load("slot1")
            self.assertEqual(loaded["career_name"], "Test")
            self.assertEqual(loaded["schema_version"], 1)

if __name__ == "__main__":
    unittest.main()
