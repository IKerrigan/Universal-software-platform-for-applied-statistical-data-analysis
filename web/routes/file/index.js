const express = require('express');

const { FileModel } = require('../../models')

const router = express.Router();

router.get('/list', async function (req, res) {
    let status = 200;

    const files = await FileModel.find({ owner: res.locals.user._id }).select('name _id');
    res.status(status).json({ files: files || [] });
});

router.get('/:name', async function (req, res) {
    let status = 200;

    const file = await FileModel.findOne({ owner: res.locals.user._id, name: req.params.name });

    if (!file) {
        status = 400;
    }

    res.status(status).json({ file });
});



router.post('/', async function (req, res) {
    let { name, content, parsed } = req.body;

    let [n, ext] = name.split('.');
    name = `${n} ${new Date().toString()}.${ext}`

    const file = await FileModel.create({ name, content, parsed, owner: res.locals.user._id })
    res.status(201).json({ file });
});

module.exports = router;