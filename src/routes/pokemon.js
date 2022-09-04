import { Router } from 'express';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
const pokemonRouter = Router();

pokemonRouter.post('/', async (req, res) => {
  try {
    const data = await prisma.pokemon.create({
      data: req.body,
    });
    return res.json({ success: true, data });
  } catch (err) {
    return res.json({ success: false, data: err });
  }
});

pokemonRouter.get('/', async (req, res) => {
  try {
    const data = await prisma.pokemon.findMany();
    return res.json({ success: true, data });
  } catch (err) {
    return res.json({ success: false, data: err });
  }
});

export default pokemonRouter;
