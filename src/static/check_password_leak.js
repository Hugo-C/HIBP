import { hashPrefix } from './hash.js';

const API_URL = 'http://localhost:8000/api/v1/haveibeenrocked/';

const passwordLeakCheckResult = document.getElementById('passwordLeakCheckResult')

document.addEventListener('keyup', ({key}) => {
    if (key === 'Enter') {
        submitPassword()
    }
})
document.getElementById('submittedPasswordButton').addEventListener('click', (e) => {
    submitPassword();
})

async function submitPassword() {
    let submittedPassword = document.getElementById('submittedPassword').value;
    let prefix = await hashPrefix(submittedPassword);
    let passwords = await fetchMatchingPasswords(prefix);

    if (passwords.includes(submittedPassword)) {
        passwordIsLeakedResult(submittedPassword)
    } else {
        passwordIsClearedResult(submittedPassword)
    }
}

async function fetchMatchingPasswords(prefix) {
    let response = await fetch(API_URL + prefix);
    let data = await response.json();
    return data[prefix];
}

function passwordIsLeakedResult(submittedPassword){
    passwordLeakCheckResult.innerHTML = `🫠 le mot de passe "${submittedPassword}" est présent dans la base`
    passwordLeakCheckResult.className = "resultLeak";
}

function passwordIsClearedResult(submittedPassword){
    passwordLeakCheckResult.innerHTML = `🥳 le mot de passe "${submittedPassword}" n'est pas dans la base`
    passwordLeakCheckResult.className = "resultClear";
}