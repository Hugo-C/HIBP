const LOWERCASE = 'abcdefghijklmnopqrstuvwxyz';
const UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const NUMBER = '0123456789';
const SPECIAL_CHAR = '#?!@$%^&*-\'+()_[]';

/**
 * Generate a password of the given length satisfying the requirements set in the optional parameters
 */
function generatePassword(
        length,
        min_lowercase = 0,
        has_uppercase = false,
        min_uppercase = 0,
        has_number = false,
        min_number = 0,
        has_special_char = false,
        min_special_char = 0,
    ) {
    // We don't check parameters consistency
    let possibleChars = LOWERCASE;
    if (has_uppercase || min_uppercase > 0) {
        possibleChars += UPPERCASE;
    }
    if (has_number || min_number > 0) {
        possibleChars += NUMBER;
    }
    if (has_special_char || min_special_char > 0) {
        possibleChars += SPECIAL_CHAR;
    }

    let password = ''
    do {
        password = _generatePassword(length, possibleChars)
    } while(!checkRequirements(password, min_lowercase, min_uppercase, min_number, min_special_char))
    return password;
}

function _generatePassword(length, possibleChars) {
    let password = ''
    for (var i = 0; i < length; i++) {
        password += getRandomChar(possibleChars)
    }
    return password;
}

/**
 * Validate password requirements. We currently use countRequirement requiring to loop over strings multiple times.
 */
function checkRequirements(password, min_lowercase, min_uppercase, min_number, min_special_char) {
    if (min_lowercase > 0 && countRequirement(password, LOWERCASE) < min_lowercase) {
        return false
    }
    if (min_uppercase > 0 && countRequirement(password, UPPERCASE) < min_uppercase) {
        return false
    }
    if (min_number > 0 && countRequirement(password, NUMBER) < min_number) {
        return false
    }
    if (min_special_char > 0 && countRequirement(password, SPECIAL_CHAR) < min_special_char) {
        return false
    }
    return true;
}

function getRandomChar(possibleChars) {
    if (possibleChars.length >= Math.pow(2, 8)) {
        throw new Error(`possibleChar length (${possibleChars.length}) is too long, some char will never be generated`);
    }
    // Create byte array and fill with 1 random number
    let byteArray = new Uint8Array(1);
    do {
        crypto.getRandomValues(byteArray);
    } while (byteArray[0] >= possibleChars.length)
    return possibleChars[byteArray[0]];
}

function countRequirement(stringTested, charRequirement) {
    let match_count = 0;
    stringTested.split('').forEach((letter) => {
        if (charRequirement.includes(letter)) {
            match_count += 1
        }
    });
    return match_count;
}

export {countRequirement, getRandomChar, generatePassword};