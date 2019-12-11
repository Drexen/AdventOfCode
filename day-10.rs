use std::fs;

fn main() {
    let input = fs::read_to_string("src\\day-10-input.txt").unwrap();

    let mut data = Vec::new();
    for line in input.lines() {
        data.push(
            line.chars()
                .map(|x| match x {
                    '.' => false,
                    '#' => true,
                    _ => unreachable!(),
                })
                .collect::<Vec<_>>(),
        );
    }

    let best = part_one(&data);
    part_two(&data, best);
}

fn part_one(data: &Vec<Vec<bool>>) -> (usize, usize) {
    let visible_astroids = data
        .iter()
        .enumerate()
        .map(|(y, line)| {
            line.iter()
                .enumerate()
                .map(|(x, _)| get_visible_asteroids(&data, x, y))
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let mut max = 0;
    let mut coordinate = (0, 0);
    for (y, row) in visible_astroids.iter().enumerate() {
        for (x, _) in row.iter().enumerate() {
            let value = visible_astroids[y][x];
            if value > max {
                max = value;
                coordinate = (x, y);
            }
        }
    }

    println!("Part one: {}", max);

    coordinate
}

#[derive(Debug)]
struct Target {
    x: usize,
    y: usize,
    angle: f32,
    distance: f32,
}

fn get_angle(x1: usize, y1: usize, x2: usize, y2: usize) -> (f32, f32) {
    let mut delta_x = x2 as f32 - x1 as f32;
    let mut delta_y = y2 as f32 - y1 as f32;
    let temp = delta_x;
    delta_x = -delta_y;
    delta_y = temp;
    let mut angle = delta_y.atan2(delta_x);
    if angle < 0.0 {
        angle += 2.0 * std::f32::consts::PI;
    }
    let distance = delta_x.abs() + delta_y.abs();
    (angle, distance)
}

fn part_two(data: &Vec<Vec<bool>>, coordinate: (usize, usize)) {
    let mut angles = Vec::new();
    for (y, row) in data.iter().enumerate() {
        for (x, entry) in row.iter().enumerate() {
            if !entry || (x, y) == coordinate {
                continue;
            }

            let (angle, distance) = get_angle(coordinate.0, coordinate.1, x, y);
            angles.push(Target {
                x,
                y,
                angle,
                distance,
            })
        }
    }

    angles.sort_by(|a, b| {
        let ordering = a.angle.partial_cmp(&b.angle).unwrap();
        if ordering == std::cmp::Ordering::Equal {
            a.distance.partial_cmp(&b.distance).unwrap()
        } else {
            ordering
        }
    });

    let mut targets = angles.iter().map(|x| (x, true)).collect::<Vec<_>>();
    let mut idx = 0;
    let mut count = 0;
    let mut prev_angle = -1.0;
    loop {
        let target = &mut targets[idx];
        if target.0.angle != prev_angle {
            if target.1 {
                count += 1;
                target.1 = false;
                prev_angle = target.0.angle;
            }
        }
        if count == 200 {
            break;
        }

        if idx == angles.len() - 1 {
            prev_angle = -1.0;
        }

        idx = (idx + 1) % angles.len();
    }

    let result = targets[idx].0.x * 100 + targets[idx].0.y;
    println!("Part two: {:?}", result);
}

fn get_visible_asteroids(data: &Vec<Vec<bool>>, x: usize, y: usize) -> u32 {
    if data[y][x] == false {
        return 0;
    }

    let mut visible_asteroids = 0;
    for (y2, row2) in data.iter().enumerate() {
        for (x2, entry2) in row2.iter().enumerate() {
            if !entry2 || (x == x2 && y == y2) {
                continue;
            }
            let delta_x = x2 as i32 - x as i32;
            let delta_y = y2 as i32 - y as i32;
            let delta_x_abs = delta_x.abs();
            let delta_y_abs = delta_y.abs();

            let gcd = gcd(delta_x_abs, delta_y_abs);
            let steps_x = delta_x / gcd;
            let steps_y = delta_y / gcd;

            let mut visible = true;
            for i in 1..gcd {
                let x3 = (x as i32 + (i * steps_x)) as usize;
                let y3 = (y as i32 + (i * steps_y)) as usize;
                if data[y3][x3] {
                    visible = false;
                    break;
                }
            }
            if visible {
                visible_asteroids += 1;
            }
        }
    }
    visible_asteroids
}

fn gcd(mut a: i32, mut b: i32) -> i32 {
    while b > 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
