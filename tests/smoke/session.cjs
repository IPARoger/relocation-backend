const { execFileSync } = require('node:child_process');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const PYTHON = path.join(ROOT, 'venv/bin/python');

function mintSession() {
  const raw = execFileSync(PYTHON, [path.join(__dirname, 'mint_session.py')], {
    cwd: ROOT,
    env: process.env,
    encoding: 'utf8',
  });
  return JSON.parse(raw.trim());
}

module.exports = { mintSession };
