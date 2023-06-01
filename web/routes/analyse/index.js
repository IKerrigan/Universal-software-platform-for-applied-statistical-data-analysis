const express = require('express');
const axios = require('axios');

const { authenticate } = require('../../middlewares');

const router = express.Router();

router.post('/first-step', authenticate, async function (req, res, next) {
    try {
        const { mode, sv_av } = req.body;
        const data = (await axios.post(process.env.ANALYSER_URL + '/first-step', { mode, sv_av })).data
        res.status(200).json(data);
    } catch (e) {
        next(e)
    }
});

router.post('/second-step', authenticate, async function (req, res, next) {
    try {
        const { mode, sv_av, values } = req.body;
        const data = (await axios.post(process.env.ANALYSER_URL + '/second-step', { mode, sv_av, values })).data
        res.status(200).json(data);
    } catch (e) {
        next(e)
    }
});

module.exports = router;