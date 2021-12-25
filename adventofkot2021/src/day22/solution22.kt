package day22

import java.io.File
import kotlin.math.max
import kotlin.math.min

data class Cuboid(val x0: Long, val x1: Long, val y0: Long, val y1: Long, val z0: Long, val z1: Long) {
    val volume get() = (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)

    private fun isValid() = x0 <= x1 && y0 <= y1 && z0 <= z1

    fun intersection(other: Cuboid): Cuboid? {
        val c = Cuboid(
            max(x0, other.x0),
            min(x1, other.x1),
            max(y0, other.y0),
            min(y1, other.y1),
            max(z0, other.z0),
            min(z1, other.z1)
        )
        return if (c.isValid()) c else null
    }

    fun turnOffBy(obj: Cuboid): List<Cuboid> {
        val intersection = this.intersection(obj)

        if (intersection == null) return listOf(this)
        else if (intersection == this) return emptyList()

        val all = mutableListOf<Cuboid>()
        if (x0 < intersection.x0) {
            all.add(this.copy(x1 = intersection.x0 - 1))
        }
        if (x1 > intersection.x1) {
            all.add(this.copy(x0 = intersection.x1 + 1))
        }
        if (y0 < intersection.y0) {
            all.add(this.copy(x0 = intersection.x0, x1 = intersection.x1, y1 = intersection.y0 - 1))
        }
        if (y1 > intersection.y1) {
            all.add(this.copy(x0 = intersection.x0, x1 = intersection.x1, y0 = intersection.y1 + 1))
        }
        if (z0 < intersection.z0) {
            all.add(intersection.copy(z0 = z0, z1 = intersection.z0 - 1))
        }
        if (z1 > intersection.z0) {
            all.add(intersection.copy(z0 = intersection.z1 + 1, z1 = z1))
        }
        return all.toList()
    }
}

private fun createCuboid(it: String): Pair<Cuboid, Boolean> {
    val (instruction, ranges) = it.split(" ")
    val turnOn = instruction == "on"
    val (x0, x1) = ranges.substringAfter("x=").substringBefore(",y").split("..")
    val (y0, y1) = ranges.substringAfter("y=").substringBefore(",z").split("..")
    val (z0, z1) = ranges.substringAfter("z=").split("..")
    return Cuboid(x0.toLong(), x1.toLong(), y0.toLong(), y1.toLong(), z0.toLong(), z1.toLong()) to turnOn
}


fun main() {
    var cuboids = listOf<Cuboid>()
    File("../day22/in.txt").readLines().forEach { line ->
        val (cuboid, on) = createCuboid(line)
        cuboids = cuboids.flatMap { it.turnOffBy(cuboid) }
        if (on) cuboids = cuboids + cuboid
    }

    val initCuboid = Cuboid(-50, 50, -50, 50, -50, 50)

    println(cuboids.mapNotNull { it.intersection(initCuboid) }.sumOf { it.volume })
    println(cuboids.sumOf { it.volume })

}