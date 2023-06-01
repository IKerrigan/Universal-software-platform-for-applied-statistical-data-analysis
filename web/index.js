require('dotenv').config();

const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const express = require('express');
const morgan = require('morgan');
const path = require('path');

class App {
    static async start() {
        const app = new App();

        try {
            await app.configure();
            return app.start();
        } catch (e) {
            console.error(e.message);
        }
    }

    constructor() {
        this.app = express();
    }

    async configure() {
        this.app.use(morgan('tiny'));
        this.app.use(bodyParser.json({ limit: '100mb' }))
        this.app.use(express.static(path.join(__dirname, 'public')));
        this.app.use('/api', require('./routes'));
        this.app.use((err, req, res, next) => {
            console.error(err.stack)
            res.status(500).send('Something broke!')
        })

        await mongoose.connect(process.env.MONGO_URI);
    }

    start() {
        return this.app.listen(process.env.PORT, () => {
            console.log(`Statistical Analysis Server started on port ${process.env.PORT}`)
        });
    }
}

App.start();
