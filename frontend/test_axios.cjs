const axios = require('axios');

async function test() {
    try {
        const res = await axios.post('http://127.0.0.1:8000/api/auth/login', { username: 'admin', password: 'admin123' });
        console.log('STATUS:', res.status);
    } catch (e) {
        console.log('ERROR:', e.response ? e.response.status : e.message);
    }
}
test();
