import { countRequirement, getRandomChar, generatePassword } from '../static/password_generation.js';

const LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
const UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const NUMBER = '0123456789';
const SPECIAL_CHAR = '#?!@$%^&*-\'+()_[]';


test('getRandomChar return char if single possibility', () => {
    let random_char = getRandomChar('a');

    expect(random_char).toBe('a');
});

test('getRandomChar return one of given possibilities', () => {
    let possibilities = 'abcdef';
    let random_char = getRandomChar(possibilities);

    expect(possibilities.includes(random_char)).toBe(true);
});

test('password length is correct', async () => {
    let expected_length = 7;

    let password = await generatePassword(expected_length);

    expect(password).toHaveLength(expected_length);
});

test('password only have lowercase by default', async () => {
    let expected_length = 7;

    let password = await generatePassword(expected_length);

    expect(password).toMatch(/[a-z]+/);
});

test('countRequirement is 0 if chars are not present', async () => {
    expect(countRequirement('abc', 'def')).toBe(0);
});

test('countRequirement is 1 if chars match a single time', async () => {
    expect(countRequirement('abcd', 'def')).toBe(1);
});

test('countRequirement counts duplicate', async () => {
    expect(countRequirement('abba', 'bcd')).toBe(2);
});

test('password with minimum 1 uppercase', async () => {
    let expected_length = 7;
    let min_uppercase = 1;

    let password = await generatePassword(
        expected_length,
        0,
        true,
        min_uppercase,
    );

    let uppercase_count = countRequirement(password, UPPERCASE);
    expect(uppercase_count).toBeGreaterThanOrEqual(min_uppercase);
});

test('password with minimum 5 uppercase', async () => {
    let expected_length = 7;
    let min_uppercase = 5;

    let password = await generatePassword(
        expected_length,
        0,
        true,
        min_uppercase,
    );

    let uppercase_count = countRequirement(password, UPPERCASE);
    expect(uppercase_count).toBeGreaterThanOrEqual(min_uppercase);
});

test('password with minimum 3 uppercase and 3 numbers', async () => {
    let expected_length = 7;
    let min_uppercase = 3;
    let min_number = 3;

    let password = await generatePassword(
        expected_length,
        0,
        true,
        min_uppercase,
        true,
        min_number,
    );

    let uppercase_count = countRequirement(password, UPPERCASE);
    expect(uppercase_count).toBeGreaterThanOrEqual(min_uppercase);
    let number_count = countRequirement(password, NUMBER);
    expect(number_count).toBeGreaterThanOrEqual(min_number);
});

test('password with minimum 3 lowercase and other chars allowed', async () => {
    let expected_length = 7;
    let min_lowercase = 3;

    let password = await generatePassword(
        expected_length,
        min_lowercase,
        true,
        0,
        true,
        0,
        true,
        0,
    );

    let lowercase_count = countRequirement(password, LOWERCASE);
    expect(lowercase_count).toBeGreaterThanOrEqual(min_lowercase);
});

test('password with minimum 4 special chars and other chars allowed', async () => {
    let expected_length = 7;
    let min_special_char = 4;

    let password = await generatePassword(
        expected_length,
        0,
        true,
        0,
        true,
        0,
        true,
        min_special_char,
    );

    let special_char_count = countRequirement(password, SPECIAL_CHAR);
    expect(special_char_count).toBeGreaterThanOrEqual(min_special_char);
});