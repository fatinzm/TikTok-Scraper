import express from "express";
import { downloadLast2TiktokVideos } from "../utils/tiktokDownloader";
import { runValidation } from "../utils/validator";

const router = express.Router();

router.post("/", async (req, res) => {
  const { username } = req.body;
  if (!username) return res.status(400).json({ error: "Username is required" });

  try {
    const videoPaths = await downloadLast2TiktokVideos(username);
    const results = await Promise.all(videoPaths.map(runValidation));
    res.json({ username, results });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Something went wrong" });
  }
});

export default router;
