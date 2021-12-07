import java.io.File

fun inputAsInts() = File("in.txt").readLines().map { it.trim().toInt() }
fun List<Int>.solve(window: Int) = this.windowed(window).count { it[window-1] > it[0] }

println(inputAsInts().solve(2))
println(inputAsInts().solve(4))
