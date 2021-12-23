package day18

import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class Test {
    @Test
    fun `test simple slit using one number`() {
        val split = split(listOf(Tk.Number(15)))
        val expected = parse("[7,8]")
        assertEquals(split, expected)
    }

    @Test
    fun `test add nothing`() {
        val added = add(listOf(),  parse("[7,8]"))
        val expected = parse("[7,8]")
        assertEquals(added, expected)
    }

    @Test
    fun testParse() {
        val parsed = parse("[1,[2,3]]")
        val expected = listOf(Tk.Open(), Tk.Number(1), Tk.Open(), Tk.Number(2), Tk.Number(3), Tk.Close(), Tk.Close())
        if (parsed != expected) throw Exception()
    }

    @Test
    fun testAdd() {
        val left = parse("[1,2]")
        val right = parse("[3,4]")
        val summed = add(left, right)
        val expected = parse("[[1,2],[3,4]]")
        if (summed != expected) throw Exception()
    }

    @Test
    fun testExplode() {
        val examples = listOf(
            listOf("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            listOf("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            listOf("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            listOf("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
            listOf("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
        )

        for ((before, after) in examples) {
            if (explode(parse(before)) != parse(after)) {
                throw Exception("$before should have been $after")
            }
        }
    }

}
