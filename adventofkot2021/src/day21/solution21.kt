package day21

data class Player(val position: Long, val points: Long = 0)

val cache = mutableMapOf<Pair<Player, Player>, Pair<Long, Long>>()

val rollFrequencies = mapOf(
    3 to 1,
    4 to 3,
    5 to 6,
    6 to 7,
    7 to 6,
    8 to 3,
    9 to 1
)

fun wins(p1: Player, p2: Player): Pair<Long, Long> {
    if (p2.points >= 21) return Pair(0, 1)

    val cached = cache[p1 to p2]
    if (cached != null) return cached

    val (wins1, wins2) = rollFrequencies.map { (roll, freq) ->
        val p1newPos = (p1.position + roll) % 10
        val (nextWins2, nextWins1) = wins(
            p2,
            Player(p1newPos, p1.points + p1newPos + 1)
        )
        Pair(freq * nextWins1, freq * nextWins2)
    }.reduce { acc, curWins ->
        Pair(acc.first + curWins.first, acc.second + curWins.second)
    }

    cache[p1 to p2] = wins1 to wins2
    return wins1 to wins2
}

fun main() {
    println(wins(Player(3), Player(7)))
    println(wins(Player(7), Player(9)))
}
