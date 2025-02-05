import { generatePassword } from './password_generation.js';

const passwordGenerationResult = document.getElementById('passwordGenerationResultDiv')

document.getElementById('generatePasswordButton').addEventListener('click', (e) => {
    generatePasswordForUI();
})

function generatePasswordForUI() {
    let length = document.getElementById('passwordLengthInput').value;
    let min_lowercase = 0;  // option not exposed to the user
    let has_uppercase = document.getElementById('hasUpperCaseInput').checked;
    let min_uppercase = parseInt(document.getElementById('minUpperCaseInput').value);

    let has_number = document.getElementById('hasNumberInput').checked;
    let min_number = parseInt(document.getElementById('minNumberInput').value);

    let has_special_char = document.getElementById('hasSpecialCharInput').checked;
    let min_special_char = parseInt(document.getElementById('minSpecialCharInput').value);

    // Weak input verification
    if (min_lowercase + min_uppercase + min_number + min_special_char > length) {
        displayPasswordGenerationInvalidChoice();
        return;
    }

    let password = generatePassword(
        length,
        min_lowercase,
        has_uppercase,
        min_uppercase,
        has_number,
        min_number,
        has_special_char,
        min_special_char,
    );
    displayPasswordGenerationResult(password)
}

function displayPasswordGenerationResult(password){
    passwordGenerationResult.innerHTML = `Mot de passe généré: <div id="passwordGenerated">${password}</div>`
}

function displayPasswordGenerationInvalidChoice(){
    passwordGenerationResult.innerHTML = '❌ Les paramètres ne sont pas cohérent'
}