import xxhash from "xxhash-wasm";

async function hashPrefix(password) {
    const { h32, h64 } = await xxhash();
    let digest =  h32(password);
    let hexadecimal_digest = digest.toString(16)
    return hexadecimal_digest.substring(0, 5)
}

export {hashPrefix};