from strategy import ALL_STRATEGIES
from tournament import run_tournament


def main() -> None:
    results = run_tournament(ALL_STRATEGIES)

    for result in results:
        print(f"  {result.name}")
        print("-" * 60)
        sub_header = (
            f"    {'Opponent':<28} {'My Score':>9} {'Their Score':>12} {'Delta':>7}"
        )
        print(sub_header)
        print("-" * 60)
        sorted_matches = sorted(
            result.match_scores, key=lambda m: m.my_score, reverse=True
        )
        for match in sorted_matches:
            delta = match.my_score - match.opp_score
            sign = "+" if delta >= 0 else ""
            print(
                f"    {match.opponent:<28} {match.my_score:>9} {match.opp_score:>12} {sign}{delta:>6}"
            )
        print("-" * 60)
        print(
            f"    {'TOTAL':<28} {result.total_score:>9}  "
            f"avg/match: {result.average_score:.2f}  "
            f"avg/round: {result.average_score_per_round:.4f}"
        )
        print()

    print(
        f"{'Rank':<5} {'Strategy':<30} {'Matches':>8} {'Total':>8} {'Avg/Match':>11} {'Avg/Round':>11}"
    )

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank:<5} "
            f"{result.name:<30} "
            f"{result.matches_played:>8} "
            f"{result.total_score:>8} "
            f"{result.average_score:>11.2f} "
            f"{result.average_score_per_round:>11.4f}"
        )

    winner = results[0]
    print()
    print("=" * 60)
    print(f"  WINNER: {winner.name}")
    print(f"  Average score per match : {winner.average_score:.2f} years free")
    print(
        f"  Average score per round : {winner.average_score_per_round:.4f} years free"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
