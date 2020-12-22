use std::collections::{HashSet, VecDeque};

fn main() {
    let mut player_one_hand: VecDeque<usize> = VecDeque::new();
    let mut player_two_hand: VecDeque<usize> = VecDeque::new();
    let mut drawing_for_player_one = true;
    for line in include_str!("day-22-input.txt").lines() {
        if line.len() == 0 {
            drawing_for_player_one = false;
        } else if let Ok(card) = line.parse::<usize>() {
            if drawing_for_player_one {
                player_one_hand.push_back(card);
            } else {
                player_two_hand.push_back(card);
            }
        }
    }

    part_one(player_one_hand.clone(), player_two_hand.clone());
    part_two(player_one_hand.clone(), player_two_hand.clone());
}

fn part_one(mut player_one_hand: VecDeque<usize>, mut player_two_hand: VecDeque<usize>) {
    while player_one_hand.len() > 0 && player_two_hand.len() > 0 {
        do_turn_part_one(&mut player_one_hand, &mut player_two_hand);
    }

    if player_one_hand.len() > 0 {
        println!("p1 wins");
        let score: usize = calculate_hand_score(&player_one_hand);
        println!("Part one = {}", score);
    } else {
        println!("p2 wins");
        let score: usize = calculate_hand_score(&player_two_hand);
        println!("Part one = {}", score);
    }
}

fn calculate_hand_score(hand: &VecDeque<usize>) -> usize {
    hand.iter()
        .rev()
        .enumerate()
        .map(|(i, card)| *card * (i + 1))
        .sum()
}

fn do_turn_part_one(player_one_hand: &mut VecDeque<usize>, player_two_hand: &mut VecDeque<usize>) {
    let p1 = player_one_hand.pop_front().unwrap();
    let p2 = player_two_hand.pop_front().unwrap();
    if p1 > p2 {
        player_one_hand.push_back(p1);
        player_one_hand.push_back(p2);
    } else {
        player_two_hand.push_back(p2);
        player_two_hand.push_back(p1);
    }
}

fn part_two(mut player_one_hand: VecDeque<usize>, mut player_two_hand: VecDeque<usize>) {
    play_game_part_two(&mut player_one_hand, &mut player_two_hand);

    if player_one_hand.len() > 0 {
        println!("p1 wins");
        let score: usize = calculate_hand_score(&player_one_hand);
        println!("Part two = {}", score);
    } else {
        println!("p2 wins");
        let score: usize = calculate_hand_score(&player_two_hand);
        println!("Part two = {}", score);
    }
}

fn play_game_part_two(
    player_one_hand: &mut VecDeque<usize>,
    player_two_hand: &mut VecDeque<usize>,
) -> bool {
    let mut history: HashSet<(VecDeque<usize>, VecDeque<usize>)> = HashSet::new();
    while player_one_hand.len() > 0 && player_two_hand.len() > 0 {
        // has this been played before?
        let game_key = (player_one_hand.clone(), player_two_hand.clone());
        if history.contains(&game_key) {
            return true;
        }

        let p1 = player_one_hand.pop_front().unwrap();
        let p2 = player_two_hand.pop_front().unwrap();

        let player_one_wins = if player_one_hand.len() >= p1 && player_two_hand.len() >= p2 {
            play_game_part_two(
                &mut player_one_hand.clone().into_iter().take(p1).collect(),
                &mut player_two_hand.clone().into_iter().take(p2).collect(),
            )
        } else {
            p1 > p2
        };

        history.insert(game_key);

        if player_one_wins {
            player_one_hand.push_back(p1);
            player_one_hand.push_back(p2);
        } else {
            player_two_hand.push_back(p2);
            player_two_hand.push_back(p1);
        }
    }
    player_one_hand.len() > 0
}
