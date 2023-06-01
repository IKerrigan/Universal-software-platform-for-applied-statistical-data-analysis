const express = require('express');
const router = express.Router();

const { authenticate } = require('../middlewares');

router.use('/analyse', authenticate, require('./analyse'));
router.use('/weather', authenticate, require('./weather'));
router.use('/file', authenticate, require('./file'));
router.use('/auth', require('./auth'));

module.exports = router;