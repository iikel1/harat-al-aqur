// Starts the dev server in "shared" mode, for putting it behind a Cloudflare
// quick tunnel so someone else can look at it live.
//
//   Terminal 1:  npm run dev:share
//   Terminal 2:  cloudflared tunnel --url http://localhost:4321
//
// cloudflared prints a https://<random>.trycloudflare.com URL - that is the one
// to send. It stays alive only while both commands are running, and it is public
// and unauthenticated, so treat it as a preview link rather than a deployment.
//
// This wrapper exists because setting an env var inline differs between cmd,
// PowerShell and bash; doing it here means one command works in all three.
import { spawn } from 'node:child_process';

const child = spawn('npm', ['run', 'dev'], {
  stdio: 'inherit',
  shell: true,
  env: { ...process.env, TUNNEL: '1' }
});

child.on('exit', (code) => process.exit(code ?? 0));
