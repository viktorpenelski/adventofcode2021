import java.io.File

data class Transition(val from: String, val to: String)
data class State(private val map: MutableMap<String, Long>) {

    companion object {
        fun fromString(state: String): State {
            val map = mutableMapOf<String, Long>()
            for (i in 1..state.lastIndex) {
                val pair = "${state[i-1]}${state[i]}"
                map[pair] = map.getOrDefault(pair, 0) + 1
            }
            return State(map)
        }
    }

    fun charOccurrenceMap(): Map<Char, Long> {
        return map.asSequence().groupBy { it.key[1] }
            .mapValues { it.value.sumOf { value -> value.value } }
    }

    fun applyTransitions(transitions: List<Transition>): State {
        val nextMap = mutableMapOf<String, Long>()
        for (transition in transitions) {
            if (!map.containsKey(transition.from)) {
                continue
            }
            nextMap[transition.from[0] + transition.to] = map.getOrDefault(transition.from, 0) + nextMap.getOrDefault(transition.from[0] + transition.to, 0)
            nextMap[transition.to + transition.from[1]] = map.getOrDefault(transition.from, 0) + nextMap.getOrDefault(transition.to + transition.from[1], 0)
        }
        return State(nextMap)
    }
}

fun parseInputs(): Pair<State, List<Transition>> {
    val path = "in.txt"
    val startState = File(path).readLines().take(1)
    val transitions = File(path)
        .readLines()
        .drop(2)
        .map {
            val split = it.split(" -> ")
            Transition(from = split[0], to = split[1])
        }.toList()

    return Pair(State.fromString(startState[0]), transitions)
}


var (state, transitions) = parseInputs()
repeat(10) {
    state = state.applyTransitions(transitions)
}
var charMap = state.charOccurrenceMap()
println(charMap.maxOf { it.value } - charMap.minOf { it.value })
repeat(30) {
    state = state.applyTransitions(transitions)
}
charMap = state.charOccurrenceMap()
println(charMap.maxOf { it.value } - charMap.minOf { it.value })
