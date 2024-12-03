use regex::Regex;
use std::env;
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let path = env::args().nth(1).unwrap_or("../test.txt".to_string());
    let contents = fs::read_to_string(&path).unwrap();
    let mut valid = 0;
    let mut valid_alt = 0;
    let mut do_active = true;
    // (?s) at the beginning makes this work over multiple lines
    let pattern = Regex::new(r"(?s)mul\((\d+),(\d+)\)|(do(?:n't)?\(\))()").unwrap();
    for (_, [first, second]) in pattern.captures_iter(&contents).map(|c| c.extract()) {
        match (first, second) {
            ("do()", _) => do_active = true,
            ("don't()", _) => do_active = false,
            (left, right) => {
                let left: i32 = left.parse().unwrap();
                let right: i32 = right.parse().unwrap();
                valid += left * right;
                if do_active {
                    valid_alt += left * right
                }
            }
        }
    }

    let duration = start.elapsed().as_micros();
    println!(
        "valid={}, valid_alt={}, done in {} µs",
        valid, valid_alt, duration
    );
}
