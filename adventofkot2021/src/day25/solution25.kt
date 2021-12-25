package day25

import java.io.File


enum class Tk(val ch: String) {
    SEA_CUCUMBER_EAST(">"),
    SEA_CUCUMBER_SOUTH("v"),
    EMPTY(".")
}

class MapState(val state: List<List<Tk>>) {

    override fun equals(other: Any?) = toString() == other.toString()
    override fun hashCode() = toString().hashCode()

    fun move(cucumberFish: Tk): MapState {
        val nextState: MutableList<MutableList<Tk>> = state.map { mutableListOf(*it.toTypedArray()) }.toMutableList()
        val direction = if (Tk.SEA_CUCUMBER_SOUTH == cucumberFish) Pair(1, 0) else Pair(0, 1)
        for (rowi in 0..state.lastIndex) {
            for (coli in 0..state[rowi].lastIndex) {
                if (state[rowi][coli] != cucumberFish) continue

                val nextEmptyCoords = checkEmpty(state, rowi + direction.first, coli + direction.second)
                if (nextEmptyCoords != null) {
                    nextState[rowi][coli] = Tk.EMPTY
                    nextState[nextEmptyCoords.first][nextEmptyCoords.second] = cucumberFish
                }

            }
        }
        return MapState(nextState)
    }

    private fun checkEmpty(state: List<List<Tk>>, ri: Int, ci: Int): Pair<Int, Int>? {
        val rowi =
            if (ri >= 0 && ri < state.size) ri
            else if (ri == -1) state.lastIndex
            else if (ri == state.size) 0
            else throw Exception("should have only been off by 1! [$ri:$ci] $state")

        val coli =
            if (ci >= 0 && ci < state[rowi].size) ci
            else if (ci == -1) state[rowi].lastIndex
            else if (ci == state[rowi].size) 0
            else throw Exception("should have only been off by 1! [$ri:$ci] $state")

        if (state[rowi][coli] != Tk.EMPTY) return null
        return Pair(rowi, coli)
    }

    override fun toString() = state.map { row -> row.joinToString("") { it.ch } }.joinToString("\n")
}

fun List<List<Tk>>.toMapState() = MapState(this)

fun rawToMapState(lines: List<String>) = lines.map { line ->
    line.map { ch ->
        when (ch) {
            '.' -> Tk.EMPTY
            '>' -> Tk.SEA_CUCUMBER_EAST
            'v' -> Tk.SEA_CUCUMBER_SOUTH
            else -> throw Exception("Panik! invalid input $ch")
        }
    }.toList()
}.toList().toMapState()

fun main() {
    var steps = 0
    var state = rawToMapState(File("../day25/in.txt").readLines())
    while(true) {
        var newState = state.move(Tk.SEA_CUCUMBER_EAST)
        newState = newState.move(Tk.SEA_CUCUMBER_SOUTH)
        steps++
        if (state == newState) break
        state = newState
    }
    print(steps)
}