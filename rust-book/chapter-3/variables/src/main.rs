fn main() {
    // error because not mut and re-assigned
    // let x = 5;
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is now {x}");
}
