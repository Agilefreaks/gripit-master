import unittest

from gripit.core.id_map import IdMap
from gripit.config import Config


class TestIdMap(unittest.TestCase):
    def setUp(self):
        self.min_id = 3
        self.max_id = 5
        self.id_map = IdMap(self.min_id, self.max_id)

    def test_constructor_always_generates_slave_addresses_using_the_given_values(self):
        self.assertEqual(self.id_map.all_ids, [3, 4, 5])

    def test_constructor_always_sets_all_ids_as_unassigned(self):
        self.assertEqual(self.id_map.unassigned_ids, self.id_map.all_ids)

    def test_constructor_always_has_no_assigned_ids(self):
        self.assertEqual(self.id_map.assigned_ids, [])

    def test_set_as_assigned_with_invalid_ids_does_not_modify_assigned_ids(self):
        ids = [1, 2]

        self.id_map.set_as_assigned(ids)

        self.assertEqual(self.id_map.assigned_ids, [])

    def test_set_as_assigned_with_valid_ids_does_not_modify_all_ids(self):
        ids = [3, 4]

        self.id_map.set_as_assigned(ids)

        self.assertEqual(self.id_map.all_ids, [3, 4, 5])

    def test_set_as_assigned_with_valid_ids_updates_assigned_ids(self):
        ids = [3, 4]

        self.id_map.set_as_assigned(ids)

        self.assertEqual(self.id_map.assigned_ids, ids)

    def test_set_as_assigned_with_valid_ids_will_remove_given_ids_from_unassigned_ids(self):
        ids = [3, 4]

        self.id_map.set_as_assigned(ids)

        self.assertEqual(self.id_map.unassigned_ids, [5])

    def test_to_bit_mask_returns_a_mask_of_given_bits(self):
        self.id_map.set_as_assigned([5])

        result = self.id_map.to_bit_mask()

        # the bit mask will be created by giving higher index elements a more significant
        # bit position
        self.assertEqual(result, int('100', 2))

    def test_set_as_assigned_with_already_assigned_ids_does_add_duplicates(self):
        ids = [3, 4]

        self.id_map.set_as_assigned(ids)
        self.id_map.set_as_assigned(ids)

        self.assertEqual(self.id_map.assigned_ids, [3, 4])
