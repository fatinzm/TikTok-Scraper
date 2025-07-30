import { exec } from "child_process";
import fs from "fs";
import path from "path";

export function downloadLast2TiktokVideos(username: string): Promise<string[]> {
  return new Promise((resolve, reject) => {
    const script = `python yt_video_fetcher.py ${username}`;
    exec(script, (err, stdout, stderr) => {
      if (err) {
        console.error("Python script error:", stderr);
        return reject(stderr || err.message);
      }
      const lines = stdout.trim().split("\n").filter(Boolean);
      const resolvedPaths = lines.map(file => path.resolve("downloads", file));
      resolve(resolvedPaths);
    });
  });
}
