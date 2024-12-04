use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

const DIRECTIONS: [(isize, isize); 8] = [
    (0, 1),
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (-1, 1),
    (1, -1),
];

fn search_xmas(puzzle: &[&str], x0: isize, y0: isize, xmax: isize, ymax: isize) -> usize {
    let mut count = 0;
    for (dx, dy) in DIRECTIONS {
        let mut remaining = vec!['S', 'A', 'M'];
        let mut x = x0;
        let mut y = y0;
        let mut valid = true;
        while let Some(next_char) = remaining.pop() {
            if (x == 0) & (dx < 0) || (y == 0) & (dy < 0) {
                valid = false;
                break;
            }
            x += dx;
            y += dy;
            if !(0..=xmax).contains(&x)
                || !(0..=ymax).contains(&y)
                || puzzle[y as usize].chars().nth(x as usize) != Some(next_char)
            {
                valid = false;
                break;
            }
        }
        if valid {
            count += 1
        }
    }
    count
}

fn search_x_mas(puzzle: &[&str], x: usize, y: usize) -> usize {
    let valid_mas = HashSet::from([('M', 'A', 'S'), ('S', 'A', 'M')]);
    if (valid_mas.contains(&(
        puzzle[y].chars().nth(x).unwrap(),
        puzzle[y + 1].chars().nth(x + 1).unwrap(),
        puzzle[y + 2].chars().nth(x + 2).unwrap(),
    ))) & (valid_mas.contains(&(
        puzzle[y + 2].chars().nth(x).unwrap(),
        puzzle[y + 1].chars().nth(x + 1).unwrap(),
        puzzle[y].chars().nth(x + 2).unwrap(),
    ))) {
        return 1;
    }
    0
}

fn main() {
    let start = Instant::now();
    let path = env::args().nth(1).unwrap_or("../test.txt".to_string());
    let contents = fs::read_to_string(&path).unwrap();
    let lines: Vec<&str> = contents.lines().collect();
    let xmax = lines.len() - 1;
    let ymax = lines[0].len() - 1;
    let mut xmas_count = 0;
    let mut x_mas_count = 0;

    for (y, &line) in lines.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            if char == 'X' {
                xmas_count +=
                    search_xmas(&lines, x as isize, y as isize, xmax as isize, ymax as isize)
            } else if (x <= xmax - 2) & (y <= ymax - 2) & ['M', 'S'].contains(&char) {
                x_mas_count += search_x_mas(&lines, x, y);
            }
        }
    }

    let duration = start.elapsed().as_micros();
    println!(
        "valid={}, valid_alt={}, done in {} µs",
        xmas_count, x_mas_count, duration
    );
}
