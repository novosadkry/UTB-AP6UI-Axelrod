from strategy import Strategy
from typing import Dict, List, Tuple

ROUNDS = 200
PAYOFFS: Dict[Tuple[str, str], Tuple[int, int]] = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (1, 1),
}


class MatchScore:
    def __init__(self, opponent: str, my_score: int, opp_score: int) -> None:
        self.opponent = opponent
        self.my_score = my_score
        self.opp_score = opp_score


class TournamentResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.total_score: int = 0
        self.matches_played: int = 0
        self.match_scores: List[MatchScore] = []

    @property
    def average_score(self) -> float:
        if self.matches_played == 0:
            return 0.0
        return self.total_score / self.matches_played

    @property
    def average_score_per_round(self) -> float:
        if self.matches_played == 0:
            return 0.0
        return self.total_score / (self.matches_played * ROUNDS)


def play_match(
    strategy_a: Strategy,
    strategy_b: Strategy,
) -> Tuple[int, int]:
    strategy_a.reset()
    strategy_b.reset()

    history_a: List[str] = []
    history_b: List[str] = []
    score_a = 0
    score_b = 0

    for _ in range(ROUNDS):
        move_a = strategy_a.move(history_a, history_b)
        move_b = strategy_b.move(history_b, history_a)

        pay_a, pay_b = PAYOFFS[(move_a, move_b)]
        score_a += pay_a
        score_b += pay_b

        history_a.append(move_a)
        history_b.append(move_b)

    return score_a, score_b


def run_tournament(strategies: List[Strategy]) -> List[TournamentResult]:
    results: Dict[str, TournamentResult] = {
        s.name: TournamentResult(s.name) for s in strategies
    }

    for i in range(len(strategies)):
        for j in range(i, len(strategies)):
            strategy_a = strategies[i]
            strategy_b = strategies[j]

            score_a, score_b = play_match(strategy_a, strategy_b)

            results[strategy_a.name].total_score += score_a
            results[strategy_a.name].matches_played += 1
            results[strategy_a.name].match_scores.append(
                MatchScore(strategy_b.name, score_a, score_b)
            )

            # Count each cross-match exactly once
            if i != j:
                results[strategy_b.name].total_score += score_b
                results[strategy_b.name].matches_played += 1
                results[strategy_b.name].match_scores.append(
                    MatchScore(strategy_a.name, score_b, score_a)
                )

    ranked = sorted(
        results.values(),
        key=lambda r: r.average_score,
        reverse=True,
    )

    return ranked
