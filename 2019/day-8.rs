use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[macro_use]
extern crate bmp;
use bmp::{Image, Pixel};

fn main() {
    let f = File::open("src\\day-8-input.txt").unwrap();
    let mut f = BufReader::new(f);

    let mut input = String::new();
    f.read_to_string(&mut input).unwrap();

    let width: u32 = 25;
    let height: u32 = 6;

    let mut chars = input.chars();
    let layers = (0..)
        .map(|_| {
            chars
                .by_ref()
                .take((width * height) as usize)
                .collect::<String>()
        })
        .take_while(|s| !s.is_empty())
        .collect::<Vec<_>>();

    part_one(&layers);
    part_two(&layers, width, height);
}

fn part_one(layers: &Vec<String>) {
    let counts = layers.iter().map(|x| get_digits(x)).collect::<Vec<_>>();

    let zeroes = counts
        .iter()
        .map(|x| x.get(&'0').unwrap_or(&0))
        .collect::<Vec<_>>();

    let min_index = zeroes
        .iter()
        .enumerate()
        .min_by(|(_, a), (_, b)| a.cmp(b))
        .map(|(index, _)| index)
        .unwrap();

    let result =
        counts[min_index].get(&'1').unwrap_or(&0) * counts[min_index].get(&'2').unwrap_or(&0);
    println!("Part one: {:?}", result);
}

fn part_two(layers: &Vec<String>, width: u32, height: u32) {
    let mut pixels = Vec::new();
    for y in 0..height {
        for x in 0..width {
            let idx = x + (y * width);
            let data = layers
                .iter()
                .map(|x| x.chars().nth(idx as usize).unwrap())
                .collect::<Vec<_>>();

            for c in data {
                match c {
                    '0' | '1' => {
                        pixels.push(c);
                        break;
                    }
                    '2' => {
                        continue;
                    }
                    _ => unreachable!(),
                }
            }
        }
    }

    let mut img = Image::new(width, height);

    for (x, y) in img.coordinates() {
        let value = pixels[(x + (y * width)) as usize];
        let rgb = if value == '0' {
            px!(0, 0, 0)
        } else {
            px!(255, 255, 255)
        };
        img.set_pixel(x, y, rgb);
    }
    let filename = "day-8-part2.bmp";
    img.save(filename).unwrap();
    println!("Part two: {:?}", filename);
}

fn get_digits(layer: &String) -> HashMap<char, i32> {
    let mut map = HashMap::new();
    for c in layer.chars() {
        let entry = map.get(&c);
        let new_count = if let Some(count) = entry {
            *count + 1
        } else {
            1
        };
        map.insert(c, new_count);
    }

    map
}
