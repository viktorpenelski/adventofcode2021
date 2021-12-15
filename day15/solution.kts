import java.io.File
import java.util.PriorityQueue

data class Node(val risk: Int, val row: Int, val col: Int) {
    var dist: Int = Int.MAX_VALUE
}

fun parseInputs(): List<List<Node>> {
    val path = "in.txt"
    return File(path).readLines()
        .mapIndexed { row, it -> it.mapIndexed{col, ch -> Node(Character.getNumericValue(ch), row, col)}.toList() }
        .toList()
}

fun List<List<Node>>.multiplyBy(multiplier: Int): List<List<Node>> {
    val multiplied = MutableList(this.size * multiplier) {
        MutableList(this[0].size * multiplier) {
            Node(0,0,0)
        }
    }
    fun Int.addRolling9(other: Int): Int {
        var res = this + other
        while (res > 9) {
           res -= 9
        }
        return res
    }

    for (row in 0..this.lastIndex) {
        for (col in 0..this[row].lastIndex) {
            for (i in 0 until multiplier) {
                for (j in 0 until multiplier) {
                    val cRow = row + i*this.size
                    val cCol = col + j*this[row].size
                    val risk = this[row][col].risk.addRolling9(i+j)
                    multiplied[cRow][cCol] = Node(risk, cRow, cCol)
                }
            }
        }
    }
    return multiplied
}

fun getNeighbours(inputs: List<List<Node>>, node: Node): List<Node> {
    val moves = listOf(-1 to 0, 1 to 0, 0 to -1, 0 to 1)
    return moves.asSequence()
                .map { node.row + it.first to node.col + it.second }
                .filter { it.first >= 0 && it.first < inputs.size }
                .filter { it.second >= 0 && it.second < inputs[it.first].size }
                .map { inputs[it.first][it.second] }
                .toList()
}

fun dijkstra(inputs: List<List<Node>>): Node {
    val end = inputs[inputs.lastIndex][inputs[inputs.lastIndex].lastIndex]
    val q = PriorityQueue<Node>() { a, b -> a.dist - b.dist }
    val start = inputs[0][0]
    start.dist = 0
    q.add(start)
    val visited = mutableSetOf<Node>()
    while (!q.isEmpty()) {
        val current = q.remove()
        if (current == end) {
            return current
        }
        if (visited.contains(current)) {
            continue
        }
        val unvisitedNeighbours = getNeighbours(inputs, current).filter { !visited.contains(it) }
        for (neighbour in unvisitedNeighbours) {
            if (neighbour.dist > current.dist + neighbour.risk) {
                neighbour.dist = current.dist + neighbour.risk
            }
        }
        q.addAll(unvisitedNeighbours)
        visited.add(current)
    }

    throw Exception("Couldn't reach an end node")
}

val end = dijkstra(parseInputs())
println(end.dist)
val bigEnd = dijkstra(parseInputs().multiplyBy(5))
println(bigEnd.dist)
