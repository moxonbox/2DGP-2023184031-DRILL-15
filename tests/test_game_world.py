import unittest
from unittest.mock import Mock

import game_world


class GameWorldTests(unittest.TestCase):
    def setUp(self):
        game_world.clear()
        game_world.collision_pairs.clear()
        self.addCleanup(game_world.clear)
        self.addCleanup(game_world.collision_pairs.clear)

    def test_registers_collision_sides_separately(self):
        boy, ball1, ball2 = object(), object(), object()
        game_world.add_collision_pair('boy:ball', boy, None)
        game_world.add_collision_pair('boy:ball', None, ball1)
        game_world.add_collision_pair('boy:ball', None, ball2)

        self.assertEqual(game_world.collision_pairs['boy:ball'],
                         [[boy], [ball1, ball2]])

    def test_dispatches_collision_to_both_objects(self):
        boy, ball = Mock(), Mock()
        boy.get_bb.return_value = ball.get_bb.return_value = (0, 0, 10, 10)
        game_world.add_collision_pair('boy:ball', boy, None)
        game_world.add_collision_pair('boy:ball', None, ball)

        game_world.handle_collisions()

        boy.handle_collision.assert_called_once_with('boy:ball', ball)
        ball.handle_collision.assert_called_once_with('boy:ball', boy)

    def test_removes_objects_from_world_and_collision_pairs(self):
        boy, ball = object(), object()
        game_world.add_oject(boy)
        game_world.add_oject(ball, 2)
        game_world.add_collision_pair('boy:ball', boy, ball)

        game_world.remove_object(ball)
        self.assertNotIn(ball, game_world.world[2])
        self.assertEqual(game_world.collision_pairs['boy:ball'], [[boy], []])

        game_world.remove_object(boy)
        self.assertNotIn(boy, game_world.world[1])
        self.assertEqual(game_world.collision_pairs['boy:ball'], [[], []])


if __name__ == '__main__':
    unittest.main()
