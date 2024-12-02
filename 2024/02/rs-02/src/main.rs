use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::time::Instant;

fn main() -> io::Result<()> {
    let start = Instant::now();
    let path = env::args().nth(1).unwrap_or("../test.txt".to_string());
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);
    let mut valid = 0;
    let mut valid_alt = 0;
    for report in reader
        .lines()
        .map_while(Result::ok)
        .map(|line| line_to_vec(&line))
    {
        if check_valid(&report) {
            valid += 1;
            valid_alt += 1;
        } else {
            for i in 0..=(report.len() - 1) {
                let mut modified_report = report.clone();
                modified_report.remove(i);
                if check_valid(&modified_report) {
                    valid_alt += 1;
                    break;
                }
            }
        }
    }

    let duration = start.elapsed().as_millis();
    println!(
        "valid={}, valid_alt={}, done in {} ms",
        valid, valid_alt, duration
    );
    Ok(())
}

fn line_to_vec(line: &str) -> Vec<i32> {
    line.split_whitespace()
        .map(|l| l.parse().unwrap())
        .collect()
}

fn check_valid(report: &[i32]) -> bool {
    let mut last: Option<&i32> = None;
    let mut sign: Option<bool> = None;
    for num in report {
        if let Some(last_value) = last {
            let diff = last_value - num;
            if !(1..=3).contains(&diff.abs()) {
                return false;
            }
            let new_sign = diff > 0;
            if let Some(sign_value) = sign {
                if sign_value != new_sign {
                    return false;
                }
            }
            sign = Some(new_sign);
        }
        last = Some(num)
    }
    true
}
