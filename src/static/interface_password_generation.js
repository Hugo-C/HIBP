import { generatePassword } from './password_generation.js';

const passwordGenerationResult = document.getElementById('passwordGenerationResultDiv')

document.getElementById('generatePasswordButton').addEventListener('click', (e) => {
    generatePasswordForUI();
})

function generatePasswordForUI() {
    let password = generatePassword(10);
    displayPasswordGenerationResult(password)
}

function displayPasswordGenerationResult(password){
    passwordGenerationResult.innerHTML = `Mot de passe généré: <div id="passwordGenerated">${password}</div>`
}