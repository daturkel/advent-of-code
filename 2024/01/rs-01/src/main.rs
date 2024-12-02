use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::time::Instant;

fn main() -> io::Result<()> {
    let start = Instant::now();
    let path = env::args().nth(1).unwrap_or("../test.txt".to_string());
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let (mut first_numbers, mut second_numbers): (Vec<i32>, Vec<i32>) = reader
        .lines()
        .map_while(Result::ok)
        .filter_map(parse_line)
        .unzip();

    // part 1
    first_numbers.sort_unstable(); // faster than sort
    second_numbers.sort_unstable();
    let length = first_numbers.len();
    let mut counts_1: HashMap<i32, i32> = HashMap::with_capacity(length); // preallocate for speed
    let mut counts_2: HashMap<i32, i32> = HashMap::with_capacity(length);

    let total_distance: i32 = first_numbers
        .iter()
        .zip(second_numbers.iter())
        .map(|(&first, &second)| {
            *counts_1.entry(first).or_insert(0) += 1;
            *counts_2.entry(second).or_insert(0) += 1;
            (first - second).abs()
        })
        .sum();

    // part 2
    let mut total = 0;
    for (&number, &count) in &counts_1 {
        total += count * number * *counts_2.entry(number).or_default()
    }
    let duration = start.elapsed().as_millis();
    println!(
        "distance is {}, similarity is {}, done in {} ms",
        total_distance, total, duration
    );
    Ok(())
}

fn parse_line(line: String) -> Option<(i32, i32)> {
    let parts: Vec<&str> = line.split_whitespace().collect();
    if parts.len() == 2 {
        if let (Ok(first), Ok(second)) = (parts[0].parse(), parts[1].parse()) {
            return Some((first, second));
        }
    }
    None
}
