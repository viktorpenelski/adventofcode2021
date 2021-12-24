package day24

import kotlinx.coroutines.Deferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.runBlocking
import java.io.File
import java.math.BigInteger
import java.util.*

class ALU(val inIter: Iterator<Int>, val commands: Iterable<String>) {
    companion object {
        val SOLUTIONS = Collections.synchronizedList(mutableListOf<String>())
    }

    var vars = mutableMapOf<String, Int>("w" to 0, "x" to 0, "y" to 0, "z" to 0)
    var prefix = ""

    fun String.isNum(): Boolean = this
        .removePrefix("-")
        .removePrefix("+")
        .all { it in '0'..'9' }

    fun String?.value(): Int {
        if (this == null) {
            throw Exception("Should not have been null!")
        } else {
            if (this.isNum()) return this.toInt()
            return vars[this] ?: throw Exception("variable should have been in $vars, but was $this instead")
        }
    }

    fun compute(): Map<String, Int> {
        for (input in commands) {
            val split = input.split(" ")
            val command = split[0]
            val a = split[1]
            val b = if (split.size == 3) split[2] else null
            when (command) {
                "inp" -> {
                    vars[a] = inIter.next()
                    prefix = "$prefix${vars[a]}"
                }
                "add" -> vars[a] = vars[a]!! + b.value()
                "mul" -> vars[a] = vars[a]!! * b.value()
                "div" -> {
                    if (b.value() == 0) {
                        throw ArithmeticException("attempting to divide by 0!")
                    }
                    vars[a] = (vars[a]!! / b.value()).toInt()
                }
                "mod" -> {
                    if (vars[a]!! < 0 || b.value() <= 0) {
                        throw ArithmeticException("attempting to apply modulo on ${vars[a]} and ${b.value()}")
                    }
                    vars[a] = vars[a]!! % b.value()
                }
                "eql" -> if (vars[a] == b.value()) vars[a] = 1 else vars[a] = 0
            }
        }
        return vars
    }
}

fun generator(toYield: String) = sequence {
    var state = toYield
    while (state.isNotEmpty()) {
        val firstDigit = Character.digit(state[0], 10)
        state = state.substring(1)
        yield(firstDigit)
    }
}

fun safeAlu(inputs: String, commands: Iterable<String>): String? {
    val alu = ALU(generator(inputs).iterator(), commands)
    try {
        val finalVars = alu.compute()
        if (finalVars["z"] == 0) {
            // println("found a solution $inputs for $finalVars")
            ALU.SOLUTIONS.add(inputs)
            return inputs
        }
    } catch (ex: Exception) {
        // just return null
    }
    return null
}

fun applyRule(state: String, rule: Map<Pair<Int, Int>, List<Pair<Char, Char>>>): List<String> {
    val applied = mutableListOf<String>()
    val chars = state.toCharArray()
    for (kv in rule) {
        for (value in kv.value) {
            chars[kv.key.first] = value.first
            chars[kv.key.second] = value.second
            applied.add(chars.concatToString())
        }
    }
    return applied
}

fun main() = runBlocking {
    val commands = File("../day24/in.txt").readLines()

    val rule23 = mapOf(Pair(2, 3) to listOf(Pair('1', '8'), Pair('2', '9')))
    val rule45 =
        mapOf(Pair(4, 5) to listOf(Pair('5', '1'), Pair('6', '2'), Pair('7', '3'), Pair('8', '4'), Pair('9', '5')))
    val rule89 = mapOf(
        Pair(8, 9) to listOf(
            Pair('1', '2'),
            Pair('2', '3'),
            Pair('3', '4'),
            Pair('4', '5'),
            Pair('5', '6'),
            Pair('6', '7'),
            Pair('7', '8'),
            Pair('8', '9')
        )
    )
    val rule710 = mapOf(
        Pair(7, 10) to listOf(
            Pair('1', '7'),
            Pair('2', '8'),
            Pair('3', '9')
        )
    )
    val rule611 = mapOf(
        Pair(6, 11) to listOf(
            Pair('1', '9')
        )
    )
    val rules = listOf(rule23, rule45, rule89, rule710, rule611)
    var stack = ArrayDeque<String>()
    stack.addFirst("xxxxxxxxxxxxxx")
    for (rule in rules) {
        val next = mutableListOf<String>()
        while (stack.isNotEmpty()) {
            val pop = stack.pop()
            val applyRule = applyRule(pop, rule)
            for (p in applyRule) {
                next.add(p)
            }
        }
        stack.addAll(next)
    }
    val someValue = stack.peek()
    val unknownIdxs = mutableListOf(someValue.indexOf('x'))
    while (someValue.indexOf('x', unknownIdxs.last() + 1) != -1) {
        unknownIdxs.add(someValue.indexOf('x', unknownIdxs.last() + 1))
    }
    var nextStack = ArrayDeque<String>()
    var replaced = true
    while(replaced) {
        replaced = false
        for (s in stack) {
            if (s.indexOf('x') != -1) {
                replaced = true
                for (i in 1..9) {
                    nextStack.add("${s.substringBefore('x')}$i${s.substringAfter('x')}")
                }
            }
        }
        if (!replaced) break
        stack = nextStack
        nextStack = ArrayDeque<String>()
    }

    print(stack)

    val jobs = mutableListOf<Deferred<String?>>()
    for (num in stack) {
        jobs.add(async(Dispatchers.Default) {
            //println("async $num on thread ${Thread.currentThread().name}")
            safeAlu(num, commands)
        })
    }
    jobs.forEach {
        it.join()
    }

    println(ALU.SOLUTIONS.maxOf { BigInteger(it) })
    println(ALU.SOLUTIONS.minOf { BigInteger(it) })

}