package day21

data class Player(val position: Long, val pointsToWin: Long)

val cache = mutableMapOf<Pair<Player, Player>, Pair<Long, Long>>()

val rollFrequency = listOf(
    3 to 1,
    4 to 3,
    5 to 6,
    6 to 7,
    7 to 6,
    8 to 3,
    9 to 1
)

fun wins(p1: Player, p2: Player): Pair<Long, Long> {
    if (p2.pointsToWin <= 0) return Pair(0, 1)

    val cached = cache[p1 to p2]
    if (cached != null) return cached

    var wins1: Long = 0
    var wins2: Long = 0
    for ((roll, freq) in rollFrequency) {
        val p1newPos = (p1.position + roll) % 10
        val (nextWins2, nextWins1) = wins(
            p2,
            Player(p1newPos, p1.pointsToWin - p1newPos - 1)
        )
        wins1 += freq * nextWins1
        wins2 += freq * nextWins2
    }
    cache[p1 to p2] = wins1 to wins2
    return wins1 to wins2
}

fun main() {
    println(wins(Player(3, 21), Player(7, 21)))
    println(wins(Player(7, 21), Player(9, 21)))
}
