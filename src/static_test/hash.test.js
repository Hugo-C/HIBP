import { hashPrefix } from "../static/hash.js";

test('hash prefix is identical to Python version', async () => {
    let prefix = await hashPrefix("rockyou");

    expect(prefix).toBe("5c283");
});