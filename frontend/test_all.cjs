const axios = require('axios');

async function test(username, password) {
    try {
        const res = await axios.post('http://127.0.0.1:8000/api/auth/login', { username: username, password: password });
        console.log('[PASS] ' + username + ' -> ' + res.status);
    } catch (e) {
        console.log('[FAIL] ' + username + ' -> ' + (e.response ? e.response.status : e.message));
    }
}

async function run() {
    await test('admin', 'admin123');
    await test('manager2', 'manager123');
    await test('teller2', 'teller123');
    await test('admin', 'wrong');
}
run();
