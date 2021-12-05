import java.io.File

fun solve(window: Int): Int {
    var lastValues = ArrayDeque<Int>()

    return File("in.txt").readLines()
        .map<String, Int> { it.trim().toInt() }
        .map<Int, Int> { currentValue ->
            if (lastValues.size < window) {
                lastValues.addLast(currentValue)
                0
            } else {
                val prevWindow = lastValues.sum()
                lastValues.removeFirst()
                lastValues.addLast(currentValue)
                val currWindow = lastValues.sum()
                if (currWindow > prevWindow) 1 else 0
            }
        }.sum()
}

println(solve(window = 1))
println(solve(window = 3))