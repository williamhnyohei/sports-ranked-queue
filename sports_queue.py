"""Queue management for sports matches."""

from dataclasses import dataclass, field
from typing import List, Optional

DEFAULT_MMR = 1000


@dataclass
class Player:
    """Represents a single player."""

    player_id: str
    mmr: int = DEFAULT_MMR
    is_dummy: bool = False


@dataclass
class Group:
    """Represents a group of players joining the queue together."""

    players: List[Player] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.players = list(self.players)

    @property
    def size(self) -> int:
        return len(self.players)

    @property
    def avg_mmr(self) -> float:
        if not self.players:
            return 0
        return sum(p.mmr for p in self.players) / self.size

    def __repr__(self) -> str:
        return f"Group(size={self.size}, avg_mmr={self.avg_mmr:.1f})"


class QueueManager:
    SPORT_SLOTS = {
        'futebol': 10,     # 5v5
        'basquete': 10,    # 5v5
        'volei': 12        # 6v6
    }

    def __init__(self) -> None:
        """Initialize empty queues for each sport."""
        self.queues: dict[str, List[Group]] = {
            sport: [] for sport in self.SPORT_SLOTS
        }

    def add_group(self, sport: str, group: Group) -> None:
        """Add a group to the queue for the given sport."""
        if sport not in self.SPORT_SLOTS:
            raise ValueError(f"Sport '{sport}' not supported")
        self.queues[sport].append(group)

    def match_groups(
        self, sport: str, ranked: bool = True, mmr_threshold: int = 100
    ) -> Optional[List[Group]]:
        """Try to form a match for the given sport.

        If ``ranked`` is ``True`` the groups' average MMR must be within
        ``mmr_threshold`` of each other. Returns a list of groups if enough
        players are found, otherwise ``None``.
        """
        if sport not in self.SPORT_SLOTS:
            raise ValueError(f"Sport '{sport}' not supported")
        needed = self.SPORT_SLOTS[sport]
        queue = self.queues[sport]

        selected: List[Group] = []
        total_players = 0
        for group in list(queue):
            if total_players + group.size > needed:
                continue
            if ranked and selected:
                if not self._within_mmr_threshold(selected, group, mmr_threshold):
                    continue
            selected.append(group)
            total_players += group.size
            if total_players == needed:
                break

        if total_players == needed:
            for g in selected:
                queue.remove(g)
            return selected
        return None

    def _within_mmr_threshold(
        self, groups: List[Group], new_group: Group, threshold: int
    ) -> bool:
        """Return True if ``new_group`` fits with ``groups`` by MMR."""
        current_total_mmr = sum(g.avg_mmr * g.size for g in groups)
        current_total_players = sum(g.size for g in groups)
        new_avg = (
            current_total_mmr + new_group.avg_mmr * new_group.size
        ) / (current_total_players + new_group.size)
        return all(
            abs(g.avg_mmr - new_avg) <= threshold for g in groups + [new_group]
        )

if __name__ == "__main__":
    qm = QueueManager()
    # Example usage
    team1 = Group([Player('a1', 1000), Player('a2', 1050), Player('a3', 990)])
    team2 = Group([Player('b1', 1010), Player('b2', 995)])
    team3 = Group([Player('c1', 1020), Player('c2', 1005), Player('c3', 1000), Player('c4', 980), Player('c5', 1015)])

    qm.add_group('futebol', team1)
    qm.add_group('futebol', team2)
    qm.add_group('futebol', team3)

    match = qm.match_groups('futebol', ranked=True)
    print('Match:', match)
