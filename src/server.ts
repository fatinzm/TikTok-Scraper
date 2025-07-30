import express from "express";
import dotenv from "dotenv";
import validateTiktokRouter from "./routes/validateTiktok";

dotenv.config();
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use("/validate-tiktok", validateTiktokRouter);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
