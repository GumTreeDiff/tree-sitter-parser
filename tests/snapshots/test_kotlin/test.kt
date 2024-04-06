import kotlin.math.*
import kotlin.math.exp

class Person <T> (val name: String, var age: Int,val t:T) {
    val tt by HashMap()
        set(value){
        }
    init{
        for (item in collection) print(item)
        when(k){
            in collection->{
            }
        }
        try{
        }catch(e:Exception){}
        HashMap<in Any,out Any>()
        if(1 in listOf(1,2,3)){
        }
    }
    @NotNull
    fun sayHello() {
        age as Number
        t as? String
        age is Int
        age !is Int
        name?.let{
            println()
        }
        println("Hello, my name is $name")
    }
    companion object {
        fun createDefaultPerson(): Person {
            return Person("John Doe", 30)!!
        }
    }
}
enum class Enum{
}
interface Interface {
}
object Object{
}

fun Int.isEven(): Boolean {
    return this % 2 == 0
}
fun calculateCircleArea(radius: Double): Double {
    return PI * radius * radius
}
val square: (Int) -> Int = { value -> value * value }

fun main() {
    val message: String = "Hello, Kotlin!"
    var count: Int = 10
    println(message)
    count += 5
    println(count)
    if (count > 0) {
        println("Count is positive")
    } else if (count < 0) {
        println("Count is negative")
    } else {
        println("Count is zero")
    }
    for (i in 1..5) {
        println(i)
    }
    val numbers: List<Int> = listOf(1, 2, 3, 4, 5)
    val doubledNumbers = numbers.map { it * 2 }
    println(doubledNumbers)
    val person = Person("Alice", 25)
    person.sayHello()
    val defaultPerson = Person.createDefaultPerson()
    println(defaultPerson.name)
    println(10.isEven())
    val circleArea = calculateCircleArea(2.5)
    println(circleArea)
    val result = square(5)
    println(result)
}