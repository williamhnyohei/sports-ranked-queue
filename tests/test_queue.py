import unittest
from sports_queue import Player, Group, QueueManager

class QueueManagerTests(unittest.TestCase):
    def test_ranked_match(self):
        qm = QueueManager()
        g1 = Group([Player('a', 1000), Player('b', 1010)])
        g2 = Group([Player('c', 1005), Player('d', 1005)])
        g3 = Group([Player('e', 1000), Player('f', 990), Player('g', 995)])
        g4 = Group([Player('h', 1005), Player('i', 1000), Player('j', 1005)])
        qm.add_group('futebol', g1)
        qm.add_group('futebol', g2)
        qm.add_group('futebol', g3)
        qm.add_group('futebol', g4)
        match = qm.match_groups('futebol', ranked=True)
        self.assertIsNotNone(match)
        self.assertEqual(sum(g.size for g in match), 10)

    def test_not_enough_players(self):
        qm = QueueManager()
        g1 = Group([Player('a', 1000)])
        g2 = Group([Player('b', 1000)])
        qm.add_group('basquete', g1)
        qm.add_group('basquete', g2)
        match = qm.match_groups('basquete', ranked=True)
        self.assertIsNone(match)

    def test_unranked_ignores_mmr(self):
        qm = QueueManager()
        g1 = Group([Player('a', 1000), Player('b', 1000), Player('c', 1000), Player('d', 1000), Player('e', 1000)])
        g2 = Group([Player('f', 1500), Player('g', 1500), Player('h', 1500), Player('i', 1500), Player('j', 1500)])
        qm.add_group('futebol', g1)
        qm.add_group('futebol', g2)
        match = qm.match_groups('futebol', ranked=False)
        self.assertIsNotNone(match)
        self.assertEqual(sum(g.size for g in match), 10)

    def test_group_with_dummies(self):
        qm = QueueManager()
        group = Group([
            Player('p1', 1000),
            Player('dummy1', 1000, True),
            Player('dummy2', 1000, True),
            Player('dummy3', 1000, True),
            Player('dummy4', 1000, True),
        ])
        qm.add_group('basquete', group)
        qm.add_group('basquete', group)
        match = qm.match_groups('basquete', ranked=True)
        self.assertIsNotNone(match)
        self.assertEqual(sum(g.size for g in match), 10)

if __name__ == '__main__':
    unittest.main()
