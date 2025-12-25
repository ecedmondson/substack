use std::io::stdin;
//use std::io::stdin;
use rand::Rng;

fn main() {
    println!("Try to guess the number between 1 - 15. Input:");
    let mut range = rand::thread_rng();
    let random_number: u32 = range.gen_range(0..15);

    let mut guess = String::new();

    // io::stdin().read_line(&mut guess).expect("Failed to read line");
    stdin().read_line(&mut guess).expect("Failed to read line");
    println!("The number was {random_number}. You guessed: {guess}");
}
