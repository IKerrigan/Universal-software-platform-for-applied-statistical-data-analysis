const jwt = require('jsonwebtoken');

const { UserModel } = require('../models');

async function authenticate(req, res, next) {
    const authHeader = req.headers.authorization;

    try {
        const { id } = jwt.verify(authHeader, process.env.JWT_SECRET);
        res.locals.user = await UserModel.findById(id); 
    } catch (err) {
        console.error(err);
        res.status(401).json({ message: "You need to be logged in to access this resource" });
    }

    return next();
}

module.exports = {
    authenticate
}