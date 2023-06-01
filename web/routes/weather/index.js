const express = require('express');
const axios = require('axios');

const { authenticate } = require('../../middlewares');

const router = express.Router();

router.get('/', authenticate, async function (req, res) {
    const { data } = await axios.post(`https://api.openweathermap.org/data/2.5/forecast?lat=50.457015&lon=30.522893&appid=${process.env.OPEN_WEATHER_API_KEY}`)
    res.status(200).json(data);
});

module.exports = router;