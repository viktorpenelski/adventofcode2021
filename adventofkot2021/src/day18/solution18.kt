package day18

import java.io.File
import kotlin.math.ceil
import kotlin.math.floor
import kotlin.math.max

sealed class Tk {
    data class Open(val tk: Char = '[') : Tk()
    data class Close(val tk: Char = ']') : Tk()
    data class Number(val num: Int) : Tk()

    val unsafeNum get() = (this as Tk.Number).num

}


// [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
fun parse(line: String): List<Tk> {
    return line.toCharArray().asSequence()
        .filter { it != ',' }
        .map<Char, Tk> {
            when (it) {
                '[' -> Tk.Open()
                ']' -> Tk.Close()
                else -> Tk.Number(it.toInt() - '0'.toInt())
            }
        }.toList()
}

fun add(left: List<Tk>, right: List<Tk>): List<Tk> {
    if (left.isEmpty()) return right
    if (right.isEmpty()) return left
    val leftArr = left.toTypedArray()
    val rightArr = right.toTypedArray()
    return listOf<Tk>(Tk.Open(), *leftArr, *rightArr, Tk.Close())
}

fun getExplodeIndex(snailfishNumber: List<Tk>): Int? {
    var opened = 0
    snailfishNumber.forEachIndexed { index, tk ->
        when (tk) {
            is Tk.Open -> opened++
            is Tk.Close -> opened--
            is Tk.Number -> {
                if (opened > 4) {
                    if (snailfishNumber[index + 1] !is Tk.Number) throw Exception("Should have been a num!")
                    if (snailfishNumber[index + 2] !is Tk.Close) throw Exception("Should have been close!")
                    return index
                }
            }
        }
    }
    return null
}

fun explode(snailfishNumber: List<Tk>): Pair<List<Tk>, Boolean> {
    val index = getExplodeIndex(snailfishNumber)
    if (index == null) {
        return Pair(snailfishNumber, false)
    } else {
        val leftSplice = snailfishNumber.slice(0..index - 2).toTypedArray()
        val rightSplice = snailfishNumber.slice(index + 3..snailfishNumber.lastIndex).toTypedArray()
        val lastIdxLeft = leftSplice.indexOfLast { it is Tk.Number }
        val firstIdxRight = rightSplice.indexOfFirst { it is Tk.Number }

        if (lastIdxLeft != -1) {
            leftSplice[lastIdxLeft] =
                Tk.Number(leftSplice[lastIdxLeft].unsafeNum + snailfishNumber[index].unsafeNum)
        }
        if (firstIdxRight != -1) {
            rightSplice[firstIdxRight] =
                Tk.Number(rightSplice[firstIdxRight].unsafeNum + snailfishNumber[index + 1].unsafeNum)
        }

        return Pair(listOf(*leftSplice, Tk.Number(0), *rightSplice), true)
    }

}

fun split(snailfishNumber: List<Tk>): Pair<List<Tk>, Boolean> {
    val toSplit = snailfishNumber.indexOfFirst { it is Tk.Number && it.num >= 10 }
    if (toSplit == -1) return Pair(snailfishNumber, false)
    val leftSplit = snailfishNumber.subList(0, toSplit).toTypedArray()
    val rightSplit = snailfishNumber.subList(toSplit + 1, snailfishNumber.size).toTypedArray()
    val numToSplit = snailfishNumber[toSplit].unsafeNum
    return Pair(
        listOf(
            *leftSplit,
            Tk.Open(),
            Tk.Number(floor(numToSplit / 2.0).toInt()),
            Tk.Number(ceil(numToSplit / 2.0).toInt()),
            Tk.Close(),
            *rightSplit
        ), true
    )
}

fun reduce(snailfishNumber: List<Tk>): List<Tk> {
    var lastNumber = snailfishNumber
    while (true) {
        val (newlyExploded, exploded) = explode(lastNumber)
        lastNumber = newlyExploded
        if (exploded) continue

        val (newlySplit, split) = split(lastNumber)
        lastNumber = newlySplit
        if (!split) return lastNumber
    }
}

fun magnitude(snum: List<Tk>): Int {
    fun rec(l: List<Tk>): Int {
        if (l.size == 0) return 0
        if (l.size == 1) return l.first().unsafeNum
        if (l.size == 2) {
            return 3 * l.first().unsafeNum + 2 * l.last().unsafeNum
        }

        if (l[0] is Tk.Number) {
            return 3 * l.first().unsafeNum + 2 * rec(l.subList(2, l.lastIndex))
        }
        if (l[l.lastIndex] is Tk.Number) {
            return 3 * (rec(l.subList(1, l.lastIndex - 1))) + 2 * l.last().unsafeNum
        }
        var brackets = 0
        var idx = 0
        do {
            if (l[idx] is Tk.Open) brackets++
            else if (l[idx] is Tk.Close) brackets--
            idx++
        } while (brackets > 0)
        val leftSlice = l.subList(1, idx - 1)
        val startRight = idx
        do {
            if (l[idx] is Tk.Open) brackets++
            else if (l[idx] is Tk.Close) brackets--
            idx++
        } while (brackets > 0)
        val rightSlice = l.subList(startRight + 1, idx - 1)
        return 3 * rec(leftSlice) + 2 * rec(rightSlice)
    }

    return rec(snum.subList(1, snum.lastIndex))

}

fun main() {
    val snailfishNumbers = File("../day18/in.txt")
        .readLines()
        .map { parse(it) }

    val sumOfAllInOrder = snailfishNumbers
        .fold(listOf<Tk>()) { acc, next ->
            reduce(add(acc, next))
        }.toList()
    println(magnitude(sumOfAllInOrder))

    var maxMagnitude = -1
    for (i in 0..snailfishNumbers.lastIndex) {
        for (j in i..snailfishNumbers.lastIndex) {
            val sum1 = reduce(add(snailfishNumbers[i], snailfishNumbers[j]))
            val sum2 = reduce(add(snailfishNumbers[j], snailfishNumbers[i]))
            val magnitude = max(magnitude(sum1), magnitude(sum2))
            if (magnitude > maxMagnitude) maxMagnitude = magnitude
        }
    }
    println(maxMagnitude)
}

