import java.io.File



// data class Fish(var timer: Int = 8) {
//     fun passTime(): Fish? {
//         if (timer == 0) {
//             timer = 6
//             return Fish()
//         } else {
//             timer--
//             return null
//         }
//     }
// }

// data class Ocean() {
//     private val mapped = mutableMapOf<Fish, Long>()

//     fun registerFish(f: Fish) {
//         mapped.put(f, 1 + mapped.getOrElse(f, 0))
//     }
//     fun registerFish(f: Collection<Fish>) {
//         for (fish in f) {
//             registerFish(fish0)
//         }
//     }

//     fun passTime() {
//         val newFish = denizens.asSequence()
//                           .map{it.passTime()}
//                           .filterNotNull()
//                           .toList()
//         registerFish(newFish)
//     }
//     fun size(): Int {
//         return denizens.size
//     }
// }




import java.io.File

fun solve(forDays: Int, initialState: Map<Int,Long>): Long {
    var state = initialState.toMutableMap()
    repeat(forDays) {
        state = state.asSequence().map { it.key - 1 to it.value}.toMap().toMutableMap()
        val growBy = state.getOrElse(-1) {0}
        state.remove(-1)
        state[6] = state.getOrElse(6){0} + growBy
        state[8] = growBy
    }
    return state.values.sum()
}

var inputs = File("in-p.txt").readLines()
                .flatMap{it.split(',')}
                .map{it.toInt()}
                .groupBy{it}
                .map{it.key to it.value.size.toLong()}
                .toMap()

println(solve(80, inputs))
println(solve(256, inputs))

