const jwt = require('jsonwebtoken');
const express = require('express');

const { UserModel } = require('../../models');

const router = express.Router();

router.post('/sign-in', async function (req, res) {
    const { email, password } = req.body;
    const user = await UserModel.findOne({ email });

    try {
        const isMatch = await user.comparePassword(password);
        if (!isMatch) {
            throw new Error(`Passwords don't match!`)
        }
    } catch (e) {
        console.error(e.message);
        return res.sendStatus(401);
    }

    console.log('here')

    res.status(200).json({
        token: jwt.sign({ id: user.id }, process.env.JWT_SECRET),
        name: user.firstName + ' ' + user.lastName
    });
});

router.post('/sign-up', async function (req, res) {
    try {
        await UserModel.create(req.body);
    } catch (e) {
        console.error(e.message);
        return res.sendStatus(400);
    }

    res.redirect('/login.html');
});

module.exports = router;