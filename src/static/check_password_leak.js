import { hashPrefix } from './hash.js';

document.addEventListener("keyup", ({key}) => {
    if (key === 'Enter') {
        submitPassword()
    }
})
document.getElementById('submittedPasswordButton').addEventListener('click', (e) => {
    submitPassword();
})

function submitPassword() {
    let password = document.getElementById('submittedPassword').value;
    hashPrefix(password).then(prefix => alert(prefix));
}