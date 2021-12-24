package day21

import java.io.File

class DeterministicDie(val sides: Int) {
    private var state = 0
    private var rolls = 0
    fun roll() = generateSequence {
        state++
        rolls++
        if (state > sides) {
            state -= sides
        }
        state
    }
    fun timesRolled(): Int {
        return rolls
    }
}

class P(val id: Int, var pos: Int, val targetScore: Int = 1000, val lapSize: Int = 10) {
    var score = 0
    fun move(distance: Int): Boolean {
        pos += distance
        if (pos > lapSize) {
            pos = pos % lapSize
            if (pos == 0) {
                pos = lapSize
            }
        }
        score += pos
        return won()
    }
    fun won(): Boolean {
        return score >= targetScore
    }
}

fun parse(): Pair<P, P> {
    val (p1pos, p2pos) = File("../day21/in.txt").readLines()
        .map { it.trim().split(": ")[1] }
        .mapIndexed { i, pos -> P(i+1, pos.toInt()) }

    return Pair(p1pos, p2pos)
}

fun main() {
    val (p1, p2) = parse()
    val players = listOf(p1, p2)
    val dice = DeterministicDie(100)
    var turn = 0
    while (true) {
        val roll = dice.roll().take(3).sum()
        val activePlayer = players[turn++ % players.size]
        val won = activePlayer.move(roll)
        println("player ${activePlayer.id} rolled ${roll} and moved to ${activePlayer.pos} with score ${activePlayer.score}")
        if (won) {
            break
        }
    }
    val loser = players.sortedBy { it.score }[0]
    println(dice.timesRolled())
    println(loser.score * dice.timesRolled())
}
