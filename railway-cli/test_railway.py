import unittest
from datetime import datetime
from railway_system import (
    RailwaySystem, EntityNotFoundError, TrackBusyError,
    SecurityCheckFailedError, InvalidScheduleError, TicketSoldOutError
)


class TestRailwaySystem(unittest.TestCase):

    def setUp(self) -> None:
        self.system = RailwaySystem()
        self.system.add_track("T1", "Main", 10.5)
        self.system.add_track("T2", "Side", 5.0)
        self.system.add_station("S1", "Москва", ["T1"])
        self.system.add_station("S2", "Санкт-Петербург", ["T2"])
        self.system.add_locomotive("L1", "EP2K", 4800)
        self.system.add_wagon("W1", "passenger", 60)
        self.system.assemble_train("TR1", "L1", ["W1"], ["S1", "S2"])

    def test_assemble_train_success(self) -> None:
        self.assertIn("TR1", self.system.trains)
        self.assertEqual(self.system.trains["TR1"].status.value, "idle")

    def test_assemble_train_missing_entity(self) -> None:
        with self.assertRaises(EntityNotFoundError):
            self.system.assemble_train("TR2", "LOCO99", ["W1"], ["S1", "S2"])

    def test_movement_success(self) -> None:
        dep = datetime(2026, 4, 25, 10, 0)
        arr = datetime(2026, 4, 25, 14, 30)
        self.system.operation_movement("TR1", dep, arr)
        self.assertEqual(len(self.system.schedules), 1)
        self.assertEqual(self.system.trains["TR1"].status.value, "moving")

    def test_movement_invalid_time(self) -> None:
        dep = datetime(2026, 4, 25, 14, 0)
        arr = datetime(2026, 4, 25, 10, 0)
        with self.assertRaises(InvalidScheduleError):
            self.system.operation_movement("TR1", dep, arr)

    def test_security_check_pass(self) -> None:
        self.system.operation_security_control("TR1")
        self.assertEqual(self.system.trains["TR1"].security_status.value, "safe")

    def test_security_check_fail_overload(self) -> None:
        self.system.wagons["W1"].current_load = 100
        with self.assertRaises(SecurityCheckFailedError):
            self.system.operation_security_control("TR1")

    def test_maintenance(self) -> None:
        self.system.operation_maintenance("TR1", "train")
        self.assertEqual(self.system.trains["TR1"].status.value, "maintenance")

    def test_ticket_sales_success(self) -> None:
        self.system.operation_movement("TR1", datetime(2026, 4, 25, 8, 0), datetime(2026, 4, 25, 12, 0))
        ticket_id = self.system.operation_ticket_sales("TR1", "Иванов И.И.", 1500.0)
        self.assertTrue(any(t.id == ticket_id and t.is_sold for t in self.system.tickets))

    def test_ticket_sales_no_schedule(self) -> None:
        with self.assertRaises(TicketSoldOutError):
            self.system.operation_ticket_sales("TR1", "Петров", 1200.0)


if __name__ == "__main__":
    unittest.main()