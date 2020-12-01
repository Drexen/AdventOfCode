use std::iter;

static BASE_PATTERN: [i32; 4] = [0, 1, 0, -1];
static RAW_INPUT: &str= "59764635797473718052486376718142408346357676818478503599633670059885748195966091103097769012608550645686932996546030476521264521211192035231303791868456877717957482002303790897587593845163033589025995509264282936119874431944634114034231860653524971772670684133884675724918425789232716494769777580613065860450960426147822968107966020797566015799032373298777368974345143861776639554900206816815180398947497976797052359051851907518938864559670396616664893641990595511306542705720282494028966984911349389079744726360038030937356245125498836945495984280140199805250151145858084911362487953389949062108285035318964376799823425466027816115616249496434133896";

fn main() {
    part_one();
    part_two();
}

fn part_one() {
    let mut input: Vec<i32> = RAW_INPUT
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i32)
        .collect();

    for _ in 0..100 {
        input = calculate_phase(&input);
    }

    println!("Part one: {:?}", input.iter().take(8).collect::<Vec<_>>())
}

fn part_two() {
    let offset: usize = RAW_INPUT
        .chars()
        .take(7)
        .collect::<String>()
        .parse()
        .unwrap();

    let input: Vec<i32> = RAW_INPUT
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i32)
        .cycle()
        .take(10000 * RAW_INPUT.len())
        .skip(offset)
        .collect();

    let mut reversed_input = input.clone();
    reversed_input.reverse();

    for _ in 0..100 {
        reversed_input = calculate_phase_reverse(&reversed_input);
    }

    println!(
        "Part two: {:?}",
        reversed_input.iter().rev().take(8).collect::<Vec<_>>()
    )
}

fn calculate_phase_reverse(reversed_input: &Vec<i32>) -> Vec<i32> {
    let mut output = Vec::new();
    let mut previous = 0;

    for i in 0..reversed_input.len() {
        previous = (reversed_input[i] + previous) % 10;
        output.push(previous);
    }

    output
}

fn calculate_phase(input: &Vec<i32>) -> Vec<i32> {
    let mut output = Vec::new();
    for (index, _) in input.iter().enumerate() {
        let pattern = get_pattern(index as i32);
        let result: i32 = input.iter().zip(pattern).map(|(&v, p)| v * p).sum();
        output.push(result.abs() % 10);
    }

    output
}

fn get_pattern(nth: i32) -> impl Iterator<Item = i32> {
    BASE_PATTERN
        .iter()
        .map(move |&x| iter::repeat(x).take((nth + 1) as usize))
        .flatten()
        .cycle()
        .skip(1)
}
