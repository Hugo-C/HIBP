import { hashPrefix } from "../static/check_password_leak.js";

test('hash prefix is identical to Python version', async () => {
    let prefix = await hashPrefix("rockyou");

    expect(prefix).toBe("5c283");
});