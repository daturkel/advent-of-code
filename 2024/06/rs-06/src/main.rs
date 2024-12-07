use indexmap::IndexMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

#[derive(Hash, Eq, PartialEq, Clone, Debug, Copy)]
struct Point {
    x: isize,
    y: isize,
}

impl Point {
    fn rotate(self) -> Point {
        match self {
            Point { x: 0, y: 1 } => Point { x: -1, y: 0 },
            Point { x: -1, y: 0 } => Point { x: 0, y: -1 },
            Point { x: 0, y: -1 } => Point { x: 1, y: 0 },
            Point { x: 1, y: 0 } => Point { x: 0, y: 1 },
            _ => Point { x: 0, y: 0 },
        }
    }

    fn move_dir(self, dir: &Point) -> Point {
        Point {
            x: self.x + dir.x,
            y: self.y + dir.y,
        }
    }

    fn in_bounds(self, bounds: Point) -> bool {
        (0..=bounds.x).contains(&self.x) && (0..=bounds.y).contains(&self.y)
    }
}

fn get_journey_length(
    lines: &[&str],
    mut pos: Point,
    mut dir: Point,
    obs_pos: Option<Point>,
    bounds: Point,
) -> Option<IndexMap<(Point, Point), Point>> {
    let mut visited: IndexMap<(Point, Point), Point> = IndexMap::new();
    loop {
        if visited.contains_key(&(pos, dir)) {
            return None;
        }
        visited.insert((pos, dir), pos);
        let next_pos = pos.move_dir(&dir);
        if !next_pos.in_bounds(bounds) {
            break;
        } else if (lines[next_pos.y as usize]
            .chars()
            .nth(next_pos.x as usize)
            .unwrap()
            == '#')
            || (Some(next_pos) == obs_pos)
        {
            dir = dir.rotate();
        } else {
            pos = next_pos;
        }
    }
    Some(visited)
}

fn solve(lines: &[&str]) -> (usize, usize) {
    let bounds = Point {
        x: (lines.len() - 1) as isize,
        y: (lines[0].len() - 1) as isize,
    };
    let mut x = 0;
    let mut y = 0;
    for (maybe_y, &line) in lines.iter().enumerate() {
        if let Some(maybe_x) = line.find('^') {
            x = maybe_x;
            y = maybe_y;
            break;
        }
    }
    let pos = Point {
        x: x as isize,
        y: y as isize,
    };
    let dir = Point { x: 0, y: -1 };
    let mut part_one_dict = get_journey_length(lines, pos, dir, None, bounds).unwrap();
    let part_one_set: HashSet<Point> = part_one_dict.values().cloned().collect();
    let part_one = part_one_set.len();

    let mut solutions: HashSet<Point> = HashSet::new();
    let mut checked: HashSet<Point> = HashSet::new();
    let mut last_dir = Point { x: 0, y: -1 };
    let mut last_pos = Point {
        x: x as isize,
        y: y as isize,
    };
    part_one_dict.shift_remove(&(last_pos, last_dir));
    for &(obs, obs_dir) in part_one_dict.keys() {
        if !checked.contains(&obs) && (last_pos != obs) {
            let check = get_journey_length(lines, last_pos, last_dir, Some(obs), bounds);
            if check.is_none() {
                solutions.insert(obs);
            }
        }
        checked.insert(obs);
        last_dir = obs_dir;
        last_pos = obs;
    }
    (part_one, solutions.len())
}

fn main() {
    let start = Instant::now();
    let path = env::args().nth(1).unwrap_or("../test.txt".to_string());
    let contents = fs::read_to_string(&path).unwrap();
    let lines: Vec<&str> = contents.lines().collect();
    let (part_one, part_two) = solve(&lines);
    let duration = start.elapsed().as_millis();
    println!(
        "part_one={}, part_two={}, done in {} ms",
        part_one, part_two, duration
    );
}
