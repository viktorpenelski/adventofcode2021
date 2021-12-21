import java.io.File
import java.util.concurrent.ForkJoinPool
import kotlin.streams.asStream
import kotlin.streams.toList

data class Point(val x: Int, val y: Int) {
    fun isWithin(rec: Rectangle) =
        x >= rec.botLeft.x && x <= rec.topRight.x
        && y >= rec.botLeft.y && y <= rec.topRight.y

    fun isPast(rec: Rectangle, velocity: Point) =
                y < rec.botLeft.y
                || (x > rec.topRight.x && velocity.x > 0)
                || (x < rec.botLeft.x && velocity.x < 0)
    }

data class Rectangle(val botLeft: Point, val topRight: Point)

data class State(val startPoint: Point, val velocity: Point, val target: Rectangle) {
    private var currentPoint = startPoint.copy()
    private var currentVelocity = velocity.copy()
    private var maxY: Int = Int.MIN_VALUE

    fun simulateSteps(): Int? {
        while (!currentPoint.isPast(target, currentVelocity)) {
            if (currentPoint.y > maxY) {
                maxY = currentPoint.y
            }
            if (currentPoint.isWithin(target)) {
                return maxY
            }
            currentPoint = Point(currentPoint.x+currentVelocity.x, currentPoint.y+currentVelocity.y)
            val xDirection = if (currentVelocity.x > 0) -1 else if (currentVelocity.x < 0) 1 else 0
            currentVelocity = Point(currentVelocity.x + xDirection, currentVelocity.y - 1)
        }
        return null
    }

}

fun parseInputs(): Pair<Point, Point> {
    val regex = "x=(-*\\d+)..(-*\\d+).*y=(-*\\d+)..(-*\\d+)".toRegex()
    return File("in.txt").readLines().take(1)
        .mapNotNull { regex.find(it) }
        .map {
            val (x1, x2, y1, y2) = it.destructured
            Pair(Point(x1.toInt(),y1.toInt()), Point(x2.toInt(), y2.toInt()))
        }.first()
}

val start = Point(0, 0)
val (botLeft, topRight) = parseInputs()
val target = Rectangle(botLeft, topRight)
val shotsInTarget = (0..target.topRight.x).asSequence().asStream().parallel().flatMap<Int> { x ->
    (target.botLeft.y..1000).asSequence().asStream().parallel().map { y ->
        State(start, Point(x,y), target).simulateSteps()
    }.filter { it != null }
}.toList()

val maxY = shotsInTarget.maxOf { it }
val validShots = shotsInTarget.count()

println("maxY: $maxY")
println("valid starting velocities: $validShots ")
