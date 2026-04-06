import random
from typing import List, Sequence


class Strategy:
    name = "Strategy"

    def reset(self) -> None:
        """Reset interního stavu před novým zápasem."""

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        raise NotImplementedError


class AlwaysCooperate(Strategy):
    name = "Always Cooperate"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        return "C"


class AlwaysDefect(Strategy):
    name = "Always Defect"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        return "D"


class TitForTat(Strategy):
    name = "Tit For Tat"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        return "C" if not opp_history else opp_history[-1]


class SuspiciousTitForTat(Strategy):
    name = "Suspicious Tit For Tat"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        return "D" if not opp_history else opp_history[-1]


class Grudger(Strategy):
    name = "Grudger (Grim Trigger)"

    def __init__(self) -> None:
        self.grudge = False

    def reset(self) -> None:
        self.grudge = False

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        if "D" in opp_history:
            self.grudge = True
        return "D" if self.grudge else "C"


class PeriodicDDC(Strategy):
    name = "Periodic DDC"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        cycle = ("D", "D", "C")
        return cycle[len(my_history) % len(cycle)]


class PeriodicCCD(Strategy):
    name = "Periodic CCD"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        cycle = ("C", "C", "D")
        return cycle[len(my_history) % len(cycle)]


class Pavlov(Strategy):
    name = "Pavlov (Win-Stay Lose-Shift)"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        if not my_history:
            return "C"
        last_my = my_history[-1]
        last_opp = opp_history[-1]
        if (last_my, last_opp) in (("C", "C"), ("D", "C")):
            return last_my
        return "D" if last_my == "C" else "C"


class RandomStrategy(Strategy):
    name = "Random (p=0.5)"

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        return "C" if self.rng.random() < 0.5 else "D"


class CustomAdaptive(Strategy):
    name = "Custom: Adaptive Strategy"

    def move(self, my_history: Sequence[str], opp_history: Sequence[str]) -> str:
        if not opp_history:
            return "C"

        rounds = len(opp_history)
        opp_defections = opp_history.count("D")
        defections_ratio = opp_defections / rounds

        # Defect if opponent is too aggressive
        if defections_ratio > 0.6:
            return "D"

        # Give chance to cooperate every 10th round
        if rounds % 10 == 0 and defections_ratio <= 0.6:
            return "C"

        # Cooperate if opponent is mostly cooperative
        return opp_history[-1]


ALL_STRATEGIES: List[Strategy] = [
    AlwaysCooperate(),
    AlwaysDefect(),
    TitForTat(),
    SuspiciousTitForTat(),
    Grudger(),
    PeriodicDDC(),
    PeriodicCCD(),
    Pavlov(),
    RandomStrategy(rng=random.Random()),
    CustomAdaptive(),
]
