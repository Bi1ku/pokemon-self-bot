import express from 'express';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import pokemonRouter from './routes/pokemon.js';
import cors from 'cors';

const app = express();

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/', pokemonRouter);

app.listen(3005, () => console.log('Server ready at http://localhost:3005'));

export default app;
